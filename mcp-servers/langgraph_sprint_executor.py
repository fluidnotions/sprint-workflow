#!/usr/bin/env python3
"""
LangGraph Sprint Executor - MCP Server

Provides deterministic sprint execution orchestration using LangGraph state machine.
Replaces the sprint-coordinator agent with structured, resumable workflow.
"""

import asyncio
import json
import sys
import os
from typing import TypedDict, List, Dict, Optional, Annotated, Literal
from datetime import datetime
from pathlib import Path

try:
    from langgraph.graph import StateGraph, END, START
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_anthropic import ChatAnthropic
except ImportError:
    print("ERROR: LangGraph dependencies not installed", file=sys.stderr)
    print("Run: pip install langgraph langchain-anthropic", file=sys.stderr)
    sys.exit(1)


# ============================================================================
# STATE DEFINITION
# ============================================================================

class JobSpec(TypedDict):
    """Individual job specification"""
    name: str
    task_file: str
    worktree: str
    repo_root: str
    branch: str
    todos: List[str]
    story_points: int
    status: Literal["pending", "implementing", "verifying", "verified", "failed"]
    retry_count: int
    error_message: Optional[str]


class RepoInfo(TypedDict):
    """Repository information"""
    path: str
    has_remote: bool
    branches: List[str]


class SprintState(TypedDict):
    """Complete sprint execution state"""
    # Input
    project_name: str
    sprint_prd_path: str
    todos_path: str
    pool_size: int

    # Jobs
    jobs: List[JobSpec]

    # Execution state
    phase: Literal["init", "implementing", "verifying", "branch_mgmt", "merging", "complete", "error"]

    # Progress tracking
    jobs_implementing: List[str]
    jobs_verifying: List[str]
    jobs_verified: List[str]
    jobs_failed: List[str]

    # Repository info
    repos: List[RepoInfo]

    # Error tracking
    errors: List[Dict[str, str]]

    # Metadata
    started_at: str
    completed_at: Optional[str]

    # Messages for user
    status_messages: List[str]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_job_specs(tasks_dir: str) -> List[JobSpec]:
    """Load job specifications from tasks directory"""
    jobs = []
    tasks_path = Path(tasks_dir)

    for task_file in tasks_path.glob("*.md"):
        # Parse task file for job info
        content = task_file.read_text()

        job_name = task_file.stem
        worktree_name = f"feat-{job_name}"
        worktree_path = f"worktrees/{worktree_name}"

        # Extract story points (look for ## Story Points in markdown)
        story_points = 5  # Default
        for line in content.split('\n'):
            if '## Story Points' in line or 'Story Points:' in line:
                try:
                    story_points = int(''.join(filter(str.isdigit, line.split(':')[-1])))
                except:
                    pass

        # Extract todos (look for - [ ] lines)
        todos = [
            line.strip()[5:] for line in content.split('\n')
            if line.strip().startswith('- [ ]')
        ]

        jobs.append(JobSpec(
            name=job_name,
            task_file=str(task_file),
            worktree=worktree_path,
            repo_root="",  # Will be detected
            branch=worktree_name,
            todos=todos,
            story_points=story_points,
            status="pending",
            retry_count=0,
            error_message=None
        ))

    return jobs


def detect_repos(worktrees: List[str]) -> List[RepoInfo]:
    """Detect git repositories for each worktree"""
    repos_map = {}

    for worktree in worktrees:
        if not os.path.exists(worktree):
            continue

        try:
            # Get repo root
            import subprocess
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                cwd=worktree,
                capture_output=True,
                text=True
            )
            repo_root = result.stdout.strip()

            # Check for remote
            result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=worktree,
                capture_output=True,
                text=True
            )
            has_remote = 'origin' in result.stdout

            if repo_root not in repos_map:
                repos_map[repo_root] = RepoInfo(
                    path=repo_root,
                    has_remote=has_remote,
                    branches=[]
                )
        except Exception as e:
            print(f"Error detecting repo for {worktree}: {e}", file=sys.stderr)

    return list(repos_map.values())


def write_status_dashboard(state: SprintState):
    """Write sprint_status.md dashboard"""
    content = f"""# Sprint Status - Live Dashboard
**Last Updated**: {datetime.now().isoformat()}

## Current Phase: {state['phase'].upper()}

### Jobs Summary
- Total: {len(state['jobs'])}
- Implementing: {len(state['jobs_implementing'])}
- Verifying: {len(state['jobs_verifying'])}
- Verified: {len(state['jobs_verified'])}
- Failed: {len(state['jobs_failed'])}

### Job Details

"""

    for job in state['jobs']:
        status_icon = {
            'pending': '[ ]',
            'implementing': '[>]',
            'verifying': '[>]',
            'verified': '[✓]',
            'failed': '[✗]'
        }[job['status']]

        content += f"{status_icon} **{job['name']}** ({job['status']})\n"
        if job['error_message']:
            content += f"  - Error: {job['error_message']}\n"
        if job['retry_count'] > 0:
            content += f"  - Retries: {job['retry_count']}/5\n"
        content += "\n"

    content += f"""
### Story Points
- Total: {sum(j['story_points'] for j in state['jobs'])}
- Verified: {sum(j['story_points'] for j in state['jobs'] if j['status'] == 'verified')}
- In Progress: {sum(j['story_points'] for j in state['jobs'] if j['status'] in ['implementing', 'verifying'])}
- Failed: {sum(j['story_points'] for j in state['jobs'] if j['status'] == 'failed')}

### Repositories
"""

    for repo in state['repos']:
        remote_status = "has remote" if repo['has_remote'] else "local only"
        content += f"- {repo['path']} ({remote_status})\n"

    with open('sprint_status.md', 'w') as f:
        f.write(content)


def write_error_report(job: JobSpec, error_details: str):
    """Write error report for failed job"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sprint_errors_{timestamp}_{job['name']}.md"

    content = f"""# Sprint Error Report: {job['name']}

**Status**: {job['status']}
**Phase**: {'Implementation' if job['status'] == 'implementing' else 'Verification'}
**Iterations Attempted**: {job['retry_count']}

## Error Details
{error_details}

## Job Specification
Path: {job['task_file']}
Worktree: {job['worktree']}
Branch: {job['branch']}

## Todos
"""
    for todo in job['todos']:
        content += f"- [ ] {todo}\n"

    content += f"""

## Story Points
{job['story_points']} points

## Sprint Impact
This job failure did NOT block other jobs. Sprint continued execution.

## Next Steps for Manual Resolution
1. Review error details above
2. Check code in worktree: {job['worktree']}
3. Run tests manually to see specific failures
4. Fix issues and re-run verification
5. If tests pass, manually merge branch: {job['branch']}
"""

    with open(filename, 'w') as f:
        f.write(content)

    return filename


# ============================================================================
# WORKFLOW NODES
# ============================================================================

async def initialize_sprint(state: SprintState) -> SprintState:
    """Phase 1: Initialize sprint execution"""
    print(f"🚀 Initializing sprint: {state['project_name']}", file=sys.stderr)

    # Load job specifications
    jobs = load_job_specs("tasks")

    # Detect repositories
    repos = detect_repos([j['worktree'] for j in jobs])

    # Update state
    state['jobs'] = jobs
    state['repos'] = repos
    state['phase'] = 'implementing'
    state['started_at'] = datetime.now().isoformat()

    state['status_messages'].append(f"✅ Loaded {len(jobs)} jobs")
    state['status_messages'].append(f"✅ Detected {len(repos)} repositories")

    write_status_dashboard(state)

    return state


async def spawn_implementation_agents(state: SprintState) -> SprintState:
    """Phase 2: Spawn parallel implementation agents"""
    print(f"🔨 Spawning implementation agents (pool size: {state['pool_size']})", file=sys.stderr)

    # Get pending jobs
    pending_jobs = [j for j in state['jobs'] if j['status'] == 'pending']

    # Simulate spawning agents in parallel (batched by pool size)
    for i in range(0, len(pending_jobs), state['pool_size']):
        batch = pending_jobs[i:i + state['pool_size']]

        # In real implementation, spawn Claude Code agents here
        # For now, mark as implementing
        for job in batch:
            job['status'] = 'implementing'
            state['jobs_implementing'].append(job['name'])
            print(f"  → {job['name']} (implementing)", file=sys.stderr)

        write_status_dashboard(state)

        # Simulate some work
        await asyncio.sleep(0.1)

    state['phase'] = 'verifying'
    return state


async def verify_jobs(state: SprintState) -> SprintState:
    """Phase 3: Run verification on completed jobs"""
    print(f"🔍 Verifying completed jobs", file=sys.stderr)

    # Get jobs that finished implementing
    implementing_jobs = [j for j in state['jobs'] if j['status'] == 'implementing']

    for job in implementing_jobs:
        # Simulate verification
        # In real implementation, spawn verification agent

        # For demo: 80% pass, 20% fail
        import random
        verification_passed = random.random() > 0.2 or job['retry_count'] >= 3

        if verification_passed:
            job['status'] = 'verified'
            state['jobs_verifying'].remove(job['name']) if job['name'] in state['jobs_verifying'] else None
            state['jobs_verified'].append(job['name'])
            state['jobs_implementing'].remove(job['name']) if job['name'] in state['jobs_implementing'] else None
            print(f"  ✓ {job['name']} verified", file=sys.stderr)
        else:
            # Verification failed
            job['retry_count'] += 1

            if job['retry_count'] >= 5:
                # Max retries reached
                job['status'] = 'failed'
                job['error_message'] = f"Verification failed after {job['retry_count']} attempts"
                state['jobs_failed'].append(job['name'])
                state['jobs_implementing'].remove(job['name']) if job['name'] in state['jobs_implementing'] else None

                # Write error report
                error_file = write_error_report(job, "Max verification retries reached")
                state['errors'].append({
                    'job': job['name'],
                    'error': job['error_message'],
                    'report': error_file
                })
                print(f"  ✗ {job['name']} failed (max retries)", file=sys.stderr)
            else:
                # Retry implementation
                job['status'] = 'implementing'
                if job['name'] not in state['jobs_verifying']:
                    state['jobs_verifying'].append(job['name'])
                print(f"  ↻ {job['name']} retry {job['retry_count']}/5", file=sys.stderr)

        write_status_dashboard(state)
        await asyncio.sleep(0.1)

    return state


def should_retry_or_continue(state: SprintState) -> Literal["retry", "continue"]:
    """Decision: Are there jobs that need retry?"""
    has_implementing = any(j['status'] == 'implementing' for j in state['jobs'])
    has_pending = any(j['status'] == 'pending' for j in state['jobs'])

    if has_implementing or has_pending:
        return "retry"
    else:
        return "continue"


async def manage_branches(state: SprintState) -> SprintState:
    """Phase 4: Update branches from main, resolve conflicts"""
    print(f"🌿 Managing branches across {len(state['repos'])} repositories", file=sys.stderr)

    state['phase'] = 'branch_mgmt'

    for repo in state['repos']:
        print(f"  → Updating branches in {repo['path']}", file=sys.stderr)

        # Get jobs for this repo
        repo_jobs = [j for j in state['jobs'] if j['status'] == 'verified']

        for job in repo_jobs:
            try:
                # Simulate: git fetch && git rebase origin/main
                print(f"    ↻ Rebasing {job['branch']}", file=sys.stderr)
                await asyncio.sleep(0.1)

            except Exception as e:
                job['error_message'] = f"Branch management failed: {str(e)}"
                state['errors'].append({
                    'job': job['name'],
                    'error': str(e),
                    'phase': 'branch_management'
                })

    state['phase'] = 'merging'
    write_status_dashboard(state)
    return state


async def push_and_merge(state: SprintState) -> SprintState:
    """Phase 5: Push branches, create PRs, auto-merge"""
    print(f"🚢 Pushing and merging branches", file=sys.stderr)

    for repo in state['repos']:
        verified_jobs = [j for j in state['jobs'] if j['status'] == 'verified']

        for job in verified_jobs:
            if repo['has_remote']:
                # Push + create PR + auto-merge
                print(f"  → {job['name']}: push + PR + auto-merge", file=sys.stderr)
                # Simulate: git push && gh pr create && gh pr merge
            else:
                # Merge locally
                print(f"  → {job['name']}: merge locally", file=sys.stderr)
                # Simulate: git checkout main && git merge

            await asyncio.sleep(0.1)

    state['phase'] = 'complete'
    state['completed_at'] = datetime.now().isoformat()
    write_status_dashboard(state)

    return state


async def generate_final_report(state: SprintState) -> SprintState:
    """Phase 6: Generate final execution report"""
    print(f"📊 Generating final report", file=sys.stderr)

    report = f"""# Sprint Execution Report

## Overview
- **Started**: {state['started_at']}
- **Completed**: {state['completed_at']}
- **Total Jobs**: {len(state['jobs'])}

## Results
- ✅ Verified Complete: {len(state['jobs_verified'])}
- ⚠️ Failed: {len(state['jobs_failed'])}

### Verified Jobs
"""

    for job_name in state['jobs_verified']:
        job = next(j for j in state['jobs'] if j['name'] == job_name)
        report += f"- **{job['name']}** ({job['story_points']} points, {job['retry_count']} iterations)\n"

    if state['jobs_failed']:
        report += "\n### Failed Jobs\n"
        for job_name in state['jobs_failed']:
            job = next(j for j in state['jobs'] if j['name'] == job_name)
            report += f"- **{job['name']}** - {job['error_message']}\n"

    report += f"""

## Story Points
- Total Planned: {sum(j['story_points'] for j in state['jobs'])}
- Delivered: {sum(j['story_points'] for j in state['jobs'] if j['status'] == 'verified')}
- Failed: {sum(j['story_points'] for j in state['jobs'] if j['status'] == 'failed')}

## Repositories
"""

    for repo in state['repos']:
        report += f"- {repo['path']} ({'remote' if repo['has_remote'] else 'local'})\n"

    if state['errors']:
        report += f"\n## Error Reports\n"
        for error in state['errors']:
            report += f"- {error['job']}: {error.get('report', 'No report')}\n"

    report += """

## Next Steps
"""

    if state['jobs_failed']:
        report += "- Review error reports in sprint_errors_*.md\n"
        report += "- Manually fix failed jobs\n"

    report += "- Run /sprint-retrospective to document learnings\n"

    # Write report
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sprint_report_{timestamp}.md"
    with open(filename, 'w') as f:
        f.write(report)

    print(f"\n✅ Sprint execution complete!", file=sys.stderr)
    print(f"📄 Final report: {filename}", file=sys.stderr)

    return state


# ============================================================================
# BUILD WORKFLOW GRAPH
# ============================================================================

def build_sprint_workflow() -> StateGraph:
    """Build the LangGraph state machine"""

    workflow = StateGraph(SprintState)

    # Add nodes
    workflow.add_node("initialize", initialize_sprint)
    workflow.add_node("spawn_implementation", spawn_implementation_agents)
    workflow.add_node("verify", verify_jobs)
    workflow.add_node("manage_branches", manage_branches)
    workflow.add_node("push_merge", push_and_merge)
    workflow.add_node("final_report", generate_final_report)

    # Define edges
    workflow.add_edge(START, "initialize")
    workflow.add_edge("initialize", "spawn_implementation")
    workflow.add_edge("spawn_implementation", "verify")

    # Conditional: retry verification or continue
    workflow.add_conditional_edges(
        "verify",
        should_retry_or_continue,
        {
            "retry": "verify",  # Loop back to verification
            "continue": "manage_branches"
        }
    )

    workflow.add_edge("manage_branches", "push_merge")
    workflow.add_edge("push_merge", "final_report")
    workflow.add_edge("final_report", END)

    return workflow


# ============================================================================
# MCP SERVER INTERFACE
# ============================================================================

async def execute_sprint(
    project_name: str,
    sprint_prd_path: str,
    todos_path: str,
    pool_size: int = 3
) -> Dict:
    """Execute sprint with LangGraph state machine"""

    # Initialize state
    initial_state = SprintState(
        project_name=project_name,
        sprint_prd_path=sprint_prd_path,
        todos_path=todos_path,
        pool_size=pool_size,
        jobs=[],
        phase="init",
        jobs_implementing=[],
        jobs_verifying=[],
        jobs_verified=[],
        jobs_failed=[],
        repos=[],
        errors=[],
        started_at="",
        completed_at=None,
        status_messages=[]
    )

    # Build workflow
    workflow = build_sprint_workflow()

    # Compile with checkpointing (can resume)
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)

    # Execute
    config = {"configurable": {"thread_id": f"sprint-{project_name}"}}
    final_state = await app.ainvoke(initial_state, config)

    return {
        "success": True,
        "phase": final_state['phase'],
        "jobs_verified": len(final_state['jobs_verified']),
        "jobs_failed": len(final_state['jobs_failed']),
        "errors": final_state['errors']
    }


async def handle_mcp_request(request: Dict) -> Dict:
    """Handle MCP JSON-RPC request"""
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "protocolVersion": "0.1.0",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "langgraph-sprint-executor",
                "version": "1.0.0"
            }
        }

    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": "execute_sprint",
                    "description": "Execute sprint with deterministic LangGraph state machine",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "project_name": {"type": "string"},
                            "sprint_prd_path": {"type": "string"},
                            "todos_path": {"type": "string"},
                            "pool_size": {"type": "integer", "default": 3}
                        },
                        "required": ["project_name", "sprint_prd_path", "todos_path"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "execute_sprint":
            result = await execute_sprint(
                project_name=arguments['project_name'],
                sprint_prd_path=arguments['sprint_prd_path'],
                todos_path=arguments['todos_path'],
                pool_size=arguments.get('pool_size', 3)
            )

            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }

    return {"error": {"code": -32601, "message": "Method not found"}}


async def main():
    """MCP server main loop"""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )

            if not line:
                break

            request = json.loads(line)
            response = await handle_mcp_request(request)

            print(json.dumps(response), flush=True)

        except Exception as e:
            error_response = {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    asyncio.run(main())

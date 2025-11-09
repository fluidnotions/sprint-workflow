# Sub-Task 5A: Parallel Implementation Node & Agent Spawning

## Parent Job
Week 5-6: Implementation & Verification

## Story Points
5

## Scope
Implement parallel job execution with agent spawning in batches. Core implementation orchestration logic.

## Can Run in Parallel
YES - Parallel with 5B (verification logic), 5C (retry/error handling)

## Todos
- [ ] Create langgraph/nodes/execution.py module
- [ ] Implement parallel_implementation() node function
- [ ] Batch jobs by pool_size for parallel execution
- [ ] Implement spawn_implementation_agent() async function
- [ ] Read job specification and Sprint PRD for agent context
- [ ] Construct implementation prompt with context
- [ ] Integrate with Claude Code agent spawning (via Task tool or API)
- [ ] Handle agent output and status updates
- [ ] Track implementing jobs in state
- [ ] Write unit tests for parallel batching logic
- [ ] Test implementation agent spawning

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/execution.py (new)
- sprint-workflow/langgraph/state.py (modify - add implementing_jobs field)
- sprint-workflow/tests/langgraph/test_execution_nodes.py (new)

## Dependencies
- Sub-task 4D (needs worktrees setup)

## Blocks
- Sub-task 5D (integration depends on all execution components)

## Implementation Notes
```python
async def parallel_implementation(state: SprintWorkflowState) -> dict:
    """Execute jobs in parallel batches."""
    pool_size = state.get("pool_size", 3)
    jobs = state["jobs"]

    # Filter jobs that need implementation
    pending_jobs = [j for j in jobs if j.get("status") != "verified"]

    # Batch jobs for parallel execution
    batches = create_batches(pending_jobs, pool_size)

    implementing_jobs = []

    for batch in batches:
        # Spawn agents in parallel
        tasks = [
            spawn_implementation_agent(job, state)
            for job in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Track results
        for job, result in zip(batch, results):
            if isinstance(result, Exception):
                implementing_jobs.append({
                    "job_name": job["name"],
                    "status": "error",
                    "error": str(result),
                    "retry_count": job.get("retry_count", 0)
                })
            else:
                implementing_jobs.append({
                    "job_name": job["name"],
                    "status": "implementing",
                    "agent_id": result["agent_id"],
                    "retry_count": job.get("retry_count", 0)
                })

    return {
        "implementing_jobs": implementing_jobs,
        "phase": "implementation_started"
    }

async def spawn_implementation_agent(job: dict, state: SprintWorkflowState) -> dict:
    """Spawn Claude Code implementation agent for job."""
    # Read job specification
    task_file = job["task_file"]
    job_spec = read_file(task_file)

    # Read Sprint PRD
    prd = read_file(state["sprint_prd_path"])

    # Construct implementation prompt
    prompt = f"""
You are an implementation agent working on: {job['name']}

## Job Specification
{job_spec}

## Sprint PRD Context
{prd}

## Worktree
Path: {job['worktree_path']}
Branch: {job['branch']}

## Instructions
1. Implement all todos in the job specification
2. Follow the implementation plan
3. Run tests to verify your work
4. Update the task file with progress
"""

    # Spawn agent via Claude Code API
    # This is a placeholder - actual implementation depends on Claude Code agent API
    agent_id = await spawn_claude_code_agent(
        prompt=prompt,
        working_directory=job["worktree_path"],
        model="claude-sonnet-4-5-20250929"
    )

    return {
        "agent_id": agent_id,
        "job_name": job["name"]
    }

def create_batches(jobs: list, batch_size: int) -> list:
    """Create batches of jobs for parallel execution."""
    return [jobs[i:i + batch_size] for i in range(0, len(jobs), batch_size)]
```

## Success Criteria
- Parallel implementation node implemented
- Batching logic working correctly
- Agent spawning function implemented
- implementing_jobs tracked in state
- Unit tests passing for batching
- Agent spawning tested (mocked)
- Error handling for failed spawns
- Integration with worktrees working

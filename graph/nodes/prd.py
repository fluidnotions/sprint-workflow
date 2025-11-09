"""PRD generation and job creation nodes."""

import json
from typing import Dict, Any
from anthropic import AsyncAnthropic
from ..state import SprintWorkflowState

async def generate_sprint_prd_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Generate Sprint PRD from approved synthesized plan."""
    synthesized_plan = state.get("synthesized_plan", {})
    sprint_theme = state.get("sprint_theme", "")
    
    # For speed, create PRD from synthesized plan without AI call
    prd = {
        "title": f"Sprint PRD: {sprint_theme}",
        "overview": synthesized_plan.get("overview", {}),
        "user_stories": synthesized_plan.get("integrated_stories", []),
        "technical_architecture": synthesized_plan.get("implementation_roadmap", {}),
        "risks": synthesized_plan.get("risk_matrix", {}),
        "execution_plan": synthesized_plan.get("execution_plan", {}),
    }
    
    return {
        "sprint_prd": prd,
        "phase": "job_creation",
        "status_messages": [f"Sprint PRD generated with {len(prd.get('user_stories', []))} stories"]
    }

async def create_jobs_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Create job specifications from PRD."""
    sprint_prd = state.get("sprint_prd", {})
    user_stories = sprint_prd.get("user_stories", [])
    
    # Simple job creation - one job per story for now
    jobs = []
    for idx, story in enumerate(user_stories):
        job = {
            "id": f"job-{idx+1}",
            "name": story.get("id", f"Story {idx+1}"),
            "description": story.get("title", ""),
            "story_points": story.get("story_points", 3),
            "status": "pending",
            "branch": f"feat/{story.get('id', f'story-{idx+1}').lower()}",
            "worktree_path": None,
        }
        jobs.append(job)
    
    return {
        "jobs": jobs,
        "status_messages": [f"Created {len(jobs)} jobs"]
    }

def validate_jobs_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Validate job specifications (stub)."""
    jobs = state.get("jobs", [])
    
    # Simple validation - check for duplicates
    job_names = [j.get("name") for j in jobs]
    duplicates = len(job_names) != len(set(job_names))
    
    validation = {
        "issues": [] if not duplicates else [{"description": "Duplicate job names"}],
        "approved": not duplicates
    }
    
    return {
        "job_validation": validation,
        "status_messages": [f"Validated {len(jobs)} jobs - {'PASS' if validation['approved'] else 'FAIL'}"]
    }

def setup_git_worktrees_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Setup git worktrees for jobs (stub)."""
    jobs = state.get("jobs", [])
    
    # Stub - just mark worktrees as "created"
    worktrees = []
    for job in jobs:
        worktree = {
            "job_id": job.get("id"),
            "branch": job.get("branch"),
            "path": f"/worktrees/{job.get('branch')}",
            "status": "ready"
        }
        worktrees.append(worktree)
    
    return {
        "worktrees": worktrees,
        "phase": "implementation",
        "status_messages": [f"Setup {len(worktrees)} worktrees"]
    }

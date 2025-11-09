# Sub-Task 4D: Git Worktree Setup Node

## Parent Job
Week 4: Job Creation & PRD Generation

## Story Points
2

## Scope
Create git branches and worktrees for each validated job to enable parallel development.

## Can Run in Parallel
YES - Can run parallel with 4C validation (setup can happen during validation)

## Todos
- [ ] Implement setup_git_worktrees() node function
- [ ] Create git branches for each job
- [ ] Set up worktrees in worktrees/ directory
- [ ] Detect repository roots for each worktree
- [ ] Copy environment files to worktrees
- [ ] Add worktrees list to state schema
- [ ] Write unit tests for worktree setup
- [ ] Test worktree setup with multi-repo scenarios

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/jobs.py (modify - add worktree setup)
- sprint-workflow/langgraph/state.py (modify - add worktrees field)
- sprint-workflow/tests/langgraph/test_jobs_nodes.py (modify - add worktree tests)

## Dependencies
- Sub-task 4B (needs jobs list)

## Blocks
- Week 5-6 implementation sub-tasks (need worktrees ready)

## Implementation Notes
```python
async def setup_git_worktrees(state: SprintWorkflowState) -> dict:
    """Create git worktrees for parallel job execution."""
    jobs = state["jobs"]
    worktrees = []

    for job in jobs:
        branch_name = f"feat/{job['name']}"
        worktree_path = f"worktrees/{branch_name}"

        # Create branch
        run_command(f"git branch {branch_name}")

        # Create worktree
        run_command(f"git worktree add {worktree_path} {branch_name}")

        # Detect repo root(s) in worktree
        repo_info = detect_repo_info(worktree_path)

        # Copy environment files
        copy_env_files(worktree_path, repo_info)

        worktrees.append({
            "job_name": job["name"],
            "branch": branch_name,
            "path": worktree_path,
            "repo_info": repo_info
        })

        # Update job with worktree info
        job["worktree_path"] = worktree_path
        job["branch"] = branch_name

    return {
        "worktrees": worktrees,
        "phase": "worktrees_ready"
    }

def detect_repo_info(worktree_path: str) -> dict:
    """Detect repository information in worktree."""
    # Check for multiple repo roots
    # Detect .git directories
    # Return repo boundaries

    repo_roots = []
    for root, dirs, files in os.walk(worktree_path):
        if '.git' in dirs:
            repo_roots.append(root)

    return {
        "roots": repo_roots,
        "has_remote": has_git_remote(worktree_path),
        "main_branch": get_main_branch_name(worktree_path)
    }

def copy_env_files(worktree_path: str, repo_info: dict):
    """Copy environment files to worktree."""
    env_files = ['.env', '.env.local', '.env.development']

    for env_file in env_files:
        if os.path.exists(env_file):
            shutil.copy(env_file, worktree_path)
```

## Success Criteria
- Worktree setup node implemented
- Git branches created for all jobs
- Worktrees created in worktrees/ directory
- Repository roots detected
- Environment files copied
- worktrees list in state schema
- Multi-repo scenarios tested
- Unit tests passing
- Cleanup on failure working

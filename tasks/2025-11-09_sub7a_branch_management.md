# Sub-Task 7A: Branch Management Node

## Parent Job
Week 7: Branch Management & Merging

## Story Points
4

## Scope
Update branches from main, detect conflicts, and group jobs by repository for parallel processing.

## Can Run in Parallel
YES - Parallel with 7B (conflict resolution helpers are independent)

## Todos
- [ ] Create langgraph/nodes/git.py module
- [ ] Implement manage_branches() node function
- [ ] Group jobs by repository root
- [ ] Spawn manage_repo_branches() per repo in parallel
- [ ] Fetch latest from origin
- [ ] Rebase each branch on origin/main
- [ ] Detect merge conflicts
- [ ] Track branch management status in state
- [ ] Write unit tests for branch management
- [ ] Test multi-repo scenarios

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/git.py (new)
- sprint-workflow/langgraph/state.py (modify - add branch_status field)
- sprint-workflow/tests/langgraph/test_git_nodes.py (new)

## Dependencies
- Sub-task 5D (needs verified jobs)

## Blocks
- Sub-task 7C (PR creation waits for branch updates)

## Implementation Notes
```python
async def manage_branches(state: SprintWorkflowState) -> dict:
    """Manage branches for verified jobs."""
    verified_jobs = state.get("verified_jobs", [])

    # Get job details for verified jobs
    jobs_to_merge = [
        job for job in state["jobs"]
        if job["name"] in verified_jobs
    ]

    # Group jobs by repository root
    repos = group_jobs_by_repo(jobs_to_merge)

    # Spawn branch management per repo in parallel
    tasks = [
        manage_repo_branches(repo, jobs, state)
        for repo, jobs in repos.items()
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    branch_status = []
    for repo, result in zip(repos.keys(), results):
        if isinstance(result, Exception):
            branch_status.append({
                "repo": repo,
                "status": "error",
                "error": str(result)
            })
        else:
            branch_status.extend(result)

    return {
        "branch_status": branch_status,
        "phase": "branches_updated"
    }

async def manage_repo_branches(repo: str, jobs: list, state: SprintWorkflowState) -> list:
    """Update branches for a repository."""
    results = []

    for job in jobs:
        worktree_path = job["worktree_path"]
        branch = job["branch"]

        # Change to worktree directory
        os.chdir(worktree_path)

        # Fetch latest
        run_command("git fetch origin")

        # Rebase on main
        rebase_result = run_command("git rebase origin/main", allow_failure=True)

        if rebase_result.returncode != 0:
            # Conflicts detected
            conflicts = detect_conflicts()

            results.append({
                "job_name": job["name"],
                "status": "conflicts",
                "conflicts": conflicts,
                "branch": branch
            })
        else:
            results.append({
                "job_name": job["name"],
                "status": "updated",
                "branch": branch
            })

    return results

def group_jobs_by_repo(jobs: list) -> dict:
    """Group jobs by repository root."""
    repos = {}

    for job in jobs:
        repo_info = job.get("repo_info", {})
        repo_root = repo_info.get("roots", ["."])[0]

        if repo_root not in repos:
            repos[repo_root] = []

        repos[repo_root].append(job)

    return repos

def detect_conflicts() -> list:
    """Detect merge conflicts in current worktree."""
    result = run_command("git diff --name-only --diff-filter=U")
    conflict_files = result.stdout.decode().strip().split("\n")
    return [f for f in conflict_files if f]

def run_command(cmd: str, allow_failure: bool = False):
    """Run shell command and return result."""
    result = subprocess.run(
        cmd.split(),
        capture_output=True
    )

    if not allow_failure and result.returncode != 0:
        raise Exception(f"Command failed: {cmd}\n{result.stderr.decode()}")

    return result
```

## Success Criteria
- Branch management node implemented
- Jobs grouped by repository
- Parallel repo processing working
- Fetch and rebase logic working
- Conflict detection implemented
- branch_status tracked in state
- Multi-repo scenarios tested
- Unit tests passing

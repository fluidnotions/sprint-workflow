# Job: Branch Management & Merging

## Overview
Automate branch management, conflict resolution, PR creation, and merging for verified jobs. Handle multi-repo scenarios, auto-merge when tests pass, and clean up worktrees. Ensures verified work is integrated without manual intervention.

## Story Points
13

## Todos from Sprint
### Branch Management Node
- [ ] Create langgraph/nodes/git.py module
- [ ] Implement manage_branches() node function
- [ ] Group jobs by repository root
- [ ] Spawn manage_repo_branches() per repo in parallel
- [ ] Track branch management status in state
- [ ] Write unit tests for branch management

### Repository Branch Updates
- [ ] Implement manage_repo_branches() async function
- [ ] Fetch latest from origin
- [ ] Rebase each branch on origin/main
- [ ] Detect merge conflicts
- [ ] Track branch update results

### Conflict Resolution
- [ ] Implement auto_resolve_conflicts() helper
- [ ] Handle non-code file conflicts (accept incoming)
- [ ] Apply conflict resolution heuristics for code
- [ ] Flag complex conflicts for manual intervention
- [ ] Add conflict errors to state
- [ ] Test conflict resolution with simulated conflicts

### PR Creation & Merging Node
- [ ] Implement push_and_merge() node function
- [ ] Detect repositories with remote vs local-only
- [ ] Push branches to origin for remote repos
- [ ] Create PRs using gh CLI (create_pr helper)
- [ ] Generate PR descriptions from job specs
- [ ] Write unit tests for PR creation

### Auto-Merge Logic
- [ ] Implement check_pr_tests() helper to wait for CI
- [ ] Auto-merge PRs when tests pass (merge_pr helper)
- [ ] Handle local-only repo merges (merge_local helper)
- [ ] Track merge status in state
- [ ] Flag failed tests for manual review
- [ ] Test auto-merge with simulated PR scenarios

### Cleanup
- [ ] Remove merged worktrees (git worktree remove)
- [ ] Delete merged branches (git branch -d)
- [ ] Track cleanup status
- [ ] Handle cleanup errors gracefully

## Implementation Plan
1. **Create git.py module** - Set up git operations nodes
2. **Implement branch management** - Group jobs by repo, update branches
3. **Implement conflict detection** - Rebase on main, detect conflicts
4. **Implement conflict resolution** - Auto-resolve simple conflicts, flag complex ones
5. **Implement PR creation** - Use gh CLI to create PRs with descriptions
6. **Implement auto-merge** - Wait for CI, merge when tests pass
7. **Implement cleanup** - Remove worktrees and branches after merge
8. **Update state schema** - Add branch_status, merge_status, cleanup_status fields
9. **Write tests** - Test branch management, conflict resolution, PR creation, merging
10. **Integration test** - Test full branch management cycle

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/git.py (new - branch management and merging)
- sprint-workflow/langgraph/state.py (modify - add branch/merge tracking fields)
- sprint-workflow/langgraph/workflow.py (modify - connect git nodes)
- sprint-workflow/tests/langgraph/test_git_nodes.py (new)

## Success Criteria
- All todos complete
- Branch management node updates from main
- Conflict resolution attempted automatically
- PR creation node integrated with gh CLI
- Auto-merge logic for passing tests
- Multi-repo scenarios handled
- Cleanup of merged worktrees
- Manual intervention flagged for conflicts
- Tests passing for all git operations

## Dependencies
- Depends on: Job 5-6 (Implementation) - requires verified jobs
- Required by: Job 8 (Integration) - merged code ready for final testing

## Technical Notes
### Branch Management Architecture
```python
async def manage_branches(state: SprintWorkflowState) -> dict:
    """Manage branches for verified jobs."""
    verified_jobs = state["verified_jobs"]

    # Group jobs by repository root
    repos = group_jobs_by_repo(verified_jobs)

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
```

### Repository Branch Updates
```python
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

            # Attempt auto-resolution
            resolved = auto_resolve_conflicts(conflicts)

            if not resolved:
                # Flag for manual intervention
                results.append({
                    "job_name": job["name"],
                    "status": "conflicts",
                    "conflicts": conflicts
                })
                continue

        results.append({
            "job_name": job["name"],
            "status": "updated",
            "branch": branch
        })

    return results
```

### Conflict Resolution Strategy
```python
def auto_resolve_conflicts(conflicts: list) -> bool:
    """Attempt to auto-resolve conflicts."""
    for conflict_file in conflicts:
        # Non-code files: accept incoming
        if is_non_code_file(conflict_file):
            run_command(f"git checkout --theirs {conflict_file}")
            run_command(f"git add {conflict_file}")
            continue

        # Code files: apply heuristics
        if can_auto_resolve_code(conflict_file):
            apply_resolution_heuristics(conflict_file)
            run_command(f"git add {conflict_file}")
        else:
            # Complex conflict - cannot auto-resolve
            return False

    # All conflicts resolved
    run_command("git rebase --continue")
    return True
```

**Heuristics:**
- Import conflicts: merge both import sets
- Whitespace conflicts: accept incoming
- Documentation conflicts: accept incoming
- Complex logic conflicts: flag for manual review

### PR Creation Pattern
```python
async def push_and_merge(state: SprintWorkflowState) -> dict:
    """Create PRs and merge verified jobs."""
    updated_branches = [b for b in state["branch_status"] if b["status"] == "updated"]
    merge_status = []

    for branch_info in updated_branches:
        job_name = branch_info["job_name"]
        branch = branch_info["branch"]

        # Detect if repo has remote
        has_remote = has_git_remote()

        if has_remote:
            # Push branch
            run_command(f"git push origin {branch}")

            # Create PR
            pr_description = generate_pr_description(job_name, state)
            pr_url = create_pr(branch, pr_description)

            # Wait for CI
            ci_passed = await check_pr_tests(pr_url)

            if ci_passed:
                # Auto-merge
                merge_pr(pr_url)
                merge_status.append({
                    "job_name": job_name,
                    "status": "merged",
                    "pr_url": pr_url
                })
            else:
                merge_status.append({
                    "job_name": job_name,
                    "status": "ci_failed",
                    "pr_url": pr_url
                })
        else:
            # Local-only repo - merge directly
            merge_local(branch)
            merge_status.append({
                "job_name": job_name,
                "status": "merged_local"
            })

    return {
        "merge_status": merge_status,
        "phase": "merging_complete"
    }
```

### PR Description Generation
```markdown
# {Job Name}

## Overview
{Job description from task file}

## Todos Completed
- [x] Todo 1
- [x] Todo 2
...

## Story Points
{from job spec}

## Testing
All tests passing in worktree

## Related
Sprint PRD: {link to PRD}
Task File: {link to task file}
```

### Auto-Merge Logic
```python
async def check_pr_tests(pr_url: str) -> bool:
    """Wait for CI tests to complete."""
    max_wait = 30 * 60  # 30 minutes
    poll_interval = 60  # 1 minute

    elapsed = 0
    while elapsed < max_wait:
        status = get_pr_status(pr_url)

        if status == "success":
            return True
        elif status == "failure":
            return False

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    # Timeout
    return False
```

### Cleanup Pattern
```python
def cleanup_worktrees(state: SprintWorkflowState) -> dict:
    """Remove merged worktrees and branches."""
    merged_jobs = [m for m in state["merge_status"] if m["status"] in ["merged", "merged_local"]]

    for job in merged_jobs:
        worktree_path = get_worktree_path(job["job_name"])
        branch = get_branch_name(job["job_name"])

        # Remove worktree
        run_command(f"git worktree remove {worktree_path}")

        # Delete branch
        run_command(f"git branch -d {branch}")

    return {
        "cleanup_status": "complete"
    }
```

### Testing Strategy
- Mock git commands for deterministic tests
- Simulate conflict scenarios
- Test auto-resolution heuristics
- Mock gh CLI for PR creation
- Test CI wait logic with timeouts
- Test multi-repo scenarios
- Test cleanup with various merge states

# Sub-Task 7C: PR Creation & Auto-Merge

## Parent Job
Week 7: Branch Management & Merging

## Story Points
4

## Scope
Create PRs using gh CLI, wait for CI tests, and auto-merge when passing. Handle both remote and local-only repos.

## Can Run in Parallel
NO - Depends on 7A (needs updated branches)

## Todos
- [ ] Implement push_and_merge() node function
- [ ] Detect repositories with remote vs local-only
- [ ] Push branches to origin for remote repos
- [ ] Create PRs using gh CLI (create_pr helper)
- [ ] Generate PR descriptions from job specs
- [ ] Implement check_pr_tests() helper to wait for CI
- [ ] Auto-merge PRs when tests pass (merge_pr helper)
- [ ] Handle local-only repo merges (merge_local helper)
- [ ] Track merge status in state
- [ ] Flag failed tests for manual review
- [ ] Write unit tests for PR creation
- [ ] Test auto-merge with simulated PR scenarios

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/git.py (modify - add PR and merge logic)
- sprint-workflow/langgraph/state.py (modify - add merge_status field)
- sprint-workflow/tests/langgraph/test_git_nodes.py (modify - add PR/merge tests)

## Dependencies
- Sub-task 7A (needs updated branches)
- Sub-task 7B (conflict resolution must succeed first)

## Blocks
- Sub-task 7D (cleanup waits for merged branches)

## Implementation Notes
```python
async def push_and_merge(state: SprintWorkflowState) -> dict:
    """Create PRs and merge verified jobs."""
    updated_branches = [
        b for b in state.get("branch_status", [])
        if b["status"] == "updated"
    ]
    merge_status = []

    for branch_info in updated_branches:
        job_name = branch_info["job_name"]
        branch = branch_info["branch"]

        # Find job details
        job = find_job_by_name(state["jobs"], job_name)

        # Detect if repo has remote
        has_remote = job["repo_info"].get("has_remote", False)

        if has_remote:
            # Push branch
            os.chdir(job["worktree_path"])
            run_command(f"git push origin {branch}")

            # Create PR
            pr_description = generate_pr_description(job, state)
            pr_url = create_pr(branch, pr_description, job)

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
            merge_local(branch, job)
            merge_status.append({
                "job_name": job_name,
                "status": "merged_local"
            })

    return {
        "merge_status": merge_status,
        "phase": "merging_complete"
    }

def generate_pr_description(job: dict, state: SprintWorkflowState) -> str:
    """Generate PR description from job specification."""
    # Read job spec
    job_spec = read_file(job["task_file"])

    # Parse todos and description
    description = f"""# {job['name']}

## Overview
{extract_overview(job_spec)}

## Todos Completed
{extract_completed_todos(job_spec)}

## Story Points
{job.get('story_points', 'Unknown')}

## Testing
All tests passing in worktree.

## Related
- Sprint PRD: {state['sprint_prd_path']}
- Task File: {job['task_file']}
"""
    return description

def create_pr(branch: str, description: str, job: dict) -> str:
    """Create PR using gh CLI."""
    # Write description to temp file
    desc_file = f"/tmp/pr_desc_{job['name']}.md"
    with open(desc_file, 'w') as f:
        f.write(description)

    # Create PR
    result = run_command(
        f"gh pr create --base main --head {branch} --title '{job['name']}' --body-file {desc_file}"
    )

    # Parse PR URL from output
    pr_url = result.stdout.decode().strip().split('\n')[-1]
    return pr_url

async def check_pr_tests(pr_url: str) -> bool:
    """Wait for CI tests to complete."""
    max_wait = 30 * 60  # 30 minutes
    poll_interval = 60  # 1 minute

    elapsed = 0
    while elapsed < max_wait:
        # Check PR status
        result = run_command(f"gh pr view {pr_url} --json statusCheckRollup")
        status_data = json.loads(result.stdout.decode())

        rollup = status_data.get("statusCheckRollup", [])

        if not rollup:
            # No CI configured
            return True

        # Check if all checks passed
        all_passed = all(
            check.get("conclusion") == "SUCCESS"
            for check in rollup
        )

        if all_passed:
            return True

        # Check for failures
        any_failed = any(
            check.get("conclusion") == "FAILURE"
            for check in rollup
        )

        if any_failed:
            return False

        # Still running
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    # Timeout
    return False

def merge_pr(pr_url: str):
    """Merge PR using gh CLI."""
    run_command(f"gh pr merge {pr_url} --auto --squash")

def merge_local(branch: str, job: dict):
    """Merge branch locally (no remote)."""
    os.chdir(job["worktree_path"])
    run_command("git checkout main")
    run_command(f"git merge {branch}")
```

## Success Criteria
- push_and_merge() node implemented
- Remote detection working
- PR creation with gh CLI working
- PR descriptions generated correctly
- CI wait logic implemented
- Auto-merge on passing tests
- Local merge for no-remote repos
- merge_status tracked in state
- Unit tests passing
- Integration tested with mocked gh CLI

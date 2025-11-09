# Sub-Task 7D: Worktree & Branch Cleanup

## Parent Job
Week 7: Branch Management & Merging

## Story Points
2

## Scope
Clean up merged worktrees and branches after successful merge.

## Can Run in Parallel
YES - Parallel with 7C (can cleanup as merges complete)

## Todos
- [ ] Remove merged worktrees (git worktree remove)
- [ ] Delete merged branches (git branch -d)
- [ ] Track cleanup status in state
- [ ] Handle cleanup errors gracefully
- [ ] Preserve failed job worktrees for debugging
- [ ] Write unit tests for cleanup
- [ ] Test cleanup with various merge states

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/git.py (modify - add cleanup)
- sprint-workflow/langgraph/state.py (modify - add cleanup_status field)
- sprint-workflow/tests/langgraph/test_git_nodes.py (modify - add cleanup tests)

## Dependencies
- Sub-task 7C (needs merge status to know what to clean)

## Blocks
- None (final cleanup step)

## Implementation Notes
```python
def cleanup_worktrees(state: SprintWorkflowState) -> dict:
    """Remove merged worktrees and branches."""
    merge_status = state.get("merge_status", [])
    cleanup_status = []

    for merge_info in merge_status:
        if merge_info["status"] not in ["merged", "merged_local"]:
            # Don't cleanup failed or unmerged jobs
            continue

        job_name = merge_info["job_name"]
        job = find_job_by_name(state["jobs"], job_name)

        worktree_path = job["worktree_path"]
        branch = job["branch"]

        try:
            # Remove worktree
            run_command(f"git worktree remove {worktree_path}", allow_failure=True)

            # Delete branch
            run_command(f"git branch -d {branch}", allow_failure=True)

            cleanup_status.append({
                "job_name": job_name,
                "status": "cleaned",
                "worktree_path": worktree_path,
                "branch": branch
            })
        except Exception as e:
            cleanup_status.append({
                "job_name": job_name,
                "status": "cleanup_failed",
                "error": str(e)
            })

    return {
        "cleanup_status": cleanup_status,
        "phase": "cleanup_complete"
    }

def preserve_failed_worktrees(state: SprintWorkflowState):
    """Preserve worktrees for failed jobs for debugging."""
    failed_jobs = state.get("failed_jobs", [])

    print("\n" + "="*60)
    print("FAILED JOBS - Worktrees Preserved for Debugging")
    print("="*60)

    for job_name in failed_jobs:
        job = find_job_by_name(state["jobs"], job_name)
        print(f"\n{job_name}:")
        print(f"  Worktree: {job['worktree_path']}")
        print(f"  Branch: {job['branch']}")
        print(f"  Task File: {job['task_file']}")

    print("\nTo manually fix and merge:")
    print("1. cd <worktree_path>")
    print("2. Fix issues")
    print("3. git add . && git commit")
    print("4. git push origin <branch>")
    print("5. Create PR manually")
```

## Success Criteria
- Cleanup function implemented
- Worktrees removed for merged jobs
- Branches deleted for merged jobs
- Failed job worktrees preserved
- Cleanup errors handled gracefully
- cleanup_status tracked in state
- Unit tests passing
- Integration with merge status working

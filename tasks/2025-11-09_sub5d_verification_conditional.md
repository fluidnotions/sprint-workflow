# Sub-Task 5D: Verification Conditional Edge & Integration

## Parent Job
Week 5-6: Implementation & Verification

## Story Points
2

## Scope
Implement conditional routing logic for verification loop and integrate all execution components.

## Can Run in Parallel
NO - Depends on 5A, 5B, 5C (needs all execution components)

## Todos
- [ ] Implement should_continue_verification() decision function
- [ ] Check for jobs still implementing or verifying
- [ ] Route to retry or continue to branch management
- [ ] Add conditional edge to workflow graph
- [ ] Test verification loop termination conditions
- [ ] Test mixed scenarios (some verified, some failed, some implementing)
- [ ] Integration test for full implementation cycle

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/execution.py (modify - add decision function)
- sprint-workflow/langgraph/workflow.py (modify - add conditional edge)
- sprint-workflow/tests/langgraph/test_execution_nodes.py (modify - add integration tests)

## Dependencies
- Sub-task 5A (needs implementation logic)
- Sub-task 5B (needs verification logic)
- Sub-task 5C (needs retry/error handling)

## Blocks
- Week 7 sub-tasks (branch management waits for verified jobs)

## Implementation Notes
```python
def should_continue_verification(state: SprintWorkflowState) -> str:
    """Decision function for verification loop."""
    implementing_jobs = state.get("implementing_jobs", [])

    # Check for jobs still implementing
    still_implementing = [
        j for j in implementing_jobs
        if j.get("status") in ["implementing", "verification_failed"]
    ]

    # Check for jobs pending verification
    pending_verification = [
        j for j in implementing_jobs
        if j.get("status") == "pending_verification"
    ]

    if still_implementing or pending_verification:
        # Continue verification loop
        return "continue_verification"
    else:
        # All jobs reached terminal state (verified or failed)
        return "proceed_to_branch_mgmt"

# In workflow.py
workflow.add_edge("parallel_implementation", "verification_loop")
workflow.add_conditional_edges(
    "verification_loop",
    should_continue_verification,
    {
        "continue_verification": "verification_loop",
        "proceed_to_branch_mgmt": "manage_branches"
    }
)

# Integration test
async def test_full_implementation_cycle():
    """Test complete implementation + verification cycle."""
    state = {
        "jobs": [
            {"name": "job1", "task_file": "tasks/job1.md", "worktree_path": "worktrees/feat-job1"},
            {"name": "job2", "task_file": "tasks/job2.md", "worktree_path": "worktrees/feat-job2"}
        ],
        "pool_size": 2,
        "sprint_prd_path": "prd.md"
    }

    # Run implementation
    result1 = await parallel_implementation(state)
    state.update(result1)

    # Run verification
    result2 = await verification_loop(state)
    state.update(result2)

    # Check routing
    routing = should_continue_verification(state)

    assert routing in ["continue_verification", "proceed_to_branch_mgmt"]
```

## Success Criteria
- Decision function implemented
- Conditional edge configured
- Verification loop terminates correctly
- All terminal states handled (verified, failed)
- Mixed scenarios tested
- Integration test passing
- Loop doesn't hang indefinitely
- Routing logic validated

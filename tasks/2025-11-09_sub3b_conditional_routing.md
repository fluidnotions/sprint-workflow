# Sub-Task 3B: Gap Analysis Conditional Edge Logic

## Parent Job
Week 3: Gap Analysis & Feedback Loop

## Story Points
3

## Scope
Implement conditional routing logic for gap analysis feedback loop with max retry limits and user approval integration.

## Can Run in Parallel
YES - Parallel with 3A (independent decision logic)

## Todos
- [ ] Implement should_apply_gap_feedback() decision function
- [ ] Add retry_counts tracking to state schema
- [ ] Configure max retry limit (3 iterations)
- [ ] Add conditional edge to workflow graph
- [ ] Test conditional routing (approved vs apply_feedback vs max_retries)
- [ ] Write unit tests for decision function
- [ ] Test edge cases (no gaps, minor gaps, critical gaps, max retries)

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/validation.py (modify - add decision function)
- sprint-workflow/langgraph/state.py (modify - add retry tracking)
- sprint-workflow/langgraph/workflow.py (modify - add conditional edge)
- sprint-workflow/tests/langgraph/test_validation_nodes.py (modify - add routing tests)

## Dependencies
- Sub-task 1D (needs workflow skeleton)
- Sub-task 3A (uses gap_analysis_output for routing decisions)

## Blocks
- None (routing logic needed but doesn't block other sub-tasks)

## Implementation Notes
```python
def should_apply_gap_feedback(state: SprintWorkflowState) -> str:
    """Decision function for gap analysis feedback loop."""
    retry_count = state.get("gap_analysis_retry_count", 0)
    recommendations = state.get("gap_analysis_output", {})

    # Max retries reached
    if retry_count >= 3:
        return "max_retries_reached"

    # No critical issues found
    severity = recommendations.get("severity", "none")
    if severity == "none":
        return "approved"

    # Critical or minor issues - ask user
    # For now, auto-apply feedback (can add user prompt later)
    if severity in ["minor", "critical"]:
        return "apply_feedback"

    # Default: approved
    return "approved"

# In workflow.py
workflow.add_conditional_edges(
    "gap_analysis",
    should_apply_gap_feedback,
    {
        "apply_feedback": "update_planning_from_feedback",
        "approved": "generate_sprint_prd",
        "max_retries_reached": "generate_sprint_prd"
    }
)
```

## Success Criteria
- Decision function implemented
- Retry tracking in state schema
- Max retry limit enforced (3)
- Conditional edge configured in workflow
- All routing scenarios tested:
  - No gaps → approved
  - Minor gaps → apply_feedback
  - Critical gaps → apply_feedback
  - Max retries → max_retries_reached
- Unit tests passing
- Edge cases handled gracefully

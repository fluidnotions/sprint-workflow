# Sub-Task 3C: Feedback Application Node

## Parent Job
Week 3: Gap Analysis & Feedback Loop

## Story Points
3

## Scope
Apply gap analysis recommendations back into planning outputs and re-trigger planning nodes.

## Can Run in Parallel
NO - Depends on 3A (needs gap analysis recommendations)

## Todos
- [ ] Implement update_planning_from_feedback() node function
- [ ] Merge gap analysis recommendations into PM output
- [ ] Merge recommendations into UX output
- [ ] Merge recommendations into Engineering output
- [ ] Track feedback history in state
- [ ] Increment gap_analysis_retry_count
- [ ] Write unit tests for feedback application
- [ ] Test feedback loop iteration (simulated issues)

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/validation.py (modify - add feedback node)
- sprint-workflow/langgraph/state.py (modify - add feedback_history field)
- sprint-workflow/tests/langgraph/test_validation_nodes.py (modify - add feedback tests)

## Dependencies
- Sub-task 3A (needs gap analysis recommendations)
- Sub-task 3B (routing determines when to apply feedback)

## Blocks
- None (feedback loop is iterative)

## Implementation Notes
```python
async def update_planning_from_feedback(state: SprintWorkflowState) -> dict:
    """Apply gap analysis recommendations to planning outputs."""
    recommendations = state["gap_analysis_output"]["recommendations"]

    # Merge recommendations into planning outputs
    updated_pm = merge_recommendations(
        state["pm_output"],
        recommendations,
        aspect="product"
    )

    updated_ux = merge_recommendations(
        state["ux_output"],
        recommendations,
        aspect="ux"
    )

    updated_eng = merge_recommendations(
        state["engineering_output"],
        recommendations,
        aspect="engineering"
    )

    # Track feedback history
    feedback_history = state.get("feedback_history", [])
    feedback_history.append({
        "iteration": state.get("gap_analysis_retry_count", 0),
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat()
    })

    return {
        "pm_output": updated_pm,
        "ux_output": updated_ux,
        "engineering_output": updated_eng,
        "feedback_history": feedback_history,
        "gap_analysis_retry_count": state.get("gap_analysis_retry_count", 0) + 1,
        "phase": "feedback_applied"
    }

def merge_recommendations(output: dict, recommendations: list, aspect: str) -> dict:
    """Merge recommendations into planning output."""
    relevant_recs = [r for r in recommendations if r.get("aspect") == aspect]

    # Create merged output with recommendations applied
    merged = output.copy()

    for rec in relevant_recs:
        if rec["type"] == "add":
            merged = add_to_output(merged, rec)
        elif rec["type"] == "modify":
            merged = modify_output(merged, rec)
        elif rec["type"] == "remove":
            merged = remove_from_output(merged, rec)

    return merged
```

## Success Criteria
- Feedback application node implemented
- Recommendations merged into planning outputs
- feedback_history tracked in state
- Retry count incremented
- Unit tests passing
- Feedback loop tested with simulated issues
- Re-triggers planning nodes correctly

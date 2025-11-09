# Sub-Task 3D: User Approval Mechanism

## Parent Job
Week 3: Gap Analysis & Feedback Loop

## Story Points
2

## Scope
Implement user interaction callback for approving or customizing gap analysis feedback before application.

## Can Run in Parallel
YES - Parallel with 3C (can be integrated later)

## Todos
- [ ] Add user interaction callback for feedback approval
- [ ] Implement approval prompt with recommendations display
- [ ] Handle user response (yes/no/customize)
- [ ] Add approval decision to state
- [ ] Test feedback loop with user approval
- [ ] Test max retry escape condition with user override
- [ ] Document user approval interface

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/validation.py (modify - add approval callback)
- sprint-workflow/langgraph/state.py (modify - add approval_decision field)
- sprint-workflow/tests/langgraph/test_validation_nodes.py (modify - add approval tests)

## Dependencies
- Sub-task 3A (needs gap analysis output to display)

## Blocks
- None (optional enhancement to feedback loop)

## Implementation Notes
```python
async def request_user_approval(recommendations: dict) -> str:
    """Request user approval for applying gap analysis feedback."""
    # Display recommendations
    print("\n" + "="*60)
    print("GAP ANALYSIS RECOMMENDATIONS")
    print("="*60)

    severity = recommendations.get("severity", "none")
    print(f"\nSeverity: {severity.upper()}")

    print("\nRecommendations:")
    for i, rec in enumerate(recommendations.get("recommendations", []), 1):
        print(f"{i}. {rec['description']}")

    print("\nOptions:")
    print("  1. Apply all recommendations and re-run planning")
    print("  2. Approve as-is (skip feedback)")
    print("  3. Customize (select which to apply)")

    # Get user input
    choice = input("\nYour choice [1/2/3]: ").strip()

    if choice == "1":
        return "apply"
    elif choice == "2":
        return "approve"
    elif choice == "3":
        return "customize"
    else:
        print("Invalid choice, defaulting to approve")
        return "approve"

def should_apply_gap_feedback_with_approval(state: SprintWorkflowState) -> str:
    """Enhanced decision function with user approval."""
    retry_count = state.get("gap_analysis_retry_count", 0)
    recommendations = state.get("gap_analysis_output", {})

    # Max retries reached
    if retry_count >= 3:
        print("\n⚠️  Max retry limit reached (3 iterations)")
        return "max_retries_reached"

    # No issues found
    severity = recommendations.get("severity", "none")
    if severity == "none":
        print("\n✅ No gaps found in planning")
        return "approved"

    # Ask user for approval
    user_decision = asyncio.run(request_user_approval(recommendations))

    if user_decision == "apply":
        return "apply_feedback"
    elif user_decision == "customize":
        # Handle customization
        customized_recs = customize_recommendations(recommendations)
        state["gap_analysis_output"]["recommendations"] = customized_recs
        return "apply_feedback"
    else:
        return "approved"
```

## Success Criteria
- User approval callback implemented
- Recommendations displayed clearly
- User choices handled (apply/approve/customize)
- approval_decision tracked in state
- Integration with conditional routing working
- Tests with mocked user input passing
- Documentation for user interface complete

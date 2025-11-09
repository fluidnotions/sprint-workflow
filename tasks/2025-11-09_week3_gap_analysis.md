# Job: Gap Analysis & Feedback Loop

## Overview
Implement the gap analysis validation node with automatic feedback loops. Includes web search integration for best practices research, conditional routing logic, and user approval mechanism. Ensures architecture validation is guaranteed and iterative.

## Story Points
13

## Todos from Sprint
### Gap Analysis Node
- [ ] Create langgraph/nodes/validation.py module
- [ ] Extract gap analyzer prompt from agents/gap-analyzer.md
- [ ] Implement gap_analysis() node function
- [ ] Add web search integration for best practices research
- [ ] Create parse_gap_analysis() helper for recommendations
- [ ] Add gap_analysis output to state schema
- [ ] Write unit tests for gap analysis node

### Conditional Edge Logic
- [ ] Implement should_apply_gap_feedback() decision function
- [ ] Add retry_counts tracking to state schema
- [ ] Configure max retry limit (3 iterations)
- [ ] Add conditional edge to workflow graph
- [ ] Test conditional routing (approved vs apply_feedback vs max_retries)

### Feedback Application Node
- [ ] Implement update_planning_from_feedback() node function
- [ ] Merge gap analysis recommendations into PM output
- [ ] Merge recommendations into UX output
- [ ] Merge recommendations into Engineering output
- [ ] Track feedback history in state
- [ ] Write unit tests for feedback application

### User Approval Mechanism
- [ ] Add user interaction callback for feedback approval
- [ ] Implement approval prompt with recommendations display
- [ ] Handle user response (yes/no/customize)
- [ ] Add approval decision to state
- [ ] Test feedback loop with simulated issues
- [ ] Test max retry escape condition

## Implementation Plan
1. **Create validation.py module** - Set up validation nodes directory
2. **Extract gap analyzer prompt** - Read agents/gap-analyzer.md for prompt template
3. **Implement gap analysis node** - Use Anthropic API with web search integration
4. **Update state schema** - Add gap_analysis_output, retry_counts, feedback_history fields
5. **Implement conditional edge** - Create decision function for routing (approved/feedback/max_retries)
6. **Implement feedback application node** - Merge recommendations into planning outputs
7. **Add user approval callback** - Implement interactive approval mechanism
8. **Connect to workflow graph** - Add nodes and conditional edges
9. **Write tests** - Test gap analysis, feedback loop, max retries, user approval
10. **Integration test** - Test full planning + gap analysis cycle

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/validation.py (new - gap analysis and feedback nodes)
- sprint-workflow/langgraph/state.py (modify - add gap analysis fields, retry tracking)
- sprint-workflow/langgraph/workflow.py (modify - add conditional edges for feedback loop)
- sprint-workflow/agents/gap-analyzer.md (read - extract prompt)
- sprint-workflow/tests/langgraph/test_validation_nodes.py (new)

## Success Criteria
- All todos complete
- Gap analysis node implemented with web search
- Conditional edge logic for feedback routing
- Update planning node applies gap analysis recommendations
- Feedback loop tested with simulated issues
- User approval mechanism for applying feedback
- Max retry limit (3) prevents infinite loops
- Tests passing for all validation scenarios

## Dependencies
- Depends on: Job 2 (Planning Nodes) - requires PM, UX, Engineering outputs
- Required by: Job 4 (Job Creation) - validated planning feeds into PRD generation

## Technical Notes
### Gap Analysis Architecture
```python
async def gap_analysis(state: SprintWorkflowState) -> dict:
    """Analyze planning outputs for gaps and inconsistencies."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Combine planning outputs
    planning_doc = combine_planning_outputs(
        state["pm_output"],
        state["ux_output"],
        state["engineering_output"],
        state["synthesis_output"]
    )

    # Web search for best practices
    search_results = await web_search_best_practices(state["sprint_theme"])

    prompt = load_gap_analyzer_prompt()
    context = f"{planning_doc}\n\nBest Practices:\n{search_results}"

    response = await client.messages.create(
        model="claude-opus-4-20250514",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=4000
    )

    recommendations = parse_gap_analysis(response.content[0].text)

    return {
        "gap_analysis_output": recommendations,
        "phase": "gap_analysis_complete"
    }
```

### Conditional Routing Logic
```python
def should_apply_gap_feedback(state: SprintWorkflowState) -> str:
    """Decision function for gap analysis feedback loop."""
    retry_count = state.get("gap_analysis_retry_count", 0)
    recommendations = state.get("gap_analysis_output", {})

    # Max retries reached
    if retry_count >= 3:
        return "max_retries_reached"

    # No critical issues found
    if recommendations.get("severity") == "none":
        return "approved"

    # Ask user for approval
    user_decision = request_user_approval(recommendations)

    if user_decision == "apply":
        return "apply_feedback"
    else:
        return "approved"
```

### Feedback Application Strategy
- Merge recommendations into existing planning outputs
- Track which recommendations were applied
- Maintain feedback history for debugging
- Re-run planning nodes with updated context

### User Approval Mechanism
- Display gap analysis recommendations to user
- Options: "Apply feedback", "Approve as-is", "Customize"
- Interactive CLI or callback-based approval
- Store approval decision in state

### Web Search Integration
- Use WebFetch tool for best practices research
- Query patterns: "{technology} best practices", "{architecture} patterns"
- Cache results to avoid redundant searches
- Include search results in gap analysis context

### Testing Strategy
- Mock web search results for deterministic tests
- Simulate gap analysis scenarios: no issues, minor issues, critical issues
- Test feedback loop iteration (1, 2, 3 iterations)
- Test max retry escape condition
- Test user approval scenarios (apply, approve, customize)

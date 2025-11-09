# Sub-Task 2B: UX Designer Planning Node

## Parent Job
Week 2: Planning Nodes Implementation

## Story Points
3

## Scope
Convert UX Designer agent to deterministic LangGraph node with prompt extraction and response parsing.

## Can Run in Parallel
YES - Fully parallel with 2A, 2C (different nodes, different files)

## Todos
- [ ] Extract UX prompt from agents/ux-designer.md
- [ ] Implement ux_planning() node function in langgraph/nodes/planning.py
- [ ] Create parse_ux_response() helper for output parsing
- [ ] Add ux_output to state schema
- [ ] Implement load_ux_prompt() helper
- [ ] Write unit tests for UX node
- [ ] Test parallel execution with PM node (integration test)

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/planning.py (modify - add UX node)
- sprint-workflow/langgraph/state.py (modify - add ux_output field)
- sprint-workflow/tests/langgraph/test_planning_nodes.py (modify - add UX tests)
- sprint-workflow/agents/ux-designer.md (read)

## Dependencies
- Sub-task 1B (needs state schema)
- Sub-task 1D (needs workflow skeleton)
- Sub-task 1C (needs testing infrastructure)

## Blocks
- Sub-task 2D (synthesis needs UX output)

## Implementation Notes
```python
async def ux_planning(state: SprintWorkflowState) -> dict:
    """UX Designer planning node."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = load_ux_prompt()
    context = f"""
Sprint Theme: {state['sprint_theme']}
Project: {state['project_name']}
PM Output: {state.get('pm_output', 'Pending...')}
"""

    response = await client.messages.create(
        model="claude-opus-4-20250514",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=4000
    )

    parsed = parse_ux_response(response.content[0].text)

    return {
        "ux_output": parsed,
        "phase": "ux_planning_complete"
    }

def parse_ux_response(text: str) -> dict:
    """Parse UX agent response into structured format."""
    return {
        "user_flows": extract_user_flows(text),
        "ui_states": extract_ui_states(text),
        "component_specs": extract_component_specs(text)
    }
```

## Success Criteria
- UX node function implemented
- Prompt successfully extracted from agents/ux-designer.md
- Response parsing working
- Unit tests passing with mocked API
- ux_output in state schema
- Parallel execution with PM node tested
- Node integrates with workflow graph

# Sub-Task 2C: Senior Engineer Planning Node

## Parent Job
Week 2: Planning Nodes Implementation

## Story Points
3

## Scope
Convert Senior Engineer agent to deterministic LangGraph node with prompt extraction and response parsing.

## Can Run in Parallel
YES - Fully parallel with 2A, 2B (different nodes, different files)

## Todos
- [ ] Extract Engineering prompt from agents/senior-engineer.md
- [ ] Implement engineering_planning() node function in langgraph/nodes/planning.py
- [ ] Create parse_engineering_response() helper for output parsing
- [ ] Add engineering_output to state schema
- [ ] Implement load_engineering_prompt() helper
- [ ] Write unit tests for Engineering node
- [ ] Test parallel execution of all three planning nodes (PM+UX+Eng)

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/planning.py (modify - add Engineering node)
- sprint-workflow/langgraph/state.py (modify - add engineering_output field)
- sprint-workflow/tests/langgraph/test_planning_nodes.py (modify - add Engineering tests)
- sprint-workflow/agents/senior-engineer.md (read)

## Dependencies
- Sub-task 1B (needs state schema)
- Sub-task 1D (needs workflow skeleton)
- Sub-task 1C (needs testing infrastructure)

## Blocks
- Sub-task 2D (synthesis needs Engineering output)

## Implementation Notes
```python
async def engineering_planning(state: SprintWorkflowState) -> dict:
    """Senior Engineer planning node."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = load_engineering_prompt()
    context = f"""
Sprint Theme: {state['sprint_theme']}
Project: {state['project_name']}
PM Output: {state.get('pm_output', 'Pending...')}
UX Output: {state.get('ux_output', 'Pending...')}
"""

    response = await client.messages.create(
        model="claude-opus-4-20250514",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=4000
    )

    parsed = parse_engineering_response(response.content[0].text)

    return {
        "engineering_output": parsed,
        "phase": "engineering_planning_complete"
    }

def parse_engineering_response(text: str) -> dict:
    """Parse Engineering agent response into structured format."""
    return {
        "technical_architecture": extract_architecture(text),
        "risk_assessment": extract_risks(text),
        "dependencies": extract_dependencies(text)
    }
```

## Success Criteria
- Engineering node function implemented
- Prompt successfully extracted from agents/senior-engineer.md
- Response parsing working
- Unit tests passing with mocked API
- engineering_output in state schema
- Parallel execution with PM+UX nodes tested
- Node integrates with workflow graph

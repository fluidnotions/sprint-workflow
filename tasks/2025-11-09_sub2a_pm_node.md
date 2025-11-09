# Sub-Task 2A: Product Manager Planning Node

## Parent Job
Week 2: Planning Nodes Implementation

## Story Points
3

## Scope
Convert Product Manager agent to deterministic LangGraph node with prompt extraction and response parsing.

## Can Run in Parallel
YES - Fully parallel with 2B, 2C (different nodes, different files)

## Todos
- [ ] Create langgraph/nodes/planning.py module
- [ ] Extract PM prompt from agents/product-manager.md
- [ ] Implement pm_planning() node function
- [ ] Create parse_pm_response() helper for output parsing
- [ ] Add pm_output to state schema
- [ ] Implement load_pm_prompt() helper
- [ ] Write unit tests for PM node
- [ ] Test with mocked Anthropic API

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/__init__.py (new)
- sprint-workflow/langgraph/nodes/planning.py (new)
- sprint-workflow/langgraph/state.py (modify - add pm_output field)
- sprint-workflow/tests/langgraph/test_planning_nodes.py (new)
- sprint-workflow/agents/product-manager.md (read)

## Dependencies
- Sub-task 1B (needs state schema)
- Sub-task 1D (needs workflow skeleton)
- Sub-task 1C (needs testing infrastructure)

## Blocks
- Sub-task 2D (synthesis needs PM output)

## Implementation Notes
```python
async def pm_planning(state: SprintWorkflowState) -> dict:
    """Product Manager planning node."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = load_pm_prompt()
    context = f"""
Sprint Theme: {state['sprint_theme']}
Project: {state['project_name']}
"""

    response = await client.messages.create(
        model="claude-opus-4-20250514",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=4000
    )

    parsed = parse_pm_response(response.content[0].text)

    return {
        "pm_output": parsed,
        "phase": "pm_planning_complete"
    }

def load_pm_prompt() -> str:
    """Load PM prompt from agent markdown file."""
    with open('agents/product-manager.md', 'r') as f:
        content = f.read()
    # Strip frontmatter, return prompt body
    return extract_prompt_from_markdown(content)

def parse_pm_response(text: str) -> dict:
    """Parse PM agent response into structured format."""
    return {
        "user_stories": extract_user_stories(text),
        "acceptance_criteria": extract_acceptance_criteria(text),
        "business_value": extract_business_value(text)
    }
```

## Success Criteria
- PM node function implemented
- Prompt successfully extracted from agents/product-manager.md
- Response parsing working
- Unit tests passing with mocked API
- pm_output in state schema
- Node integrates with workflow graph

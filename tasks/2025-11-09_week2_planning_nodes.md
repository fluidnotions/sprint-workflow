# Job: Planning Nodes Implementation

## Overview
Convert the parallel planning agents (Product Manager, UX Designer, Senior Engineer) from agent-based orchestration to deterministic LangGraph nodes. Includes synthesis node to combine all three outputs into a unified plan.

## Story Points
13

## Todos from Sprint
### Product Manager Node
- [ ] Create langgraph/nodes/planning.py module
- [ ] Extract PM prompt from agents/product-manager.md
- [ ] Implement pm_planning() node function
- [ ] Create parse_pm_response() helper for output parsing
- [ ] Add PM output to state schema
- [ ] Write unit tests for PM node

### UX Designer Node
- [ ] Extract UX prompt from agents/ux-designer.md
- [ ] Implement ux_planning() node function
- [ ] Create parse_ux_response() helper for output parsing
- [ ] Add UX output to state schema
- [ ] Write unit tests for UX node
- [ ] Test parallel execution with PM node

### Senior Engineer Node
- [ ] Extract Engineering prompt from agents/senior-engineer.md
- [ ] Implement engineering_planning() node function
- [ ] Create parse_engineering_response() helper for output parsing
- [ ] Add Engineering output to state schema
- [ ] Write unit tests for Engineering node
- [ ] Test parallel execution of all three planning nodes

### Synthesis Node
- [ ] Implement synthesize_planning() node function
- [ ] Combine PM + UX + Engineering outputs into unified plan
- [ ] Generate intermediate planning document
- [ ] Add synthesis output to state schema
- [ ] Write unit tests for synthesis node
- [ ] Test end-to-end planning phase (PM+UX+Eng → synthesis)

## Implementation Plan
1. **Extract prompts** - Read agents/product-manager.md, agents/ux-designer.md, agents/senior-engineer.md
2. **Create planning.py module** - Set up nodes directory structure
3. **Implement PM node** - Convert PM agent to LangGraph node with Anthropic API
4. **Implement UX node** - Convert UX agent to LangGraph node
5. **Implement Engineering node** - Convert Engineering agent to LangGraph node
6. **Update state schema** - Add pm_output, ux_output, engineering_output, synthesis_output fields
7. **Implement synthesis node** - Combine all three outputs into unified planning document
8. **Write unit tests** - Test each node independently and parallel execution
9. **Integration test** - Test full planning phase end-to-end

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/__init__.py (new)
- sprint-workflow/langgraph/nodes/planning.py (new - PM, UX, Eng, Synthesis nodes)
- sprint-workflow/langgraph/state.py (modify - add planning output fields)
- sprint-workflow/langgraph/workflow.py (modify - connect planning nodes to graph)
- sprint-workflow/tests/langgraph/test_planning_nodes.py (new)
- sprint-workflow/agents/product-manager.md (read - extract prompt)
- sprint-workflow/agents/ux-designer.md (read - extract prompt)
- sprint-workflow/agents/senior-engineer.md (read - extract prompt)

## Success Criteria
- All todos complete
- PM planning node extracts prompts from agents/product-manager.md
- UX planning node extracts prompts from agents/ux-designer.md
- Engineering planning node extracts prompts from agents/senior-engineer.md
- Synthesis node combines all three outputs
- Planning phase testable in isolation
- Parallel execution of PM/UX/Engineering verified
- State schema updated with planning outputs
- Unit tests passing for all nodes

## Dependencies
- Depends on: Job 1 (Infrastructure) - requires state schema and workflow graph
- Required by: Job 3 (Gap Analysis) - gap analysis uses planning outputs

## Technical Notes
### Prompt Extraction Pattern
```python
# Read agent markdown file
with open('agents/product-manager.md', 'r') as f:
    content = f.read()

# Extract prompt section (everything after frontmatter)
prompt = extract_prompt_from_markdown(content)
```

### Node Implementation Pattern
```python
async def pm_planning(state: SprintWorkflowState) -> dict:
    """Product Manager planning node."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = load_pm_prompt()
    context = build_pm_context(state)

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
```

### Parallel Execution Strategy
- Use LangGraph's built-in parallel node execution
- PM, UX, Engineering nodes run concurrently
- Synthesis node waits for all three to complete
- State updates merged automatically

### Output Parsing
- Create structured parsers for each agent's markdown output
- Extract user stories, acceptance criteria, technical specs
- Validate required sections present
- Handle parsing errors gracefully

### Testing Strategy
- Mock Anthropic API for unit tests
- Test each node with sample inputs
- Verify parallel execution order
- Test synthesis combines outputs correctly

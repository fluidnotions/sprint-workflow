# Sub-Task 2D: Planning Synthesis Node

## Parent Job
Week 2: Planning Nodes Implementation

## Story Points
4

## Scope
Combine PM, UX, and Engineering outputs into unified planning document. This node waits for all three parallel nodes to complete.

## Can Run in Parallel
NO - Depends on 2A, 2B, 2C completing

## Todos
- [ ] Implement synthesize_planning() node function in langgraph/nodes/planning.py
- [ ] Combine PM + UX + Engineering outputs into unified plan
- [ ] Generate intermediate planning document
- [ ] Add synthesis_output to state schema
- [ ] Write unit tests for synthesis node
- [ ] Test end-to-end planning phase (PM+UX+Eng → synthesis)
- [ ] Validate synthesis includes all required sections

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/planning.py (modify - add synthesis node)
- sprint-workflow/langgraph/state.py (modify - add synthesis_output field)
- sprint-workflow/tests/langgraph/test_planning_nodes.py (modify - add synthesis tests)

## Dependencies
- Sub-task 2A (needs PM output)
- Sub-task 2B (needs UX output)
- Sub-task 2C (needs Engineering output)

## Blocks
- Sub-task 3A (gap analysis uses synthesis output)

## Implementation Notes
```python
async def synthesize_planning(state: SprintWorkflowState) -> dict:
    """Combine all planning outputs into unified document."""
    synthesis = {
        "overview": f"Sprint: {state['sprint_theme']}",
        "user_stories": state["pm_output"]["user_stories"],
        "acceptance_criteria": state["pm_output"]["acceptance_criteria"],
        "user_flows": state["ux_output"]["user_flows"],
        "ui_components": state["ux_output"]["component_specs"],
        "architecture": state["engineering_output"]["technical_architecture"],
        "risks": state["engineering_output"]["risk_assessment"],
        "dependencies": state["engineering_output"]["dependencies"]
    }

    # Generate planning document
    planning_doc = format_planning_document(synthesis)

    # Optionally write to file for reference
    # write_file(f"thoughts/planning_{state['sprint_theme']}.md", planning_doc)

    return {
        "synthesis_output": synthesis,
        "phase": "synthesis_complete"
    }

def format_planning_document(synthesis: dict) -> str:
    """Format synthesis into readable markdown document."""
    doc = f"""# Sprint Planning: {synthesis['overview']}

## User Stories
{format_user_stories(synthesis['user_stories'])}

## Acceptance Criteria
{format_criteria(synthesis['acceptance_criteria'])}

## User Flows
{format_flows(synthesis['user_flows'])}

## UI Components
{format_components(synthesis['ui_components'])}

## Technical Architecture
{format_architecture(synthesis['architecture'])}

## Risks
{format_risks(synthesis['risks'])}

## Dependencies
{format_dependencies(synthesis['dependencies'])}
"""
    return doc
```

## Success Criteria
- Synthesis node combines all three outputs
- Unified planning document generated
- synthesis_output in state schema
- End-to-end planning phase tested
- All required sections present in synthesis
- Unit tests passing
- Integration with gap analysis validated

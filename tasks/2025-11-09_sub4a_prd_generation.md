# Sub-Task 4A: PRD Generation Node

## Parent Job
Week 4: Job Creation & PRD Generation

## Story Points
3

## Scope
Generate Sprint PRD from validated planning outputs and extract todos from user stories.

## Can Run in Parallel
YES - Parallel with 4B (job creation), both read from same planning outputs

## Todos
- [ ] Create langgraph/nodes/artifacts.py module
- [ ] Implement generate_sprint_prd() node function
- [ ] Synthesize PM + UX + Engineering + Gap Analysis into PRD
- [ ] Write PRD to thoughts/sprint-plans/{project}/ directory
- [ ] Generate todos from PRD user stories
- [ ] Add sprint_prd_path and todos_path to state schema
- [ ] Write unit tests for PRD generation
- [ ] Test todo extraction from various PRD formats

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/artifacts.py (new)
- sprint-workflow/langgraph/state.py (modify - add PRD/todos paths)
- sprint-workflow/tests/langgraph/test_artifacts_nodes.py (new)

## Dependencies
- Sub-task 3A (needs validated planning via gap analysis)
- Sub-task 3C (if feedback applied, uses updated planning)

## Blocks
- Sub-task 4B (job creation reads PRD and todos)

## Implementation Notes
```python
async def generate_sprint_prd(state: SprintWorkflowState) -> dict:
    """Generate Sprint PRD from validated planning outputs."""
    prd_content = synthesize_prd(
        pm_output=state["pm_output"],
        ux_output=state["ux_output"],
        engineering_output=state["engineering_output"],
        gap_analysis=state.get("gap_analysis_output", {}),
        synthesis=state["synthesis_output"]
    )

    # Write PRD
    project = state["project_name"]
    timestamp = datetime.now().strftime("%Y-%m-%d")
    prd_dir = f"thoughts/sprint-plans/{project}"
    os.makedirs(prd_dir, exist_ok=True)

    prd_path = f"{prd_dir}/{timestamp}_prd_{state['sprint_theme']}.md"
    write_file(prd_path, prd_content)

    # Generate todos from user stories
    todos = extract_todos_from_prd(prd_content)
    todos_path = f"{timestamp}_{state['sprint_theme']}_todos.md"
    write_file(todos_path, todos)

    return {
        "sprint_prd_path": prd_path,
        "todos_path": todos_path,
        "phase": "prd_generated"
    }

def synthesize_prd(pm_output, ux_output, engineering_output, gap_analysis, synthesis) -> str:
    """Synthesize all planning into PRD format."""
    prd = f"""# Sprint PRD: {synthesis['overview']}

## User Stories
{format_user_stories(pm_output['user_stories'])}

## Acceptance Criteria
{format_acceptance_criteria(pm_output['acceptance_criteria'])}

## User Flows
{format_user_flows(ux_output['user_flows'])}

## UI Components
{format_ui_components(ux_output['component_specs'])}

## Technical Architecture
{format_architecture(engineering_output['technical_architecture'])}

## Dependencies
{format_dependencies(engineering_output['dependencies'])}

## Risks & Mitigations
{format_risks(engineering_output['risk_assessment'])}

## Gap Analysis Results
{format_gap_analysis(gap_analysis)}
"""
    return prd

def extract_todos_from_prd(prd_content: str) -> str:
    """Extract user stories as todo checklist."""
    # Parse user stories from PRD
    user_stories = parse_user_stories_from_prd(prd_content)

    todos = "# Sprint Todos\n\n"
    for story in user_stories:
        todos += f"- [ ] {story['title']}\n"
        for task in story.get('tasks', []):
            todos += f"  - [ ] {task}\n"

    return todos
```

## Success Criteria
- PRD generation node implemented
- PRD written to correct directory structure
- Todos extracted from user stories
- sprint_prd_path and todos_path in state
- Unit tests passing
- PRD format validated
- Integration with gap analysis results working

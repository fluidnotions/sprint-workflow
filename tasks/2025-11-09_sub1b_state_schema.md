# Sub-Task 1B: State Schema TypedDicts

## Parent Job
Week 1: Infrastructure & State Schema

## Story Points
3

## Scope
Define all TypedDict schemas for the LangGraph state machine. This creates the data structures that flow through the entire workflow.

## Can Run in Parallel
PARTIALLY - Can run parallel with 1A after initial setup, parallel with 1C completely

## Todos
- [ ] Create langgraph/state.py module
- [ ] Define SprintWorkflowState TypedDict with all fields
- [ ] Define JobSpec TypedDict for job specifications
- [ ] Define RepoInfo TypedDict for repository information
- [ ] Define ErrorRecord TypedDict for error tracking
- [ ] Add type hints and documentation for all state fields
- [ ] Create test_state.py for state schema validation

## Files to Create/Modify
- sprint-workflow/langgraph/__init__.py (new)
- sprint-workflow/langgraph/state.py (new)
- sprint-workflow/tests/langgraph/__init__.py (new)
- sprint-workflow/tests/langgraph/test_state.py (new)

## Dependencies
- Sub-task 1A (needs dependencies installed)

## Blocks
- Sub-task 1D (workflow needs state schema)
- All Week 2+ sub-tasks (all nodes use state)

## Implementation Notes
```python
# Key TypedDicts to define
class SprintWorkflowState(TypedDict):
    # Input
    sprint_theme: str
    project_name: str
    pool_size: int

    # Planning outputs
    pm_output: dict
    ux_output: dict
    engineering_output: dict
    synthesis_output: dict

    # Validation
    gap_analysis_output: dict
    gap_analysis_retry_count: int

    # Jobs & Execution
    jobs: List[JobSpec]
    sprint_prd_path: str
    todos_path: str

    # Progress tracking
    implementing_jobs: List[dict]
    verified_jobs: List[str]
    failed_jobs: List[str]

    # Git
    worktrees: List[dict]
    branch_status: List[dict]
    merge_status: List[dict]

    # Phase tracking
    phase: Literal["init", "planning", "gap_analysis", ...]
    errors: List[ErrorRecord]
```

## Success Criteria
- All TypedDicts defined with complete field documentation
- Type hints working in IDE
- Test validation passing for all schemas
- No circular import dependencies

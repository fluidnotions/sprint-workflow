# Job: Infrastructure & State Schema

## Overview
Establish the LangGraph foundation including dependencies, state schema, workflow skeleton, and testing infrastructure. This job creates the deterministic state machine framework that all other jobs will build upon.

## Story Points
8

## Todos from Sprint
### Setup & Dependencies
- [ ] Install LangGraph dependencies (langgraph, langchain-anthropic, langchain-core)
- [ ] Update requirements.txt with new dependencies
- [ ] Create installation script for LangGraph (scripts/install_langgraph.sh)
- [ ] Verify ANTHROPIC_API_KEY environment variable setup

### State Schema
- [ ] Create langgraph/state.py module
- [ ] Define SprintWorkflowState TypedDict with all fields
- [ ] Define JobSpec TypedDict for job specifications
- [ ] Define RepoInfo TypedDict for repository information
- [ ] Define ErrorRecord TypedDict for error tracking
- [ ] Add type hints and documentation for all state fields

### Workflow Graph Skeleton
- [ ] Create langgraph/workflow.py module
- [ ] Implement build_workflow() function returning StateGraph
- [ ] Add all node definitions (stubs initially)
- [ ] Define edges between nodes
- [ ] Add conditional edges for feedback loops
- [ ] Configure MemorySaver checkpointing

### Testing Infrastructure
- [ ] Create tests/langgraph/ directory
- [ ] Set up pytest configuration
- [ ] Create test_state.py for state schema tests
- [ ] Create test_workflow.py for workflow graph tests
- [ ] Implement basic workflow execution test with dummy state
- [ ] Add CI/CD configuration for tests

## Implementation Plan
1. **Install dependencies** - Add langgraph, langchain-anthropic, langchain-core to requirements.txt
2. **Create state.py** - Define all TypedDict schemas with comprehensive field documentation
3. **Create workflow.py** - Build skeleton StateGraph with stub nodes for all 11 phases
4. **Set up testing** - Create test directory structure and pytest configuration
5. **Write state tests** - Validate TypedDict schemas and field types
6. **Write workflow tests** - Test graph structure, edges, and checkpoint serialization
7. **Document architecture** - Add inline documentation explaining state transitions

## Files to Create/Modify
- sprint-workflow/requirements.txt (modify - add langgraph dependencies)
- sprint-workflow/scripts/install_langgraph.sh (new - dependency installation)
- sprint-workflow/langgraph/__init__.py (new)
- sprint-workflow/langgraph/state.py (new - state schema definitions)
- sprint-workflow/langgraph/workflow.py (new - workflow graph skeleton)
- sprint-workflow/tests/langgraph/__init__.py (new)
- sprint-workflow/tests/langgraph/test_state.py (new)
- sprint-workflow/tests/langgraph/test_workflow.py (new)
- sprint-workflow/tests/pytest.ini (new - pytest configuration)

## Success Criteria
- All todos complete
- State schema defined with TypedDict for SprintWorkflowState
- Workflow graph skeleton created with all nodes
- Checkpointing working with MemorySaver
- Unit test framework set up
- Skeleton workflow can execute end-to-end (even with stubs)
- Tests passing for state schema validation
- CI/CD configuration working

## Dependencies
- Depends on: None (foundation job)
- Required by: All other jobs (2-8)

## Technical Notes
### State Schema Design
- Use TypedDict for strong typing and IDE support
- Include phase tracking with Literal types for safety
- Track retry counts for feedback loops
- Separate concerns: SprintWorkflowState, JobSpec, RepoInfo, ErrorRecord

### Workflow Graph Architecture
```python
# Graph structure
init → planning (parallel: PM, UX, Eng) → synthesis →
gap_analysis → [feedback loop] → prd_generation →
job_creation → job_validation → [feedback loop] →
worktree_setup → implementation → verification →
[retry loop] → branch_mgmt → merging → complete
```

### Checkpointing Strategy
- Use MemorySaver for development/testing
- Design for future Redis/SQLite backend
- Checkpoint after each node execution
- Enable mid-workflow resumption

### Testing Approach
- Unit tests for state schema validation
- Integration tests for graph structure
- Mock node implementations for workflow tests
- Test checkpoint serialization/deserialization

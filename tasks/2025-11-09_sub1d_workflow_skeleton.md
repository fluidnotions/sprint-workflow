# Sub-Task 1D: Workflow Graph Skeleton

## Parent Job
Week 1: Infrastructure & State Schema

## Story Points
3

## Scope
Create the LangGraph workflow skeleton with all node stubs, edges, and conditional routing. This defines the state machine structure.

## Can Run in Parallel
NO - Depends on state schema (1B)

## Todos
- [ ] Create langgraph/workflow.py module
- [ ] Implement build_workflow() function returning StateGraph
- [ ] Add all node definitions (stubs initially - just return state)
- [ ] Define edges between nodes
- [ ] Add conditional edges for feedback loops
- [ ] Configure MemorySaver checkpointing
- [ ] Create test_workflow.py for graph structure tests
- [ ] Test workflow execution with dummy state

## Files to Create/Modify
- sprint-workflow/langgraph/workflow.py (new)
- sprint-workflow/tests/langgraph/test_workflow.py (new)

## Dependencies
- Sub-task 1B (needs state schema)
- Sub-task 1C (needs testing infrastructure)

## Blocks
- All Week 2+ implementation sub-tasks (nodes replace stubs)

## Implementation Notes
```python
def build_workflow() -> StateGraph:
    """Build the sprint workflow graph."""
    workflow = StateGraph(SprintWorkflowState)

    # Add all nodes (stubs for now)
    workflow.add_node("pm_planning", stub_node)
    workflow.add_node("ux_planning", stub_node)
    workflow.add_node("engineering_planning", stub_node)
    workflow.add_node("synthesize_planning", stub_node)
    workflow.add_node("gap_analysis", stub_node)
    workflow.add_node("update_planning_from_feedback", stub_node)
    workflow.add_node("generate_sprint_prd", stub_node)
    workflow.add_node("create_jobs", stub_node)
    workflow.add_node("validate_jobs", stub_node)
    workflow.add_node("setup_git_worktrees", stub_node)
    workflow.add_node("parallel_implementation", stub_node)
    workflow.add_node("verification_loop", stub_node)
    workflow.add_node("manage_branches", stub_node)
    workflow.add_node("push_and_merge", stub_node)

    # Define edges
    workflow.set_entry_point("pm_planning")

    # Parallel planning
    workflow.add_edge("pm_planning", "synthesize_planning")
    workflow.add_edge("ux_planning", "synthesize_planning")
    workflow.add_edge("engineering_planning", "synthesize_planning")

    # Gap analysis feedback loop
    workflow.add_edge("synthesize_planning", "gap_analysis")
    workflow.add_conditional_edges(
        "gap_analysis",
        should_apply_gap_feedback,
        {
            "apply_feedback": "update_planning_from_feedback",
            "approved": "generate_sprint_prd",
            "max_retries_reached": "generate_sprint_prd"
        }
    )
    workflow.add_edge("update_planning_from_feedback", "pm_planning")

    # Job creation
    workflow.add_edge("generate_sprint_prd", "create_jobs")
    workflow.add_edge("create_jobs", "validate_jobs")
    workflow.add_conditional_edges(
        "validate_jobs",
        should_apply_job_feedback,
        {
            "apply_feedback": "create_jobs",
            "approved": "setup_git_worktrees"
        }
    )

    # Implementation
    workflow.add_edge("setup_git_worktrees", "parallel_implementation")
    workflow.add_edge("parallel_implementation", "verification_loop")
    workflow.add_conditional_edges(
        "verification_loop",
        should_continue_verification,
        {
            "continue_verification": "verification_loop",
            "proceed_to_branch_mgmt": "manage_branches"
        }
    )

    # Merging
    workflow.add_edge("manage_branches", "push_and_merge")
    workflow.set_finish_point("push_and_merge")

    return workflow

def stub_node(state: SprintWorkflowState) -> dict:
    """Stub node that just returns empty updates."""
    return {}
```

## Success Criteria
- Workflow graph builds successfully
- All nodes defined (even as stubs)
- All edges and conditional edges configured
- Checkpointing working with MemorySaver
- Graph structure tests passing
- Can execute end-to-end with stubs
- Graph visualization generates correctly

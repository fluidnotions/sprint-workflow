"""Complete LangGraph workflow with all nodes integrated."""

from typing import Dict, Any
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from .state import SprintWorkflowState
from .nodes import (
    synthesize_planning_node,
    gap_analysis_node,
    update_planning_from_feedback_node,
    user_approval_node,
    generate_sprint_prd_node,
    create_jobs_node,
    validate_jobs_node,
    setup_git_worktrees_node,
    parallel_implementation_node,
    verification_loop_node,
    manage_branches_node,
    push_and_merge_node,
    generate_final_report_node,
)
from .routing import (
    should_apply_gap_feedback,
    should_apply_job_feedback,
    should_continue_verification,
)


def build_complete_workflow() -> StateGraph:
    """Build the complete sprint workflow with all nodes."""
    workflow = StateGraph(SprintWorkflowState)
    
    # All nodes
    workflow.add_node("synthesize_planning", synthesize_planning_node)
    workflow.add_node("gap_analysis", gap_analysis_node)
    workflow.add_node("update_planning_from_feedback", update_planning_from_feedback_node)
    workflow.add_node("user_approval", user_approval_node)
    workflow.add_node("generate_sprint_prd", generate_sprint_prd_node)
    workflow.add_node("create_jobs", create_jobs_node)
    workflow.add_node("validate_jobs", validate_jobs_node)
    workflow.add_node("setup_git_worktrees", setup_git_worktrees_node)
    workflow.add_node("parallel_implementation", parallel_implementation_node)
    workflow.add_node("verification_loop", verification_loop_node)
    workflow.add_node("manage_branches", manage_branches_node)
    workflow.add_node("push_and_merge", push_and_merge_node)
    workflow.add_node("generate_final_report", generate_final_report_node)
    
    # Edges
    workflow.add_edge(START, "synthesize_planning")
    workflow.add_edge("synthesize_planning", "gap_analysis")
    
    # Gap feedback loop
    workflow.add_conditional_edges(
        "gap_analysis",
        should_apply_gap_feedback,
        {
            "apply_feedback": "update_planning_from_feedback",
            "approved": "user_approval",
            "max_retries": "user_approval",
        }
    )
    workflow.add_edge("update_planning_from_feedback", "gap_analysis")
    
    # PRD & Jobs
    workflow.add_edge("user_approval", "generate_sprint_prd")
    workflow.add_edge("generate_sprint_prd", "create_jobs")
    workflow.add_edge("create_jobs", "validate_jobs")
    
    # Job validation loop
    workflow.add_conditional_edges(
        "validate_jobs",
        should_apply_job_feedback,
        {
            "apply_feedback": "create_jobs",
            "approved": "setup_git_worktrees",
            "max_retries": "setup_git_worktrees",
        }
    )
    
    # Implementation
    workflow.add_edge("setup_git_worktrees", "parallel_implementation")
    workflow.add_edge("parallel_implementation", "verification_loop")
    
    # Verification loop
    workflow.add_conditional_edges(
        "verification_loop",
        should_continue_verification,
        {
            "retry": "verification_loop",
            "continue": "manage_branches",
        }
    )
    
    # Finalization
    workflow.add_edge("manage_branches", "push_and_merge")
    workflow.add_edge("push_and_merge", "generate_final_report")
    workflow.add_edge("generate_final_report", END)
    
    return workflow


def compile_complete_workflow(checkpointer: bool = True):
    """Compile the complete workflow."""
    workflow = build_complete_workflow()
    
    if checkpointer:
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    else:
        return workflow.compile()

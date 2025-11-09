"""LangGraph workflow graph definition for sprint execution.

This module defines the complete state machine structure with all nodes,
edges, and conditional routing for the sprint workflow.
"""

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from .state import SprintWorkflowState


# ============================================================================
# STUB NODES (to be implemented in future sub-tasks)
# ============================================================================

def stub_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Stub node that returns state unchanged.

    This is a placeholder for nodes that will be implemented in future
    sub-tasks. It simply returns the state without modifications.
    """
    return {}


# ============================================================================
# CONDITIONAL EDGE FUNCTIONS
# ============================================================================

def should_apply_gap_feedback(state: SprintWorkflowState) -> Literal["apply_feedback", "approved", "max_retries"]:
    """Decide whether to apply gap analysis feedback or proceed.

    Args:
        state: Current workflow state

    Returns:
        - "apply_feedback": Gap analysis found issues, loop back to update planning
        - "approved": No issues found, proceed to PRD generation
        - "max_retries": Max retries reached, proceed anyway
    """
    gap_analysis = state.get("gap_analysis")

    # If no gap analysis run yet, proceed
    if not gap_analysis:
        return "approved"

    # Check retry count
    retry_count = state.get("retry_counts", {}).get("gap_analysis", 0)
    if retry_count >= 3:
        return "max_retries"

    # Check if issues found
    issues = gap_analysis.get("issues_found", [])
    if issues:
        return "apply_feedback"

    return "approved"


def should_apply_job_feedback(state: SprintWorkflowState) -> Literal["apply_feedback", "approved", "max_retries"]:
    """Decide whether to apply job validation feedback or proceed.

    Args:
        state: Current workflow state

    Returns:
        - "apply_feedback": Job validation found issues, loop back to job creation
        - "approved": No issues found, proceed to worktree setup
        - "max_retries": Max retries reached, proceed anyway
    """
    # Check retry count
    retry_count = state.get("retry_counts", {}).get("job_validation", 0)
    if retry_count >= 3:
        return "max_retries"

    # Check if jobs need revision
    # (Stub implementation - will be enhanced in Week 4)
    return "approved"


def should_continue_verification(state: SprintWorkflowState) -> Literal["retry", "continue"]:
    """Decide whether to continue verification loop or proceed to branch management.

    Args:
        state: Current workflow state

    Returns:
        - "retry": Jobs still implementing/verifying, loop back
        - "continue": All jobs verified or failed, proceed to branch management
    """
    jobs = state.get("jobs", [])

    # Check if any jobs are still implementing or verifying
    for job in jobs:
        status = job.get("status")
        if status in ["implementing", "verifying"]:
            return "retry"

    # All jobs reached terminal state (verified or failed)
    return "continue"


# ============================================================================
# WORKFLOW GRAPH BUILDER
# ============================================================================

def build_workflow() -> StateGraph:
    """Build the complete sprint workflow state machine.

    This function creates the LangGraph StateGraph with all nodes,
    edges, and conditional routing for the sprint execution workflow.

    The workflow consists of these phases:
    1. Planning (parallel PM/UX/Engineering)
    2. Gap Analysis (with feedback loop)
    3. PRD Generation
    4. Job Creation (with validation feedback loop)
    5. Worktree Setup
    6. Implementation (parallel execution)
    7. Verification (with retry loops)
    8. Branch Management
    9. Merging (PR creation and auto-merge)

    Returns:
        StateGraph configured with all workflow nodes and edges
    """
    workflow = StateGraph(SprintWorkflowState)

    # ========================================================================
    # PLANNING PHASE NODES
    # ========================================================================
    workflow.add_node("pm_planning", stub_node)
    workflow.add_node("ux_planning", stub_node)
    workflow.add_node("engineering_planning", stub_node)
    workflow.add_node("synthesize_planning", stub_node)

    # ========================================================================
    # GAP ANALYSIS NODES
    # ========================================================================
    workflow.add_node("gap_analysis", stub_node)
    workflow.add_node("update_planning_from_feedback", stub_node)

    # ========================================================================
    # PRD & JOB CREATION NODES
    # ========================================================================
    workflow.add_node("generate_sprint_prd", stub_node)
    workflow.add_node("create_jobs", stub_node)
    workflow.add_node("validate_jobs", stub_node)
    workflow.add_node("update_jobs_from_feedback", stub_node)

    # ========================================================================
    # WORKTREE & IMPLEMENTATION NODES
    # ========================================================================
    workflow.add_node("setup_git_worktrees", stub_node)
    workflow.add_node("parallel_implementation", stub_node)
    workflow.add_node("verification_loop", stub_node)

    # ========================================================================
    # BRANCH MANAGEMENT & MERGING NODES
    # ========================================================================
    workflow.add_node("manage_branches", stub_node)
    workflow.add_node("push_and_merge", stub_node)
    workflow.add_node("generate_final_report", stub_node)

    # ========================================================================
    # DEFINE WORKFLOW EDGES
    # ========================================================================

    # Entry point: Start with parallel planning
    workflow.add_edge(START, "pm_planning")
    workflow.add_edge(START, "ux_planning")
    workflow.add_edge(START, "engineering_planning")

    # Parallel planning converges to synthesis
    workflow.add_edge("pm_planning", "synthesize_planning")
    workflow.add_edge("ux_planning", "synthesize_planning")
    workflow.add_edge("engineering_planning", "synthesize_planning")

    # Synthesis flows to gap analysis
    workflow.add_edge("synthesize_planning", "gap_analysis")

    # Gap analysis conditional: feedback loop or proceed
    workflow.add_conditional_edges(
        "gap_analysis",
        should_apply_gap_feedback,
        {
            "apply_feedback": "update_planning_from_feedback",
            "approved": "generate_sprint_prd",
            "max_retries": "generate_sprint_prd",
        }
    )

    # Feedback loop: update planning and re-run all planning nodes
    workflow.add_edge("update_planning_from_feedback", "pm_planning")

    # PRD generation flows to job creation
    workflow.add_edge("generate_sprint_prd", "create_jobs")

    # Job creation flows to validation
    workflow.add_edge("create_jobs", "validate_jobs")

    # Job validation conditional: feedback loop or proceed
    workflow.add_conditional_edges(
        "validate_jobs",
        should_apply_job_feedback,
        {
            "apply_feedback": "update_jobs_from_feedback",
            "approved": "setup_git_worktrees",
            "max_retries": "setup_git_worktrees",
        }
    )

    # Job feedback loop: update jobs and re-validate
    workflow.add_edge("update_jobs_from_feedback", "validate_jobs")

    # Worktree setup flows to implementation
    workflow.add_edge("setup_git_worktrees", "parallel_implementation")

    # Implementation flows to verification
    workflow.add_edge("parallel_implementation", "verification_loop")

    # Verification conditional: retry loop or proceed
    workflow.add_conditional_edges(
        "verification_loop",
        should_continue_verification,
        {
            "retry": "verification_loop",
            "continue": "manage_branches",
        }
    )

    # Branch management flows to merging
    workflow.add_edge("manage_branches", "push_and_merge")

    # Merging flows to final report
    workflow.add_edge("push_and_merge", "generate_final_report")

    # Final report is the end
    workflow.add_edge("generate_final_report", END)

    return workflow


def compile_workflow(checkpointer: bool = True) -> Any:
    """Compile the workflow graph with optional checkpointing.

    Args:
        checkpointer: If True, use MemorySaver for checkpoint support

    Returns:
        Compiled workflow app ready for invocation
    """
    workflow = build_workflow()

    if checkpointer:
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    else:
        return workflow.compile()


def get_workflow_visualization() -> str:
    """Generate a text representation of the workflow graph.

    Returns:
        String describing the workflow structure
    """
    return """
    Sprint Workflow Graph Structure:

    START → pm_planning ─┐
         → ux_planning ───┼─→ synthesize_planning → gap_analysis
         → engineering_planning ┘                         │
                                                           ├─→ (approved) → generate_sprint_prd
                                                           │
                                                           └─→ (feedback) → update_planning_from_feedback
                                                                              │
                                                                              └─→ Loop back to pm_planning

    generate_sprint_prd → create_jobs → validate_jobs
                                            │
                                            ├─→ (approved) → setup_git_worktrees
                                            │
                                            └─→ (feedback) → update_jobs_from_feedback
                                                               │
                                                               └─→ Loop back to validate_jobs

    setup_git_worktrees → parallel_implementation → verification_loop
                                                         │
                                                         ├─→ (retry) → Loop back to verification_loop
                                                         │
                                                         └─→ (continue) → manage_branches

    manage_branches → push_and_merge → generate_final_report → END

    Key Features:
    - Parallel planning (PM, UX, Engineering run simultaneously)
    - Two feedback loops (gap analysis, job validation)
    - One retry loop (verification)
    - Checkpointing enabled for resumability
    """

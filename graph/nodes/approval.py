"""User approval and interaction nodes."""

from typing import Dict, Any
import json

from ..state import SprintWorkflowState


def user_approval_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Request user approval for sprint plan (stub implementation).
    
    In a full implementation, this would:
    1. Display synthesized plan summary to user
    2. Wait for user input (approve/reject/modify)
    3. Store user decision in state
    
    For now, this is a passthrough node that auto-approves.
    Future enhancement: integrate with CLI or web interface.
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict with user_approved flag
    """
    synthesized_plan = state.get("synthesized_plan", {})
    gap_analysis = state.get("gap_analysis", {})
    
    # Generate summary for user (would be displayed in UI)
    overview = synthesized_plan.get("overview", {})
    execution_plan = synthesized_plan.get("execution_plan", {})
    
    summary = {
        "total_user_stories": overview.get("total_user_stories", 0),
        "total_components": overview.get("total_components", 0),
        "total_story_points": execution_plan.get("total_estimated_points", 0),
        "critical_risks": gap_analysis.get("overall_assessment", {}).get("critical_blockers", 0),
        "readiness_score": gap_analysis.get("overall_assessment", {}).get("readiness_score", 0.0),
    }
    
    # Auto-approve for now (future: prompt user)
    user_decision = "approved"
    
    # Store approval metadata
    approval_info = {
        "decision": user_decision,
        "timestamp": "auto",  # Future: actual timestamp
        "summary_shown": summary,
        "feedback": None,  # Future: user comments
    }
    
    return {
        "user_approved": user_decision == "approved",
        "approval_info": approval_info,
        "status_messages": [
            f"Plan summary: {summary['total_user_stories']} stories, "
            f"{summary['total_story_points']} points - Auto-approved"
        ]
    }

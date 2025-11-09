"""Feedback application nodes for iterative improvement."""

from typing import Dict, Any

from ..state import SprintWorkflowState


def update_planning_from_feedback_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Apply gap analysis feedback to update planning outputs.
    
    Takes issues from gap analysis and incorporates them back into
    the synthesized plan without re-running PM/UX/Engineering nodes.
    
    Strategy:
    1. Extract high-severity issues from gap analysis
    2. Add missing user stories for critical gaps
    3. Update risk matrix with newfound risks
    4. Enhance architecture components based on feedback
    5. Update execution plan to account for new work
    
    Args:
        state: Current workflow state with gap_analysis and synthesized_plan
        
    Returns:
        Dict with updated synthesized_plan incorporating feedback
    """
    gap_analysis = state.get("gap_analysis", {})
    synthesized_plan = state.get("synthesized_plan", {})
    
    if not gap_analysis or not synthesized_plan:
        return {"status_messages": ["No feedback to apply - skipping"]}
    
    issues = gap_analysis.get("issues_found", [])
    
    # Filter for actionable issues (critical and high severity)
    actionable_issues = [
        issue for issue in issues
        if issue.get("severity") in ["critical", "high"]
    ]
    
    if not actionable_issues:
        return {"status_messages": ["No critical/high issues to address"]}
    
    # Create updated plan
    updated_plan = synthesized_plan.copy()
    
    # 1. Add missing user stories for gaps
    existing_stories = updated_plan.get("integrated_stories", [])
    new_stories = []
    
    for issue in actionable_issues:
        if issue.get("category") in ["technical", "ux"]:
            # Create a new user story for this gap
            story_id = f"US-GAP-{len(existing_stories) + len(new_stories) + 1}"
            new_story = {
                "id": story_id,
                "title": f"Address: {issue.get('description', 'Gap')}",
                "acceptance_criteria": [issue.get("recommendation", "Fix identified gap")],
                "business_value": "high" if issue.get("severity") == "critical" else "medium",
                "story_points": _estimate_story_points(issue.get("estimated_effort", "")),
                "source": "gap_analysis",
                "ui_components": [],
                "user_flows": [],
            }
            new_stories.append(new_story)
    
    # 2. Update risk matrix
    risk_matrix = updated_plan.get("risk_matrix", {})
    existing_risks = risk_matrix.get("technical_risks", [])
    
    new_risks = []
    for issue in actionable_issues:
        if issue.get("category") in ["security", "scalability", "operational"]:
            new_risk = {
                "description": issue.get("description"),
                "severity": issue.get("severity"),
                "mitigation": issue.get("recommendation"),
                "impact": issue.get("impact"),
                "source": "gap_analysis"
            }
            new_risks.append(new_risk)
    
    # 3. Update execution plan with additional work
    execution_plan = updated_plan.get("execution_plan", {})
    phase_1 = execution_plan.get("phase_1_foundation", {})
    
    # Add gap-derived foundation work
    foundation_items = phase_1.get("items", [])
    for issue in actionable_issues:
        if issue.get("category") in ["technical", "security", "operational"]:
            foundation_items.append({
                "type": "gap_mitigation",
                "description": issue.get("description"),
                "action": issue.get("recommendation"),
                "severity": issue.get("severity")
            })
    
    # Recalculate story points
    added_points = sum(story.get("story_points", 0) for story in new_stories)
    total_points = execution_plan.get("total_estimated_points", 0) + added_points
    
    # Assemble updated plan
    updated_plan["integrated_stories"] = existing_stories + new_stories
    updated_plan["risk_matrix"]["technical_risks"] = existing_risks + new_risks
    updated_plan["execution_plan"]["phase_1_foundation"]["items"] = foundation_items[:5]  # Top 5
    updated_plan["execution_plan"]["total_estimated_points"] = total_points
    
    # Add feedback metadata
    updated_plan["_feedback_applied"] = {
        "issues_addressed": len(actionable_issues),
        "stories_added": len(new_stories),
        "risks_added": len(new_risks),
        "points_added": added_points,
    }
    
    return {
        "synthesized_plan": updated_plan,
        "status_messages": [
            f"Feedback applied: {len(new_stories)} stories added, "
            f"{len(new_risks)} risks added, {added_points} story points added"
        ]
    }


def _estimate_story_points(effort_str: str) -> int:
    """Estimate story points from effort string.
    
    Args:
        effort_str: String like "3 story points" or "2 days"
        
    Returns:
        Story point estimate
    """
    effort_lower = effort_str.lower()
    
    # Try to extract number
    import re
    numbers = re.findall(r'\d+', effort_lower)
    
    if numbers and "story point" in effort_lower:
        return int(numbers[0])
    elif numbers and "day" in effort_lower:
        # Rough conversion: 1 day = 2 story points
        return int(numbers[0]) * 2
    elif numbers and "hour" in effort_lower:
        # Rough conversion: 4 hours = 1 story point
        return max(1, int(numbers[0]) // 4)
    else:
        # Default to medium complexity
        return 3

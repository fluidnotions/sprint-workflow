"""Synthesis node for combining planning outputs."""

from typing import Dict, Any

from ..state import SprintWorkflowState


def synthesize_planning_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Synthesize planning outputs from PM, UX, and Engineering nodes.
    
    Takes the outputs from the three parallel planning nodes and creates
    a unified, coherent planning document that integrates:
    - User stories from PM with UI components from UX
    - Technical architecture from Engineering with user flows from UX
    - Risks from Engineering with success metrics from PM
    - A comprehensive execution plan
    
    Args:
        state: Current workflow state with pm_output, ux_output, engineering_output
        
    Returns:
        Dict with synthesized_plan containing unified planning document
    """
    pm_output = state.get("pm_output", {})
    ux_output = state.get("ux_output", {})
    engineering_output = state.get("engineering_output", {})
    
    # Extract key elements from each planning output
    user_stories = pm_output.get("user_stories", [])
    priorities = pm_output.get("priorities", [])
    success_metrics = pm_output.get("success_metrics", [])
    
    user_flows = ux_output.get("user_flows", [])
    ui_components = ux_output.get("ui_components", [])
    accessibility = ux_output.get("accessibility", {})
    
    architecture = engineering_output.get("architecture", {})
    technical_approach = engineering_output.get("technical_approach", {})
    risks = engineering_output.get("risks", [])
    performance = engineering_output.get("performance_considerations", {})
    
    # Build integrated plan
    synthesized_plan = {
        "overview": {
            "total_user_stories": len(user_stories),
            "total_components": len(ui_components),
            "total_risks": len(risks),
            "architecture_components": len(architecture.get("components", [])),
        },
        
        "integrated_stories": _integrate_stories_with_ux(
            user_stories, ui_components, user_flows
        ),
        
        "implementation_roadmap": {
            "priorities": priorities,
            "technical_stack": technical_approach,
            "architecture_overview": architecture,
        },
        
        "risk_matrix": {
            "technical_risks": risks,
            "accessibility_requirements": accessibility,
            "performance_targets": performance,
        },
        
        "success_criteria": {
            "business_metrics": success_metrics,
            "technical_requirements": {
                "accessibility_level": accessibility.get("wcag_level", "AA"),
                "scalability": performance.get("scalability", "Not specified"),
            },
        },
        
        "execution_plan": _create_execution_plan(
            user_stories, risks, architecture.get("components", [])
        ),
        
        "_meta": {
            "node": "synthesize_planning",
            "inputs_processed": {
                "pm": bool(pm_output),
                "ux": bool(ux_output),
                "engineering": bool(engineering_output),
            }
        }
    }
    
    return {
        "synthesized_plan": synthesized_plan,
        "phase": "gap_analysis",  # Move to next phase
        "status_messages": [
            f"Planning synthesis complete: {len(user_stories)} stories, "
            f"{len(ui_components)} components, {len(risks)} risks identified"
        ]
    }


def _integrate_stories_with_ux(user_stories, ui_components, user_flows):
    """Integrate user stories with UX components and flows."""
    integrated = []
    
    for story in user_stories:
        story_id = story.get("id", "")
        integrated_story = {
            **story,
            "ui_components": [],
            "user_flows": [],
        }
        
        # Match components that might relate to this story
        story_title_lower = story.get("title", "").lower()
        for component in ui_components:
            component_name = component.get("name", "").lower()
            # Simple matching - could be more sophisticated
            if any(word in component_name for word in story_title_lower.split() if len(word) > 3):
                integrated_story["ui_components"].append(component["name"])
        
        # Match flows that might relate to this story
        for flow in user_flows:
            flow_name = flow.get("name", "").lower()
            if any(word in flow_name for word in story_title_lower.split() if len(word) > 3):
                integrated_story["user_flows"].append(flow["name"])
        
        integrated.append(integrated_story)
    
    return integrated


def _create_execution_plan(user_stories, risks, components):
    """Create phased execution plan."""
    # Calculate total story points
    total_points = sum(story.get("story_points", 0) for story in user_stories)
    
    # Categorize by business value and complexity
    high_value_stories = [s for s in user_stories if s.get("business_value") == "high"]
    
    # Identify foundation work (high-risk items, infrastructure components)
    foundation_work = []
    for risk in risks:
        if risk.get("severity") in ["high", "critical"]:
            foundation_work.append({
                "type": "risk_mitigation",
                "description": risk.get("description"),
                "action": risk.get("mitigation")
            })
    
    for component in components:
        if component.get("type") in ["database", "cache", "infrastructure"]:
            foundation_work.append({
                "type": "infrastructure",
                "description": f"Set up {component.get('name')}",
                "technology": component.get("technology")
            })
    
    return {
        "phase_1_foundation": {
            "story_points": int(total_points * 0.3),
            "focus": "Infrastructure and high-risk mitigation",
            "items": foundation_work[:3]  # Top 3 foundation items
        },
        "phase_2_core": {
            "story_points": int(total_points * 0.5),
            "focus": "High-value user stories",
            "stories": [s.get("id") for s in high_value_stories]
        },
        "phase_3_polish": {
            "story_points": int(total_points * 0.2),
            "focus": "Remaining features, testing, refinement",
            "activities": ["Complete remaining stories", "Integration testing", "Performance optimization"]
        },
        "total_estimated_points": total_points,
    }

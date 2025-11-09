"""Tests for synthesis planning node."""

import pytest

from graph.nodes.synthesis import (
    synthesize_planning_node,
    _integrate_stories_with_ux,
    _create_execution_plan
)


class TestSynthesisPlanningNode:
    """Tests for synthesis planning node."""

    def test_synthesis_combines_all_outputs(
        self, 
        mock_pm_planning_output,
        mock_ux_planning_output,
        mock_engineering_output
    ):
        """Test that synthesis combines PM, UX, and Engineering outputs."""
        state = {
            "pm_output": mock_pm_planning_output,
            "ux_output": mock_ux_planning_output,
            "engineering_output": mock_engineering_output,
        }
        
        result = synthesize_planning_node(state)
        
        assert "synthesized_plan" in result
        assert "status_messages" in result
        assert "phase" in result
        assert result["phase"] == "gap_analysis"
        
        plan = result["synthesized_plan"]
        assert "overview" in plan
        assert "integrated_stories" in plan
        assert "implementation_roadmap" in plan
        assert "risk_matrix" in plan
        assert "success_criteria" in plan
        assert "execution_plan" in plan
        
        # Check metadata
        assert plan["_meta"]["inputs_processed"]["pm"] is True
        assert plan["_meta"]["inputs_processed"]["ux"] is True
        assert plan["_meta"]["inputs_processed"]["engineering"] is True

    def test_synthesis_handles_missing_outputs(self):
        """Test synthesis with some missing outputs."""
        state = {
            "pm_output": {"user_stories": [], "priorities": []},
            "ux_output": {},  # Empty
            "engineering_output": None,  # Missing
        }
        
        result = synthesize_planning_node(state)
        
        assert "synthesized_plan" in result
        plan = result["synthesized_plan"]
        
        # Should still generate valid structure
        assert "overview" in plan
        assert plan["overview"]["total_user_stories"] == 0
        assert plan["_meta"]["inputs_processed"]["pm"] is True
        assert plan["_meta"]["inputs_processed"]["ux"] is False
        assert plan["_meta"]["inputs_processed"]["engineering"] is False

    def test_integrate_stories_with_ux(self):
        """Test integration of user stories with UX elements."""
        user_stories = [
            {
                "id": "US-1",
                "title": "Dashboard view for users",
                "story_points": 5
            }
        ]
        ui_components = [
            {"name": "Dashboard", "type": "component"},
            {"name": "UserProfile", "type": "component"}
        ]
        user_flows = [
            {"name": "Dashboard Navigation"}
        ]
        
        integrated = _integrate_stories_with_ux(
            user_stories, ui_components, user_flows
        )
        
        assert len(integrated) == 1
        assert "ui_components" in integrated[0]
        assert "user_flows" in integrated[0]
        # Should match "Dashboard" based on title matching
        assert "Dashboard" in integrated[0]["ui_components"]

    def test_create_execution_plan(self):
        """Test execution plan creation."""
        user_stories = [
            {"id": "US-1", "story_points": 5, "business_value": "high"},
            {"id": "US-2", "story_points": 3, "business_value": "medium"},
            {"id": "US-3", "story_points": 8, "business_value": "high"},
        ]
        risks = [
            {"description": "Database risk", "severity": "high", "mitigation": "Add caching"},
            {"description": "API risk", "severity": "low", "mitigation": "Rate limiting"}
        ]
        components = [
            {"name": "Database", "type": "database", "technology": "PostgreSQL"},
            {"name": "Cache", "type": "cache", "technology": "Redis"}
        ]
        
        plan = _create_execution_plan(user_stories, risks, components)
        
        assert "phase_1_foundation" in plan
        assert "phase_2_core" in plan
        assert "phase_3_polish" in plan
        assert "total_estimated_points" in plan
        
        assert plan["total_estimated_points"] == 16
        assert "US-1" in plan["phase_2_core"]["stories"]
        assert "US-3" in plan["phase_2_core"]["stories"]

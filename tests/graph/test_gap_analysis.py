"""Tests for gap analysis node."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from graph.nodes.gap_analysis import gap_analysis_node


class TestGapAnalysisNode:
    """Tests for Gap Analysis node."""

    @pytest.mark.asyncio
    async def test_gap_analysis_identifies_issues(self, sample_sprint_state):
        """Test that gap analysis identifies issues."""
        sample_sprint_state["synthesized_plan"] = {
            "integrated_stories": [],
            "implementation_roadmap": {},
            "risk_matrix": {}
        }
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = '''```json
{
  "issues_found": [
    {
      "category": "security",
      "severity": "critical",
      "description": "Missing authentication middleware",
      "impact": "Unauthorized access possible",
      "recommendation": "Add JWT authentication",
      "estimated_effort": "3 story points"
    },
    {
      "category": "scalability",
      "severity": "high",
      "description": "No caching strategy defined",
      "impact": "Poor performance under load",
      "recommendation": "Implement Redis caching",
      "estimated_effort": "5 story points"
    }
  ],
  "strengths": [
    "Comprehensive user stories",
    "Good accessibility planning"
  ],
  "overall_assessment": {
    "readiness_score": 0.6,
    "critical_blockers": 1,
    "high_priority_items": 1,
    "recommendation": "revise"
  }
}
```'''
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 500
        mock_response.usage.output_tokens = 300

        with patch('graph.nodes.gap_analysis.AsyncAnthropic') as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.return_value = mock_client

            result = await gap_analysis_node(sample_sprint_state)

            assert "gap_analysis" in result
            assert "retry_counts" in result
            assert "status_messages" in result

            gap_analysis = result["gap_analysis"]
            assert "issues_found" in gap_analysis
            assert "strengths" in gap_analysis
            assert "overall_assessment" in gap_analysis
            assert "_meta" in gap_analysis

            assert len(gap_analysis["issues_found"]) == 2
            assert gap_analysis["issues_found"][0]["severity"] == "critical"
            assert gap_analysis["overall_assessment"]["critical_blockers"] == 1

            # Verify retry count incremented
            assert result["retry_counts"]["gap_analysis"] == 1

    @pytest.mark.asyncio
    async def test_gap_analysis_approves_good_plan(self, sample_sprint_state):
        """Test gap analysis approving a good plan."""
        sample_sprint_state["synthesized_plan"] = {
            "integrated_stories": [{"id": "US-1"}],
            "implementation_roadmap": {"technical_stack": {}},
            "risk_matrix": {"technical_risks": []}
        }
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = '''```json
{
  "issues_found": [],
  "strengths": [
    "Comprehensive architecture",
    "Good risk mitigation",
    "Strong testing strategy"
  ],
  "overall_assessment": {
    "readiness_score": 0.95,
    "critical_blockers": 0,
    "high_priority_items": 0,
    "recommendation": "approve"
  }
}
```'''
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 400
        mock_response.usage.output_tokens = 200

        with patch('graph.nodes.gap_analysis.AsyncAnthropic') as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.return_value = mock_client

            result = await gap_analysis_node(sample_sprint_state)

            gap_analysis = result["gap_analysis"]
            assert len(gap_analysis["issues_found"]) == 0
            assert gap_analysis["overall_assessment"]["recommendation"] == "approve"

    @pytest.mark.asyncio
    async def test_gap_analysis_fallback(self, sample_sprint_state):
        """Test fallback when JSON parsing fails."""
        sample_sprint_state["synthesized_plan"] = {}
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Invalid JSON response"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50

        with patch('graph.nodes.gap_analysis.AsyncAnthropic') as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.return_value = mock_client

            result = await gap_analysis_node(sample_sprint_state)

            gap_analysis = result["gap_analysis"]
            assert len(gap_analysis["issues_found"]) == 0
            assert gap_analysis["overall_assessment"]["recommendation"] == "approve"
            assert gap_analysis["overall_assessment"]["readiness_score"] == 0.8

    @pytest.mark.asyncio
    async def test_gap_analysis_tracks_retry_count(self, sample_sprint_state):
        """Test that retry count is properly tracked."""
        sample_sprint_state["synthesized_plan"] = {}
        sample_sprint_state["retry_counts"] = {"gap_analysis": 2}
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = '{"issues_found": [], "strengths": [], "overall_assessment": {"readiness_score": 0.8, "critical_blockers": 0, "high_priority_items": 0, "recommendation": "approve"}}'
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50

        with patch('graph.nodes.gap_analysis.AsyncAnthropic') as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.return_value = mock_client

            result = await gap_analysis_node(sample_sprint_state)

            # Should increment from 2 to 3
            assert result["retry_counts"]["gap_analysis"] == 3

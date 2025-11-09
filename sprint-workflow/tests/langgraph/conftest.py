"""Conftest for langgraph-specific tests.

Provides fixtures specific to testing LangGraph workflow nodes.
"""

import pytest
from typing import Dict, Any
from unittest.mock import Mock, AsyncMock


# ============================================================================
# NODE-SPECIFIC FIXTURES
# ============================================================================

@pytest.fixture
def mock_pm_planning_output() -> Dict[str, Any]:
    """Mock output from PM planning node."""
    return {
        "user_stories": [
            {
                "id": "US-1",
                "title": "As a user, I want to track sprint progress",
                "acceptance_criteria": [
                    "Sprint status visible in dashboard",
                    "Real-time updates",
                    "Historical data available"
                ],
                "business_value": "high",
                "story_points": 8
            },
            {
                "id": "US-2",
                "title": "As a developer, I want automated verification",
                "acceptance_criteria": [
                    "Tests run automatically",
                    "Feedback provided within 5 minutes",
                    "Retry logic for transient failures"
                ],
                "business_value": "medium",
                "story_points": 5
            }
        ],
        "priorities": ["US-1", "US-2"],
        "success_metrics": [
            "90%+ sprint completion rate",
            "70% reduction in debugging time"
        ]
    }


@pytest.fixture
def mock_ux_planning_output() -> Dict[str, Any]:
    """Mock output from UX planning node."""
    return {
        "user_flows": [
            {
                "name": "Sprint Creation Flow",
                "steps": [
                    "User provides sprint theme",
                    "System runs planning agents",
                    "User reviews Sprint PRD",
                    "User approves and starts sprint"
                ]
            }
        ],
        "ui_components": [
            {
                "name": "SprintDashboard",
                "type": "component",
                "props": ["sprintId", "refreshInterval"],
                "states": ["loading", "ready", "error"]
            }
        ],
        "accessibility": {
            "wcag_level": "AA",
            "keyboard_navigation": True,
            "screen_reader_support": True
        }
    }


@pytest.fixture
def mock_engineering_output() -> Dict[str, Any]:
    """Mock output from engineering planning node."""
    return {
        "architecture": {
            "components": [
                {
                    "name": "StateGraph",
                    "type": "workflow_engine",
                    "technology": "LangGraph"
                },
                {
                    "name": "CheckpointManager",
                    "type": "persistence",
                    "technology": "MemorySaver"
                }
            ],
            "data_flow": "State flows through nodes sequentially with conditional branching"
        },
        "technical_approach": {
            "language": "Python 3.9+",
            "frameworks": ["LangGraph", "LangChain", "Anthropic"],
            "patterns": ["State Machine", "Command Pattern", "Strategy Pattern"]
        },
        "risks": [
            {
                "description": "Complex state management",
                "mitigation": "Strong TypedDict definitions, comprehensive tests",
                "severity": "medium"
            }
        ]
    }


@pytest.fixture
def mock_gap_analysis_output() -> Dict[str, Any]:
    """Mock output from gap analysis node."""
    return {
        "issues_found": [
            {
                "category": "security",
                "description": "Missing input validation on user-provided sprint theme",
                "recommendation": "Add input sanitization and length limits",
                "severity": "high"
            },
            {
                "category": "performance",
                "description": "No rate limiting for Anthropic API calls",
                "recommendation": "Implement exponential backoff and rate limiting",
                "severity": "medium"
            }
        ],
        "best_practices": [
            "Use async/await for all I/O operations",
            "Implement comprehensive error handling",
            "Add monitoring and observability"
        ],
        "approval_needed": True
    }


# ============================================================================
# WORKFLOW EXECUTION FIXTURES
# ============================================================================

@pytest.fixture
def mock_workflow_execution():
    """Mock successful workflow execution."""
    async def _execute(state: Dict[str, Any]) -> Dict[str, Any]:
        """Mock workflow execution that updates state."""
        state["phase"] = "complete"
        state["completed_at"] = "2025-11-09T12:00:00"
        state["status_messages"].append("Workflow complete")
        return state

    return _execute


@pytest.fixture
def mock_node_execution():
    """Mock individual node execution."""
    def _create_node_mock(output_key: str, output_value: Any):
        """Create a mock node that updates state with given output."""
        async def _node(state: Dict[str, Any]) -> Dict[str, Any]:
            state[output_key] = output_value
            return state

        return _node

    return _create_node_mock


# ============================================================================
# VERIFICATION FIXTURES
# ============================================================================

@pytest.fixture
def mock_verification_result():
    """Mock verification result for a job."""
    def _create_result(passed: bool = True, feedback: str = "") -> Dict[str, Any]:
        return {
            "passed": passed,
            "tests_run": 10,
            "tests_passed": 10 if passed else 7,
            "tests_failed": 0 if passed else 3,
            "coverage_percent": 85.0,
            "feedback": feedback or ("All tests passed" if passed else "Some tests failed"),
            "details": {
                "test_failures": [] if passed else [
                    "test_feature_x: AssertionError",
                    "test_integration: ConnectionError",
                    "test_edge_case: ValueError"
                ]
            }
        }

    return _create_result

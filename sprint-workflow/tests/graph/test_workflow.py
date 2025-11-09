"""Tests for LangGraph workflow graph structure."""

import pytest
from datetime import datetime

from graph.workflow import (
    build_workflow,
    compile_workflow,
    should_apply_gap_feedback,
    should_apply_job_feedback,
    should_continue_verification,
)
from graph.state import SprintWorkflowState


class TestWorkflowBuilder:
    """Tests for build_workflow function."""

    def test_workflow_builds_successfully(self):
        """Test that workflow graph builds without errors."""
        workflow = build_workflow()
        assert workflow is not None

    def test_workflow_has_all_nodes(self):
        """Test that workflow includes all expected nodes."""
        workflow = build_workflow()
        compiled = workflow.compile()

        # Get node names from the compiled graph
        graph = compiled.get_graph()
        nodes = [node.name for node in graph.nodes.values()]

        # Planning nodes
        assert "pm_planning" in nodes
        assert "ux_planning" in nodes
        assert "engineering_planning" in nodes
        assert "synthesize_planning" in nodes

        # Gap analysis nodes
        assert "gap_analysis" in nodes
        assert "update_planning_from_feedback" in nodes

        # PRD & job creation nodes
        assert "generate_sprint_prd" in nodes
        assert "create_jobs" in nodes
        assert "validate_jobs" in nodes
        assert "update_jobs_from_feedback" in nodes

        # Implementation nodes
        assert "setup_git_worktrees" in nodes
        assert "parallel_implementation" in nodes
        assert "verification_loop" in nodes

        # Branch management nodes
        assert "manage_branches" in nodes
        assert "push_and_merge" in nodes
        assert "generate_final_report" in nodes

    def test_workflow_compiles_with_checkpointer(self):
        """Test that workflow compiles with checkpointing enabled."""
        app = compile_workflow(checkpointer=True)
        assert app is not None

    def test_workflow_compiles_without_checkpointer(self):
        """Test that workflow compiles without checkpointing."""
        app = compile_workflow(checkpointer=False)
        assert app is not None


class TestConditionalEdges:
    """Tests for conditional edge decision functions."""

    def test_gap_feedback_approved_when_no_issues(self):
        """Test gap analysis approves when no issues found."""
        state: SprintWorkflowState = {
            "gap_analysis": {"issues_found": []},
            "retry_counts": {},
        }

        decision = should_apply_gap_feedback(state)
        assert decision == "approved"

    def test_gap_feedback_applies_when_issues_found(self):
        """Test gap analysis applies feedback when issues found."""
        state: SprintWorkflowState = {
            "gap_analysis": {
                "issues_found": [
                    {"description": "Missing security validation"}
                ]
            },
            "retry_counts": {"gap_analysis": 1},
        }

        decision = should_apply_gap_feedback(state)
        assert decision == "apply_feedback"

    def test_gap_feedback_max_retries(self):
        """Test gap analysis proceeds after max retries."""
        state: SprintWorkflowState = {
            "gap_analysis": {
                "issues_found": [
                    {"description": "Still has issues"}
                ]
            },
            "retry_counts": {"gap_analysis": 3},
        }

        decision = should_apply_gap_feedback(state)
        assert decision == "max_retries"

    def test_gap_feedback_approved_when_no_analysis(self):
        """Test gap analysis approves when no analysis run yet."""
        state: SprintWorkflowState = {
            "gap_analysis": None,
            "retry_counts": {},
        }

        decision = should_apply_gap_feedback(state)
        assert decision == "approved"

    def test_job_feedback_approved_by_default(self):
        """Test job validation approves by default (stub)."""
        state: SprintWorkflowState = {
            "retry_counts": {},
        }

        decision = should_apply_job_feedback(state)
        assert decision == "approved"

    def test_job_feedback_max_retries(self):
        """Test job validation proceeds after max retries."""
        state: SprintWorkflowState = {
            "retry_counts": {"job_validation": 3},
        }

        decision = should_apply_job_feedback(state)
        assert decision == "max_retries"

    def test_verification_retry_when_jobs_implementing(self):
        """Test verification retries when jobs still implementing."""
        state: SprintWorkflowState = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "implementing"},
            ]
        }

        decision = should_continue_verification(state)
        assert decision == "retry"

    def test_verification_retry_when_jobs_verifying(self):
        """Test verification retries when jobs still verifying."""
        state: SprintWorkflowState = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "verifying"},
            ]
        }

        decision = should_continue_verification(state)
        assert decision == "retry"

    def test_verification_continue_when_all_complete(self):
        """Test verification continues when all jobs complete."""
        state: SprintWorkflowState = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "verified"},
                {"name": "job3", "status": "failed"},
            ]
        }

        decision = should_continue_verification(state)
        assert decision == "continue"

    def test_verification_continue_when_no_jobs(self):
        """Test verification continues when no jobs exist."""
        state: SprintWorkflowState = {
            "jobs": []
        }

        decision = should_continue_verification(state)
        assert decision == "continue"


class TestWorkflowExecution:
    """Tests for end-to-end workflow execution with stubs."""

    @pytest.mark.asyncio
    async def test_workflow_executes_with_minimal_state(self, sample_sprint_state):
        """Test workflow executes end-to-end with minimal state."""
        app = compile_workflow(checkpointer=True)

        # Extend sample state with required fields for workflow
        state = sample_sprint_state.copy()
        state.update({
            "gap_analysis": None,
            "retry_counts": {},
            "jobs": [],
        })

        config = {"configurable": {"thread_id": "test-workflow-1"}}

        # Execute workflow
        # Note: With stub nodes, this should complete quickly
        result = await app.ainvoke(state, config)

        # Verify state was returned
        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_workflow_checkpointing(self, sample_sprint_state):
        """Test workflow checkpointing works."""
        app = compile_workflow(checkpointer=True)

        state = sample_sprint_state.copy()
        state.update({
            "gap_analysis": None,
            "retry_counts": {},
            "jobs": [],
        })

        config = {"configurable": {"thread_id": "test-checkpoint-1"}}

        # Execute workflow
        result = await app.ainvoke(state, config)

        # Get checkpoint history
        history = []
        for checkpoint in app.get_state_history(config):
            history.append(checkpoint)

        # Should have checkpoints
        assert len(history) > 0

    @pytest.mark.asyncio
    async def test_workflow_with_gap_feedback_loop(self, sample_sprint_state):
        """Test workflow handles gap analysis feedback loop."""
        app = compile_workflow(checkpointer=True)

        state = sample_sprint_state.copy()
        state.update({
            "gap_analysis": {
                "issues_found": [{"description": "Test issue"}]
            },
            "retry_counts": {"gap_analysis": 0},
            "jobs": [],
        })

        config = {"configurable": {"thread_id": "test-gap-loop-1"}}

        # Execute workflow - should handle feedback loop
        result = await app.ainvoke(state, config)

        # Workflow should complete despite feedback loop
        # (max retries will eventually allow it to proceed)
        assert result is not None


class TestWorkflowVisualization:
    """Tests for workflow visualization."""

    def test_visualization_generates(self):
        """Test that workflow visualization generates text output."""
        from graph.workflow import get_workflow_visualization

        viz = get_workflow_visualization()

        assert viz is not None
        assert len(viz) > 0
        assert "Sprint Workflow Graph Structure" in viz
        assert "pm_planning" in viz
        assert "gap_analysis" in viz
        assert "verification_loop" in viz

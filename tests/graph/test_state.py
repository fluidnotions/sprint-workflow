"""Tests for LangGraph state schema definitions."""

import pytest
from typing import get_type_hints

from graph.state import (
    SprintWorkflowState,
    JobSpec,
    RepoInfo,
    ErrorRecord,
    WorkflowPhase,
    JobStatus,
)


class TestJobSpec:
    """Tests for JobSpec TypedDict."""

    def test_job_spec_structure(self):
        """Test JobSpec has all required fields."""
        hints = get_type_hints(JobSpec)

        assert "name" in hints
        assert "task_file" in hints
        assert "worktree" in hints
        assert "repo_root" in hints
        assert "branch" in hints
        assert "todos" in hints
        assert "story_points" in hints
        assert "status" in hints
        assert "retry_count" in hints

    def test_job_spec_instance(self):
        """Test creating a JobSpec instance."""
        job: JobSpec = {
            "name": "test-job",
            "task_file": "tasks/test.md",
            "worktree": "worktrees/feat-test",
            "repo_root": "/path/to/repo",
            "branch": "feat-test",
            "todos": ["Task 1", "Task 2"],
            "story_points": 5,
            "status": "pending",
            "retry_count": 0,
            "error_message": None,
            "files_to_modify": ["file1.py", "file2.py"],
            "dependencies": [],
        }

        assert job["name"] == "test-job"
        assert job["story_points"] == 5
        assert job["status"] == "pending"


class TestRepoInfo:
    """Tests for RepoInfo TypedDict."""

    def test_repo_info_structure(self):
        """Test RepoInfo has all required fields."""
        hints = get_type_hints(RepoInfo)

        assert "path" in hints
        assert "has_remote" in hints
        assert "branches" in hints
        assert "default_branch" in hints

    def test_repo_info_instance(self):
        """Test creating a RepoInfo instance."""
        repo: RepoInfo = {
            "path": "/path/to/repo",
            "has_remote": True,
            "branches": ["main", "feat-test"],
            "default_branch": "main",
        }

        assert repo["has_remote"] is True
        assert len(repo["branches"]) == 2


class TestErrorRecord:
    """Tests for ErrorRecord TypedDict."""

    def test_error_record_structure(self):
        """Test ErrorRecord has all required fields."""
        hints = get_type_hints(ErrorRecord)

        assert "job" in hints
        assert "phase" in hints
        assert "error" in hints
        assert "timestamp" in hints
        assert "report_path" in hints

    def test_error_record_instance(self):
        """Test creating an ErrorRecord instance."""
        from datetime import datetime

        error: ErrorRecord = {
            "job": "test-job",
            "phase": "verification",
            "error": "Tests failed",
            "timestamp": datetime.now().isoformat(),
            "report_path": "errors/test-job.md",
        }

        assert error["job"] == "test-job"
        assert error["phase"] == "verification"


class TestSprintWorkflowState:
    """Tests for SprintWorkflowState TypedDict."""

    def test_sprint_state_structure(self):
        """Test SprintWorkflowState has all required fields."""
        hints = get_type_hints(SprintWorkflowState)

        # Input fields
        assert "sprint_theme" in hints
        assert "project_name" in hints
        assert "features" in hints
        assert "pool_size" in hints

        # Phase tracking
        assert "phase" in hints

        # Planning outputs
        assert "pm_output" in hints
        assert "ux_output" in hints
        assert "engineering_output" in hints
        assert "synthesis_output" in hints

        # Validation
        assert "gap_analysis" in hints
        assert "retry_counts" in hints

        # Sprint artifacts
        assert "sprint_prd_path" in hints
        assert "todos_path" in hints

        # Jobs
        assert "jobs" in hints
        assert "jobs_implementing" in hints
        assert "jobs_verifying" in hints
        assert "jobs_verified" in hints
        assert "jobs_failed" in hints

        # Repositories
        assert "repos" in hints
        assert "worktrees" in hints
        assert "branch_status" in hints
        assert "merge_status" in hints

        # Errors
        assert "errors" in hints

        # Metadata
        assert "started_at" in hints
        assert "completed_at" in hints
        assert "checkpoints" in hints
        assert "status_messages" in hints

    def test_sprint_state_minimal_instance(self):
        """Test creating a minimal SprintWorkflowState instance."""
        from datetime import datetime

        state: SprintWorkflowState = {
            "sprint_theme": "Test Sprint",
            "project_name": "test-project",
            "features": ["Feature 1", "Feature 2"],
            "pool_size": 3,
            "phase": "init",
            "retry_counts": {},
            "jobs": [],
            "jobs_implementing": [],
            "jobs_verifying": [],
            "jobs_verified": [],
            "jobs_failed": [],
            "repos": [],
            "worktrees": [],
            "branch_status": [],
            "merge_status": [],
            "errors": [],
            "started_at": datetime.now().isoformat(),
            "checkpoints": [],
            "status_messages": [],
        }

        assert state["sprint_theme"] == "Test Sprint"
        assert state["pool_size"] == 3
        assert state["phase"] == "init"
        assert len(state["jobs"]) == 0

    def test_sprint_state_with_jobs(self):
        """Test SprintWorkflowState with jobs populated."""
        from datetime import datetime

        job1: JobSpec = {
            "name": "infrastructure",
            "task_file": "tasks/infra.md",
            "worktree": "worktrees/feat-infra",
            "repo_root": "/repo",
            "branch": "feat-infra",
            "todos": ["Setup DB", "Configure CI"],
            "story_points": 8,
            "status": "pending",
            "retry_count": 0,
            "error_message": None,
            "files_to_modify": [],
            "dependencies": [],
        }

        state: SprintWorkflowState = {
            "sprint_theme": "Infrastructure Sprint",
            "project_name": "my-project",
            "features": ["CI/CD", "Database"],
            "pool_size": 2,
            "phase": "job_creation",
            "retry_counts": {"gap_analysis": 1},
            "jobs": [job1],
            "jobs_implementing": [],
            "jobs_verifying": [],
            "jobs_verified": [],
            "jobs_failed": [],
            "repos": [],
            "worktrees": [],
            "branch_status": [],
            "merge_status": [],
            "errors": [],
            "started_at": datetime.now().isoformat(),
            "checkpoints": ["init", "planning"],
            "status_messages": ["Sprint initialized", "Planning complete"],
        }

        assert len(state["jobs"]) == 1
        assert state["jobs"][0]["name"] == "infrastructure"
        assert state["jobs"][0]["story_points"] == 8
        assert len(state["checkpoints"]) == 2


class TestTypeAliases:
    """Tests for type aliases."""

    def test_workflow_phase_values(self):
        """Test WorkflowPhase literal values."""
        valid_phases = [
            "init",
            "planning",
            "gap_analysis",
            "prd_generation",
            "job_creation",
            "job_validation",
            "worktree_setup",
            "implementation",
            "verification",
            "branch_mgmt",
            "merging",
            "complete",
            "error",
        ]

        # This test just validates we can import the type
        # TypedDict Literal validation happens at type-check time
        from graph.state import WorkflowPhase
        assert WorkflowPhase is not None

    def test_job_status_values(self):
        """Test JobStatus literal values."""
        valid_statuses = [
            "pending",
            "implementing",
            "verifying",
            "verified",
            "failed",
        ]

        # This test just validates we can import the type
        from graph.state import JobStatus
        assert JobStatus is not None

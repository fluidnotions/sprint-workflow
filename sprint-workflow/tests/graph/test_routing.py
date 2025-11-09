"""Tests for conditional routing logic."""

import pytest
from graph.routing import (
    should_apply_gap_feedback,
    should_apply_job_feedback,
    should_continue_verification,
    should_retry_on_error,
)


class TestGapFeedbackRouting:
    """Tests for gap analysis feedback routing."""

    def test_no_gap_analysis_approves(self):
        """Test that missing gap analysis auto-approves."""
        state = {"gap_analysis": None, "retry_counts": {}}
        
        result = should_apply_gap_feedback(state)
        
        assert result == "approved"

    def test_critical_blockers_apply_feedback(self):
        """Test that critical blockers trigger feedback loop."""
        state = {
            "gap_analysis": {
                "issues_found": [{"severity": "critical"}],
                "overall_assessment": {
                    "critical_blockers": 1,
                    "high_priority_items": 0,
                    "recommendation": "revise"
                }
            },
            "retry_counts": {"gap_analysis": 1}
        }
        
        result = should_apply_gap_feedback(state)
        
        assert result == "apply_feedback"

    def test_high_priority_with_revise_applies_feedback(self):
        """Test that high priority issues with revise recommendation apply feedback."""
        state = {
            "gap_analysis": {
                "issues_found": [{"severity": "high"}],
                "overall_assessment": {
                    "critical_blockers": 0,
                    "high_priority_items": 2,
                    "recommendation": "revise"
                }
            },
            "retry_counts": {"gap_analysis": 0}
        }
        
        result = should_apply_gap_feedback(state)
        
        assert result == "apply_feedback"

    def test_high_priority_with_approve_passes(self):
        """Test that high priority items don't block if recommendation is approve."""
        state = {
            "gap_analysis": {
                "issues_found": [{"severity": "high"}],
                "overall_assessment": {
                    "critical_blockers": 0,
                    "high_priority_items": 1,
                    "recommendation": "approve"
                }
            },
            "retry_counts": {}
        }
        
        result = should_apply_gap_feedback(state)
        
        assert result == "approved"

    def test_max_retries_proceeds_anyway(self):
        """Test that max retries causes bypass even with issues."""
        state = {
            "gap_analysis": {
                "issues_found": [{"severity": "critical"}],
                "overall_assessment": {
                    "critical_blockers": 1,
                    "high_priority_items": 0,
                    "recommendation": "major_revision"
                }
            },
            "retry_counts": {"gap_analysis": 3}
        }
        
        result = should_apply_gap_feedback(state)
        
        assert result == "max_retries"


class TestJobFeedbackRouting:
    """Tests for job validation feedback routing."""

    def test_no_validation_approves(self):
        """Test that missing validation auto-approves."""
        state = {"retry_counts": {}}
        
        result = should_apply_job_feedback(state)
        
        assert result == "approved"

    def test_validation_issues_apply_feedback(self):
        """Test that validation issues trigger feedback."""
        state = {
            "job_validation": {
                "issues": [
                    {"description": "Job overlap detected"}
                ]
            },
            "retry_counts": {"job_validation": 0}
        }
        
        result = should_apply_job_feedback(state)
        
        assert result == "apply_feedback"

    def test_max_retries_proceeds(self):
        """Test max retries bypass."""
        state = {
            "job_validation": {"issues": [{}]},
            "retry_counts": {"job_validation": 3}
        }
        
        result = should_apply_job_feedback(state)
        
        assert result == "max_retries"


class TestVerificationRouting:
    """Tests for verification loop routing."""

    def test_implementing_jobs_retry(self):
        """Test that implementing jobs continue verification loop."""
        state = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "implementing"}
            ]
        }
        
        result = should_continue_verification(state)
        
        assert result == "retry"

    def test_verifying_jobs_retry(self):
        """Test that verifying jobs continue loop."""
        state = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "verifying"}
            ]
        }
        
        result = should_continue_verification(state)
        
        assert result == "retry"

    def test_all_verified_continues(self):
        """Test that all verified jobs exit loop."""
        state = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "verified"}
            ]
        }
        
        result = should_continue_verification(state)
        
        assert result == "continue"

    def test_mixed_terminal_states_continues(self):
        """Test that mix of verified/failed exits loop."""
        state = {
            "jobs": [
                {"name": "job1", "status": "verified"},
                {"name": "job2", "status": "failed"}
            ]
        }
        
        result = should_continue_verification(state)
        
        assert result == "continue"

    def test_no_jobs_continues(self):
        """Test that no jobs exits loop."""
        state = {"jobs": []}
        
        result = should_continue_verification(state)
        
        assert result == "continue"


class TestErrorRetryRouting:
    """Tests for error retry routing."""

    def test_first_error_retries(self):
        """Test that first error retries."""
        state = {"retry_counts": {}}
        
        result = should_retry_on_error(state, "network_error")
        
        assert result == "retry"

    def test_max_retries_fails(self):
        """Test that max retries causes failure."""
        state = {"retry_counts": {"api_error": 3}}
        
        result = should_retry_on_error(state, "api_error")
        
        assert result == "fail"

    def test_retry_tracking(self):
        """Test retry count tracking."""
        state = {"retry_counts": {"db_error": 2}}
        
        result = should_retry_on_error(state, "db_error")
        
        assert result == "retry"

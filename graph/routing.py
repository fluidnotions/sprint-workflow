"""Conditional routing logic for workflow edges.

This module contains all decision functions that determine
which path the workflow takes at conditional branches.
"""

from typing import Literal
import logging

from .state import SprintWorkflowState

# Configure logging
logger = logging.getLogger(__name__)


def should_apply_gap_feedback(
    state: SprintWorkflowState
) -> Literal["apply_feedback", "approved", "max_retries"]:
    """Decide whether to apply gap analysis feedback or proceed.
    
    Decision logic:
    1. If no gap analysis yet → approve (first time through)
    2. If retry count >= 3 → max_retries (prevent infinite loops)
    3. If critical/high issues found → apply_feedback (need revision)
    4. If only low/medium issues or no issues → approved
    
    Args:
        state: Current workflow state
        
    Returns:
        - "apply_feedback": Gap analysis found critical issues, revise planning
        - "approved": No critical issues, proceed to PRD generation
        - "max_retries": Max retries reached, proceed despite issues
    """
    gap_analysis = state.get("gap_analysis")
    
    # First time through - no analysis yet
    if not gap_analysis:
        logger.info("No gap analysis found - approving by default")
        return "approved"
    
    # Check retry count to prevent infinite loops
    retry_count = state.get("retry_counts", {}).get("gap_analysis", 0)
    if retry_count >= 3:
        logger.warning(
            f"Gap analysis retry limit reached ({retry_count} attempts) - "
            "proceeding despite issues"
        )
        return "max_retries"
    
    # Analyze severity of issues found
    issues = gap_analysis.get("issues_found", [])
    overall = gap_analysis.get("overall_assessment", {})
    
    critical_count = overall.get("critical_blockers", 0)
    high_priority_count = overall.get("high_priority_items", 0)
    recommendation = overall.get("recommendation", "approve")
    
    # Critical blockers always require feedback
    if critical_count > 0:
        logger.info(
            f"Found {critical_count} critical blocker(s) - applying feedback"
        )
        return "apply_feedback"
    
    # High priority items + "revise" recommendation require feedback
    if high_priority_count > 0 and recommendation in ["revise", "major_revision"]:
        logger.info(
            f"Found {high_priority_count} high priority issue(s) "
            f"with recommendation '{recommendation}' - applying feedback"
        )
        return "apply_feedback"
    
    # Otherwise approve
    logger.info(
        f"Gap analysis passed: {len(issues)} total issues, "
        f"{critical_count} critical, {high_priority_count} high priority - approving"
    )
    return "approved"


def should_apply_job_feedback(
    state: SprintWorkflowState
) -> Literal["apply_feedback", "approved", "max_retries"]:
    """Decide whether to apply job validation feedback or proceed.
    
    Decision logic:
    1. If retry count >= 3 → max_retries
    2. If job validation found issues → apply_feedback
    3. Otherwise → approved
    
    Args:
        state: Current workflow state
        
    Returns:
        - "apply_feedback": Job validation found issues, revise jobs
        - "approved": Jobs validated, proceed to worktree setup
        - "max_retries": Max retries reached, proceed anyway
    """
    # Check retry count
    retry_count = state.get("retry_counts", {}).get("job_validation", 0)
    if retry_count >= 3:
        logger.warning(
            f"Job validation retry limit reached ({retry_count} attempts) - "
            "proceeding anyway"
        )
        return "max_retries"
    
    # Check job validation results (will be implemented in Batch 4)
    job_validation = state.get("job_validation")
    
    if job_validation:
        validation_issues = job_validation.get("issues", [])
        if validation_issues:
            logger.info(
                f"Job validation found {len(validation_issues)} issue(s) - "
                "applying feedback"
            )
            return "apply_feedback"
    
    logger.info("Job validation passed - approving")
    return "approved"


def should_continue_verification(
    state: SprintWorkflowState
) -> Literal["retry", "continue"]:
    """Decide whether to continue verification loop or proceed.
    
    Decision logic:
    1. If any job is "implementing" or "verifying" → retry (still in progress)
    2. All jobs in terminal states (verified/failed/cancelled) → continue
    
    Args:
        state: Current workflow state
        
    Returns:
        - "retry": Jobs still in progress, continue verification loop
        - "continue": All jobs complete, proceed to branch management
    """
    jobs = state.get("jobs", [])
    
    if not jobs:
        logger.warning("No jobs found - continuing to branch management")
        return "continue"
    
    # Count jobs by status
    status_counts = {
        "implementing": 0,
        "verifying": 0,
        "verified": 0,
        "failed": 0,
        "cancelled": 0,
    }
    
    for job in jobs:
        status = job.get("status", "unknown")
        if status in status_counts:
            status_counts[status] += 1
    
    in_progress = status_counts["implementing"] + status_counts["verifying"]
    completed = status_counts["verified"] + status_counts["failed"] + status_counts["cancelled"]
    
    if in_progress > 0:
        logger.info(
            f"Verification loop: {in_progress} job(s) still in progress "
            f"({status_counts['implementing']} implementing, "
            f"{status_counts['verifying']} verifying) - retrying"
        )
        return "retry"
    
    logger.info(
        f"Verification complete: {completed} job(s) finished "
        f"({status_counts['verified']} verified, {status_counts['failed']} failed) - continuing"
    )
    return "continue"


def should_retry_on_error(
    state: SprintWorkflowState,
    error_type: str
) -> Literal["retry", "fail"]:
    """Decide whether to retry after an error or fail the workflow.
    
    Generic error retry logic with exponential backoff awareness.
    
    Args:
        state: Current workflow state
        error_type: Type of error (for tracking retry counts)
        
    Returns:
        - "retry": Retry the operation
        - "fail": Give up and fail the workflow
    """
    retry_counts = state.get("retry_counts", {})
    current_retries = retry_counts.get(error_type, 0)
    max_retries = 3
    
    if current_retries >= max_retries:
        logger.error(
            f"Max retries ({max_retries}) exceeded for {error_type} - failing"
        )
        return "fail"
    
    logger.warning(
        f"Error in {error_type} - retrying (attempt {current_retries + 1}/{max_retries})"
    )
    return "retry"

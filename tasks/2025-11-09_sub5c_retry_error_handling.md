# Sub-Task 5C: Retry Logic & Error Handling

## Parent Job
Week 5-6: Implementation & Verification

## Story Points
4

## Scope
Implement retry logic with feedback for failed verifications and non-blocking error handling for permanently failed jobs.

## Can Run in Parallel
YES - Parallel with 5A (implementation), 5B (verification)

## Todos
- [ ] Implement retry counter per job
- [ ] Generate verification feedback for failed jobs
- [ ] Re-spawn implementation agent with feedback
- [ ] Track retry iterations (max 5)
- [ ] Implement non-blocking failure handling
- [ ] Mark jobs as failed after max retries
- [ ] Generate error reports (write_error_report helper)
- [ ] Add errors to state.errors list
- [ ] Continue sprint execution despite failures
- [ ] Write unit tests for retry logic
- [ ] Write unit tests for error handling
- [ ] Test retry loop with simulated failures

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/execution.py (modify - add retry and error handling)
- sprint-workflow/langgraph/state.py (modify - add errors field)
- sprint-workflow/tests/langgraph/test_execution_nodes.py (modify - add retry/error tests)

## Dependencies
- Sub-task 5B (needs verification results to trigger retries)

## Blocks
- Sub-task 5D (integration needs retry logic)

## Implementation Notes
```python
async def handle_verification_failures(state: SprintWorkflowState) -> dict:
    """Handle failed verifications with retry or mark as failed."""
    implementing_jobs = state.get("implementing_jobs", [])
    verified_jobs = state.get("verified_jobs", [])
    failed_jobs = state.get("failed_jobs", [])
    errors = state.get("errors", [])

    for job_status in implementing_jobs:
        if job_status.get("status") != "verification_failed":
            continue

        retry_count = job_status.get("retry_count", 0)

        if retry_count < 5:
            # Generate feedback and retry
            feedback = generate_verification_feedback(
                job_status["verification_failure"]
            )

            # Re-spawn agent with feedback
            job = find_job_by_name(state["jobs"], job_status["job_name"])
            agent_id = await spawn_implementation_agent_with_feedback(
                job, state, feedback
            )

            job_status["agent_id"] = agent_id
            job_status["retry_count"] = retry_count + 1
            job_status["status"] = "implementing"
            job_status["feedback"] = feedback
        else:
            # Max retries reached - mark as failed
            job_status["status"] = "failed"
            failed_jobs.append(job_status["job_name"])

            # Generate error report
            error_report_path = write_error_report(
                job_status,
                job_status["verification_failure"]
            )

            errors.append({
                "job_name": job_status["job_name"],
                "error_type": "verification_failure",
                "report_path": error_report_path,
                "retry_count": retry_count
            })

            # Log but don't stop sprint
            print(f"⚠️  Job failed: {job_status['job_name']}")
            print(f"📄 Error report: {error_report_path}")
            print("ℹ️  Sprint continues - other jobs proceeding")

    return {
        "implementing_jobs": implementing_jobs,
        "verified_jobs": verified_jobs,
        "failed_jobs": failed_jobs,
        "errors": errors,
        "phase": "handling_failures"
    }

def generate_verification_feedback(verification_failure: dict) -> str:
    """Generate feedback for failed verification."""
    feedback = "Verification failed. Please address the following:\n\n"

    for check_name, check_result in verification_failure["checks"].items():
        if not check_result["passed"]:
            feedback += f"## {check_name.title()}\n"
            feedback += f"{check_result.get('message', 'Check failed')}\n"
            feedback += f"```\n{check_result.get('errors', '')}\n```\n\n"

    return feedback

async def spawn_implementation_agent_with_feedback(
    job: dict,
    state: SprintWorkflowState,
    feedback: str
) -> str:
    """Re-spawn implementation agent with verification feedback."""
    # Similar to spawn_implementation_agent but includes feedback
    task_file = job["task_file"]
    job_spec = read_file(task_file)
    prd = read_file(state["sprint_prd_path"])

    prompt = f"""
You are re-implementing: {job['name']} (Retry #{job.get('retry_count', 0) + 1})

## Job Specification
{job_spec}

## Sprint PRD Context
{prd}

## Previous Verification Feedback
{feedback}

## Instructions
1. Address the verification failures above
2. Re-implement the affected components
3. Run tests to verify fixes
4. Update task file with progress
"""

    agent_id = await spawn_claude_code_agent(
        prompt=prompt,
        working_directory=job["worktree_path"],
        model="claude-sonnet-4-5-20250929"
    )

    return agent_id

def write_error_report(job_status: dict, verification_failure: dict) -> str:
    """Write detailed error report for failed job."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"sprint_errors_{timestamp}_{job_status['job_name']}.md"

    report = f"""# Sprint Error Report: {job_status['job_name']}

**Status**: failed
**Phase**: Verification
**Iterations Attempted**: {job_status.get('retry_count', 0)}

## Error Details

{format_verification_failure(verification_failure)}

## Job Specification
Path: {job_status.get('task_file', 'Unknown')}
Worktree: {job_status.get('worktree_path', 'Unknown')}
Branch: {job_status.get('branch', 'Unknown')}

## Next Steps for Manual Resolution
1. Check worktree: cd {job_status.get('worktree_path', 'worktrees/...')}
2. Run tests manually
3. Fix failures
4. Re-run verification
"""

    write_file(report_path, report)
    return report_path
```

## Success Criteria
- Retry logic implemented
- Verification feedback generated
- Agent re-spawning with feedback working
- Max retries enforced (5)
- Non-blocking error handling
- Error reports generated
- errors list in state
- Sprint continues despite failures
- Unit tests passing
- Retry scenarios tested

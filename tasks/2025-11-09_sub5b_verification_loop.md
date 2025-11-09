# Sub-Task 5B: Verification Loop Node

## Parent Job
Week 5-6: Implementation & Verification

## Story Points
5

## Scope
Implement verification checks for completed jobs including tests, quality checks, and acceptance criteria validation.

## Can Run in Parallel
YES - Parallel with 5A (implementation), 5C (error handling)

## Todos
- [ ] Implement verification_loop() node function
- [ ] Define verify_job() async function for individual job verification
- [ ] Run tests in job worktree (pytest, npm test, etc.)
- [ ] Check code quality standards (linting, type hints)
- [ ] Validate acceptance criteria completion
- [ ] Track verification results in state
- [ ] Add verified_jobs list to state schema
- [ ] Write unit tests for verification logic
- [ ] Test verification with simulated pass/fail scenarios

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/execution.py (modify - add verification)
- sprint-workflow/langgraph/state.py (modify - add verified_jobs, failed_jobs)
- sprint-workflow/tests/langgraph/test_execution_nodes.py (modify - add verification tests)

## Dependencies
- Sub-task 4D (needs worktrees for testing)

## Blocks
- Sub-task 5D (integration needs verification logic)

## Implementation Notes
```python
async def verification_loop(state: SprintWorkflowState) -> dict:
    """Verify implemented jobs."""
    implementing_jobs = state.get("implementing_jobs", [])
    verified_jobs = state.get("verified_jobs", [])
    failed_jobs = state.get("failed_jobs", [])

    for job_status in implementing_jobs:
        if job_status["status"] == "implementing":
            # Wait for agent completion (check if agent finished)
            is_complete = await check_agent_completion(job_status["agent_id"])

            if not is_complete:
                continue  # Still implementing

        # Run verification
        verification_result = await verify_job(job_status["job_name"], state)

        if verification_result["passed"]:
            # Verification passed
            verified_jobs.append(job_status["job_name"])
        else:
            # Verification failed - handle in retry logic (sub-task 5C)
            job_status["verification_failure"] = verification_result
            job_status["status"] = "verification_failed"

    return {
        "verified_jobs": verified_jobs,
        "failed_jobs": failed_jobs,
        "implementing_jobs": implementing_jobs,
        "phase": "verification_in_progress"
    }

async def verify_job(job_name: str, state: SprintWorkflowState) -> dict:
    """Run verification checks on a job."""
    # Find job in state
    job = find_job_by_name(state["jobs"], job_name)
    worktree_path = job["worktree_path"]

    results = {
        "passed": True,
        "checks": {}
    }

    # 1. Run tests
    test_result = await run_tests_in_worktree(worktree_path)
    results["checks"]["tests"] = test_result
    if not test_result["passed"]:
        results["passed"] = False

    # 2. Check code quality
    quality_result = await check_code_quality(worktree_path)
    results["checks"]["quality"] = quality_result
    if not quality_result["passed"]:
        results["passed"] = False

    # 3. Validate acceptance criteria
    criteria_result = await validate_acceptance_criteria(job, state)
    results["checks"]["acceptance_criteria"] = criteria_result
    if not criteria_result["passed"]:
        results["passed"] = False

    # 4. Check file existence
    files_result = check_expected_files(job, worktree_path)
    results["checks"]["files"] = files_result
    if not files_result["passed"]:
        results["passed"] = False

    return results

async def run_tests_in_worktree(worktree_path: str) -> dict:
    """Run tests in worktree."""
    os.chdir(worktree_path)

    # Detect test framework
    if os.path.exists("pytest.ini") or os.path.exists("setup.py"):
        # Python - pytest
        result = subprocess.run(["pytest"], capture_output=True)
    elif os.path.exists("package.json"):
        # Node.js - npm test
        result = subprocess.run(["npm", "test"], capture_output=True)
    else:
        return {"passed": True, "message": "No tests found"}

    return {
        "passed": result.returncode == 0,
        "output": result.stdout.decode(),
        "errors": result.stderr.decode()
    }

async def check_code_quality(worktree_path: str) -> dict:
    """Check linting, type hints, documentation."""
    # Run linters, type checkers
    # Return pass/fail
    return {"passed": True}

async def validate_acceptance_criteria(job: dict, state: SprintWorkflowState) -> dict:
    """Validate acceptance criteria from PRD."""
    # Parse PRD for acceptance criteria
    # Check if implemented
    return {"passed": True}
```

## Success Criteria
- Verification loop node implemented
- verify_job() function working
- Test execution in worktrees
- Code quality checks implemented
- Acceptance criteria validation working
- verified_jobs and failed_jobs tracked
- Unit tests passing
- Pass/fail scenarios tested
- Integration with worktrees validated

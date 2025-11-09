# Job: Implementation & Verification

## Overview
Implement parallel job execution with automatic verification loops. Spawn implementation agents in batches, run tests and quality checks, handle retries with feedback, and manage non-blocking error handling. This is the most complex job with highest story points.

## Story Points
21

## Todos from Sprint
### Parallel Implementation Node
- [ ] Create langgraph/nodes/execution.py module
- [ ] Implement parallel_implementation() node function
- [ ] Batch jobs by pool_size for parallel execution
- [ ] Spawn implementation agents using asyncio.gather()
- [ ] Track implementing jobs in state
- [ ] Write unit tests for parallel batching logic

### Implementation Agent Spawning
- [ ] Implement spawn_implementation_agent() async function
- [ ] Read job specification and Sprint PRD
- [ ] Construct implementation prompt with context
- [ ] Integrate with Claude Code agent spawning (via Task tool or API)
- [ ] Handle agent output and status updates
- [ ] Test implementation agent spawning

### Verification Loop Node
- [ ] Implement verification_loop() node function
- [ ] Define verify_job() async function for individual job verification
- [ ] Run tests in job worktree
- [ ] Check code quality standards
- [ ] Validate acceptance criteria completion
- [ ] Track verification results in state

### Retry Logic
- [ ] Implement retry counter per job
- [ ] Generate verification feedback for failed jobs
- [ ] Re-spawn implementation agent with feedback
- [ ] Track retry iterations (max 5)
- [ ] Test retry loop with simulated failures

### Error Handling
- [ ] Implement non-blocking failure handling
- [ ] Mark jobs as failed after max retries
- [ ] Generate error reports (write_error_report helper)
- [ ] Add errors to state.errors list
- [ ] Continue sprint execution despite failures
- [ ] Write unit tests for error handling

### Verification Conditional Edge
- [ ] Implement should_continue_verification() decision function
- [ ] Check for jobs still implementing or verifying
- [ ] Route to retry or continue to branch management
- [ ] Test verification loop termination conditions
- [ ] Test mixed scenarios (some verified, some failed, some implementing)

## Implementation Plan
1. **Create execution.py module** - Set up implementation and verification nodes
2. **Implement parallel batching** - Divide jobs into batches by pool_size
3. **Implement agent spawning** - Create async function to spawn Claude Code agents
4. **Integrate with Task tool** - Connect to Claude Code agent spawning API
5. **Implement verification** - Run tests, quality checks, acceptance criteria validation
6. **Implement retry logic** - Track retries per job, re-spawn with feedback
7. **Implement error handling** - Non-blocking failures, error reporting
8. **Implement conditional routing** - Decision function for verification loop
9. **Update state schema** - Add implementing_jobs, verified_jobs, failed_jobs, retry_counts
10. **Write tests** - Test batching, spawning, verification, retries, error handling
11. **Integration test** - Test full implementation cycle with simulated jobs

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/execution.py (new - implementation and verification)
- sprint-workflow/langgraph/state.py (modify - add implementation tracking fields)
- sprint-workflow/langgraph/workflow.py (modify - connect implementation nodes)
- sprint-workflow/tests/langgraph/test_execution_nodes.py (new)

## Success Criteria
- All todos complete
- Parallel implementation node spawns agents in batches
- Verification loop node runs tests and quality checks
- Retry logic with feedback (max 5 iterations)
- Non-blocking error handling
- Error reports generated for failed jobs
- Sprint continues despite individual job failures
- All jobs reach terminal state (verified or failed)
- Tests passing for all execution scenarios

## Dependencies
- Depends on: Job 4 (Job Creation) - requires jobs and worktrees
- Required by: Job 7 (Branch Management) - verified jobs ready for merging

## Technical Notes
### Parallel Implementation Architecture
```python
async def parallel_implementation(state: SprintWorkflowState) -> dict:
    """Execute jobs in parallel batches."""
    pool_size = state.get("pool_size", 3)
    jobs = state["jobs"]

    # Batch jobs for parallel execution
    batches = create_batches(jobs, pool_size)

    implementing_jobs = []

    for batch in batches:
        # Spawn agents in parallel
        tasks = [
            spawn_implementation_agent(job, state)
            for job in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Track results
        for job, result in zip(batch, results):
            if isinstance(result, Exception):
                implementing_jobs.append({
                    "job_name": job["name"],
                    "status": "error",
                    "error": str(result)
                })
            else:
                implementing_jobs.append({
                    "job_name": job["name"],
                    "status": "implementing",
                    "agent_id": result["agent_id"]
                })

    return {
        "implementing_jobs": implementing_jobs,
        "phase": "implementation_started"
    }
```

### Implementation Agent Spawning
```python
async def spawn_implementation_agent(job: JobSpec, state: SprintWorkflowState) -> dict:
    """Spawn Claude Code implementation agent for job."""
    # Read job specification
    task_file = f"tasks/{job['task_file']}"
    job_spec = read_file(task_file)

    # Read Sprint PRD
    prd = read_file(state["sprint_prd_path"])

    # Construct implementation prompt
    prompt = f"""
You are an implementation agent working on: {job['name']}

## Job Specification
{job_spec}

## Sprint PRD Context
{prd}

## Worktree
Path: {job['worktree_path']}
Branch: {job['branch']}

## Instructions
Implement all todos in the job specification. Follow the implementation plan.
Run tests to verify your work. Update the task file with progress.
"""

    # Spawn agent via Claude Code API
    agent_id = await spawn_claude_code_agent(
        prompt=prompt,
        working_directory=job["worktree_path"],
        model="claude-sonnet-4-5-20250929"
    )

    return {
        "agent_id": agent_id,
        "job_name": job["name"]
    }
```

### Verification Strategy
```python
async def verification_loop(state: SprintWorkflowState) -> dict:
    """Verify implemented jobs."""
    implementing_jobs = state["implementing_jobs"]
    verified_jobs = []
    failed_jobs = []

    for job_status in implementing_jobs:
        if job_status["status"] == "implementing":
            # Wait for agent completion
            await wait_for_agent(job_status["agent_id"])

        # Run verification
        verification_result = await verify_job(job_status["job_name"], state)

        if verification_result["passed"]:
            verified_jobs.append(job_status)
        else:
            # Check retry count
            retry_count = job_status.get("retry_count", 0)

            if retry_count < 5:
                # Re-spawn with feedback
                feedback = generate_verification_feedback(verification_result)
                job_status["retry_count"] = retry_count + 1
                job_status["feedback"] = feedback

                # Re-spawn agent
                agent_id = await spawn_implementation_agent_with_feedback(
                    job_status, state, feedback
                )
                job_status["agent_id"] = agent_id
            else:
                # Max retries reached
                failed_jobs.append(job_status)
                write_error_report(job_status, verification_result)

    return {
        "verified_jobs": verified_jobs,
        "failed_jobs": failed_jobs,
        "phase": "verification_complete"
    }
```

### Verification Checks
1. **Test Execution** - Run pytest in worktree, verify all tests pass
2. **Code Quality** - Check linting, type hints, documentation
3. **Acceptance Criteria** - Validate user stories completed
4. **File Existence** - Verify all expected files created/modified
5. **Integration** - Check imports, dependencies, API contracts

### Non-Blocking Error Handling
- Continue sprint despite individual job failures
- Track errors in state.errors list
- Generate detailed error reports
- Mark jobs as "failed" but don't stop workflow
- Allow successful jobs to proceed to merging

### Conditional Routing Logic
```python
def should_continue_verification(state: SprintWorkflowState) -> str:
    """Decision function for verification loop."""
    implementing = [j for j in state["implementing_jobs"] if j["status"] == "implementing"]
    verifying = [j for j in state["implementing_jobs"] if j.get("retry_count", 0) > 0]

    if implementing or verifying:
        return "continue_verification"
    else:
        return "proceed_to_branch_mgmt"
```

### Testing Strategy
- Mock agent spawning for deterministic tests
- Simulate verification scenarios: pass, fail, error
- Test retry logic with various retry counts
- Test non-blocking failure handling
- Test batch execution with different pool sizes
- Test mixed scenarios (some pass, some fail, some error)

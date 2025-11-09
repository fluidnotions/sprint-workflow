# Sub-Task 4C: Job Validation & Feedback Loop

## Parent Job
Week 4: Job Creation & PRD Generation

## Story Points
3

## Scope
Run gap analysis on each job specification and implement feedback loop for job refinement.

## Can Run in Parallel
NO - Depends on 4B (needs jobs created)

## Todos
- [ ] Implement validate_jobs() node function
- [ ] Run gap analysis on each job specification
- [ ] Identify missing components per job
- [ ] Calculate story points per job
- [ ] Add job validation results to state
- [ ] Implement should_apply_job_feedback() decision function
- [ ] Implement update_jobs_from_feedback() node function
- [ ] Add conditional edge for job validation loop
- [ ] Test job feedback loop with simulated issues
- [ ] Test max retry escape condition

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/jobs.py (modify - add validation nodes)
- sprint-workflow/langgraph/state.py (modify - add job_validation_results)
- sprint-workflow/langgraph/workflow.py (modify - add job validation conditional edge)
- sprint-workflow/tests/langgraph/test_jobs_nodes.py (modify - add validation tests)

## Dependencies
- Sub-task 4B (needs jobs created)
- Sub-task 3A (reuses gap analysis logic)

## Blocks
- Sub-task 4D (worktree setup waits for validated jobs)

## Implementation Notes
```python
async def validate_jobs(state: SprintWorkflowState) -> dict:
    """Validate job specifications via gap analysis."""
    jobs = state["jobs"]
    validation_results = []

    for job in jobs:
        # Run gap analysis on job spec
        job_content = read_file(job["task_file"])
        prd = read_file(state["sprint_prd_path"])

        validation = await analyze_job_completeness(job_content, prd)

        validation_results.append({
            "job_name": job["name"],
            "gaps": validation["gaps"],
            "missing_components": validation["missing"],
            "story_points": validation["story_points"]
        })

    return {
        "job_validation_results": validation_results,
        "phase": "jobs_validated"
    }

async def analyze_job_completeness(job_spec: str, prd: str) -> dict:
    """Analyze job for completeness."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""
Analyze this job specification for completeness:

## Job Specification
{job_spec}

## Sprint PRD (for context)
{prd}

Check for:
1. All acceptance criteria covered
2. Clear file lists
3. Dependency identification
4. Story point accuracy

Return structured analysis.
"""

    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    return parse_job_analysis(response.content[0].text)

def should_apply_job_feedback(state: SprintWorkflowState) -> str:
    """Decision function for job validation feedback loop."""
    validation_results = state.get("job_validation_results", [])
    retry_count = state.get("job_validation_retry_count", 0)

    # Max retries
    if retry_count >= 2:
        return "approved"

    # Check for critical gaps
    has_critical_gaps = any(
        len(v.get("gaps", [])) > 0
        for v in validation_results
    )

    if has_critical_gaps:
        return "apply_feedback"
    else:
        return "approved"

async def update_jobs_from_feedback(state: SprintWorkflowState) -> dict:
    """Apply validation feedback to jobs."""
    # Merge validation recommendations back into job specs
    # Re-generate task files with improvements
    # Increment retry count

    return {
        "job_validation_retry_count": state.get("job_validation_retry_count", 0) + 1,
        "phase": "job_feedback_applied"
    }
```

## Success Criteria
- Job validation node implemented
- Gap analysis runs per job
- Validation results in state
- Feedback loop working
- Max retries enforced
- Story points calculated
- Unit tests passing
- Integration with job creation tested

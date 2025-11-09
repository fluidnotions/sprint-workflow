# Job: Job Creation & PRD Generation

## Overview
Generate Sprint PRD from validated planning outputs, create jobs with code co-location analysis, validate jobs with gap analysis, and set up git worktrees for parallel development. This job bridges planning and execution phases.

## Story Points
13

## Todos from Sprint
### PRD Generation Node
- [ ] Create langgraph/nodes/artifacts.py module
- [ ] Implement generate_sprint_prd() node function
- [ ] Synthesize PM + UX + Engineering + Gap Analysis into PRD
- [ ] Write PRD to thoughts/sprint-plans/{project}/ directory
- [ ] Generate todos from PRD user stories
- [ ] Add sprint_prd_path and todos_path to state schema

### Job Creator Node
- [ ] Create langgraph/nodes/jobs.py module
- [ ] Extract job creator prompt from agents/job-creator.md
- [ ] Implement create_jobs() node function
- [ ] Analyze code co-location for todo grouping
- [ ] Generate task files in tasks/ directory
- [ ] Add jobs list to state schema
- [ ] Write unit tests for job creation

### Job Validation Node
- [ ] Implement validate_jobs() node function
- [ ] Run gap analysis on each job specification
- [ ] Identify missing components per job
- [ ] Calculate story points per job
- [ ] Add job validation results to state
- [ ] Write unit tests for job validation

### Job Feedback Loop
- [ ] Implement should_apply_job_feedback() decision function
- [ ] Implement update_jobs_from_feedback() node function
- [ ] Add conditional edge for job validation loop
- [ ] Test job feedback loop with simulated issues
- [ ] Test max retry escape condition

### Worktree Setup Node
- [ ] Implement setup_git_worktrees() node function
- [ ] Create git branches for each job
- [ ] Set up worktrees in worktrees/ directory
- [ ] Detect repository roots for each worktree
- [ ] Copy environment files to worktrees
- [ ] Test worktree setup with multi-repo scenarios

## Implementation Plan
1. **Create artifacts.py module** - Set up PRD and artifact generation
2. **Implement PRD generation** - Synthesize all planning outputs into structured PRD
3. **Generate todos from PRD** - Extract user stories as todo checklist
4. **Create jobs.py module** - Set up job creation and validation
5. **Extract job creator prompt** - Read agents/job-creator.md
6. **Implement code co-location analysis** - Group todos by file/directory proximity
7. **Generate task files** - Write job specifications to tasks/ directory
8. **Implement job validation** - Run gap analysis on each job
9. **Implement job feedback loop** - Apply validation recommendations to jobs
10. **Implement worktree setup** - Create git branches and worktrees for parallel execution
11. **Update state schema** - Add PRD, todos, jobs, worktrees fields
12. **Write tests** - Test PRD generation, job creation, validation, worktree setup

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/artifacts.py (new - PRD generation)
- sprint-workflow/langgraph/nodes/jobs.py (new - job creation and validation)
- sprint-workflow/langgraph/state.py (modify - add PRD, jobs, worktrees fields)
- sprint-workflow/langgraph/workflow.py (modify - connect job creation nodes)
- sprint-workflow/agents/job-creator.md (read - extract prompt)
- sprint-workflow/tests/langgraph/test_artifacts_nodes.py (new)
- sprint-workflow/tests/langgraph/test_jobs_nodes.py (new)

## Success Criteria
- All todos complete
- Job creator node analyzes code co-location
- Task files generated for each job
- Job validation node performs gap analysis per job
- Worktree setup node creates git worktrees
- Multi-repo scenarios tested
- Job creation testable end-to-end
- PRD generated from planning outputs
- Todos extracted from user stories
- Job feedback loop working

## Dependencies
- Depends on: Job 3 (Gap Analysis) - requires validated planning outputs
- Required by: Job 5-6 (Implementation) - jobs and worktrees needed for parallel execution

## Technical Notes
### PRD Generation Pattern
```python
async def generate_sprint_prd(state: SprintWorkflowState) -> dict:
    """Generate Sprint PRD from validated planning outputs."""
    prd_content = synthesize_prd(
        pm_output=state["pm_output"],
        ux_output=state["ux_output"],
        engineering_output=state["engineering_output"],
        gap_analysis=state["gap_analysis_output"]
    )

    # Write PRD
    project = state["project_name"]
    timestamp = datetime.now().strftime("%Y-%m-%d")
    prd_path = f"thoughts/sprint-plans/{project}/{timestamp}_prd_{state['sprint_theme']}.md"

    write_file(prd_path, prd_content)

    # Generate todos from user stories
    todos = extract_todos_from_prd(prd_content)
    todos_path = f"{timestamp}_{state['sprint_theme']}_todos.md"
    write_file(todos_path, todos)

    return {
        "sprint_prd_path": prd_path,
        "todos_path": todos_path,
        "phase": "prd_generated"
    }
```

### Code Co-location Analysis
```python
async def create_jobs(state: SprintWorkflowState) -> dict:
    """Analyze code co-location and create job groups."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Read todos and PRD
    todos = read_file(state["todos_path"])
    prd = read_file(state["sprint_prd_path"])

    # Analyze codebase structure
    codebase_structure = analyze_directory_structure()

    prompt = load_job_creator_prompt()
    context = f"Todos:\n{todos}\n\nPRD:\n{prd}\n\nCodebase:\n{codebase_structure}"

    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=8000
    )

    jobs = parse_job_specifications(response.content[0].text)

    # Write task files
    for job in jobs:
        task_path = f"tasks/{timestamp}_{job['name']}.md"
        write_file(task_path, job["content"])

    return {
        "jobs": jobs,
        "phase": "jobs_created"
    }
```

### Job Validation Strategy
- Run gap analysis on each job specification
- Check for:
  - Missing acceptance criteria
  - Unclear dependencies
  - Incomplete file lists
  - Story point accuracy
- Generate validation report per job
- Apply feedback loop (max 3 iterations)

### Worktree Setup Pattern
```python
async def setup_git_worktrees(state: SprintWorkflowState) -> dict:
    """Create git worktrees for parallel job execution."""
    worktrees = []

    for job in state["jobs"]:
        branch_name = f"feat/{job['name']}"
        worktree_path = f"worktrees/{branch_name}"

        # Create branch
        run_command(f"git branch {branch_name}")

        # Create worktree
        run_command(f"git worktree add {worktree_path} {branch_name}")

        # Detect repo root
        repo_info = detect_repo_info(worktree_path)

        # Copy environment files
        copy_env_files(worktree_path, repo_info)

        worktrees.append({
            "job_name": job["name"],
            "branch": branch_name,
            "path": worktree_path,
            "repo_info": repo_info
        })

    return {
        "worktrees": worktrees,
        "phase": "worktrees_ready"
    }
```

### Multi-Repo Support
- Detect multiple repository roots in worktree
- Create separate branches per repo
- Track repo boundaries in JobSpec
- Handle environment file copying per repo

### Testing Strategy
- Mock PRD synthesis with sample planning outputs
- Test todo extraction from various PRD formats
- Mock job creator agent for deterministic tests
- Test code co-location grouping logic
- Verify worktree creation and cleanup
- Test multi-repo scenarios

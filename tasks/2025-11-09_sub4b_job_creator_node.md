# Sub-Task 4B: Job Creator Node with Code Co-location

## Parent Job
Week 4: Job Creation & PRD Generation

## Story Points
5

## Scope
Analyze code co-location and create job groups from todos and PRD. This is the core job creation logic.

## Can Run in Parallel
PARTIALLY - Can start in parallel with 4A, but needs PRD output to complete

## Todos
- [ ] Create langgraph/nodes/jobs.py module
- [ ] Extract job creator prompt from agents/job-creator.md
- [ ] Implement create_jobs() node function
- [ ] Analyze code co-location for todo grouping
- [ ] Implement analyze_directory_structure() helper
- [ ] Generate task files in tasks/ directory
- [ ] Add jobs list to state schema
- [ ] Write unit tests for job creation
- [ ] Test code co-location grouping logic

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/jobs.py (new)
- sprint-workflow/langgraph/state.py (modify - add jobs field)
- sprint-workflow/tests/langgraph/test_jobs_nodes.py (new)
- sprint-workflow/agents/job-creator.md (read)

## Dependencies
- Sub-task 4A (needs PRD and todos paths)

## Blocks
- Sub-task 4C (validation needs job specs)
- Sub-task 4D (worktree setup needs jobs)

## Implementation Notes
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
    context = f"""
## Todos
{todos}

## Sprint PRD
{prd}

## Codebase Structure
{codebase_structure}

Analyze the todos and group them by code co-location (files/directories that will be modified together).
Create job specifications with clear boundaries to minimize merge conflicts.
"""

    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=8000
    )

    jobs = parse_job_specifications(response.content[0].text)

    # Write task files
    timestamp = datetime.now().strftime("%Y-%m-%d")
    for job in jobs:
        task_path = f"tasks/{timestamp}_{job['name']}.md"
        write_file(task_path, job["content"])
        job["task_file"] = task_path

    return {
        "jobs": jobs,
        "phase": "jobs_created"
    }

def analyze_directory_structure() -> str:
    """Analyze codebase for co-location analysis."""
    # Run tree command or similar
    result = subprocess.run(
        ["tree", "-L", "3", "-d"],
        capture_output=True,
        text=True
    )
    return result.stdout

def parse_job_specifications(text: str) -> list:
    """Parse job creator output into structured job specs."""
    # Extract job specifications from agent response
    jobs = []
    # Parse markdown sections into job dicts
    # Each job has: name, description, todos, files, story_points
    return jobs
```

## Success Criteria
- Job creator node implemented
- Code co-location analysis working
- Task files generated for each job
- jobs list in state schema
- Unit tests passing
- Grouping logic validated with sample todos
- Integration with PRD working

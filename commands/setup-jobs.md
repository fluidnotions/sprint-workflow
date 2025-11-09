---
description: Organize sprint tasks by code co-location and set up parallel development
allowed-tools: Read, Write, Edit, Bash, Task
argument-hint: "[todo-file] [--pool=N]"
---

# Setup Jobs

Transform conceptually organized todos into code-colocated jobs with git worktrees for parallel execution.

## Arguments

- `todo-file`: Path to todos (default: most recent `*_todos.md`)
- `--pool=N`: Number of parallel agents (default: 3, max: 10)

## Terminology

**Important**: This command transforms **todos** into **jobs**. See key definitions:
- **Todo**: Single checklist item from sprint plan (atomic unit of work)
- **Job**: Code-colocated grouping of related todos that modify the same codebase areas
- **Task**: The resulting specification file for a job (stored in `tasks/`)

Example: 10 todos from a sprint plan might become 3 jobs:
- Job 1: "auth-system" (5 todos related to authentication)
- Job 2: "api-endpoints" (3 todos for API changes)  
- Job 3: "frontend-dashboard" (2 todos for UI changes)

Each job gets its own git worktree for parallel development.

## Step 1: Read Sprint Artifacts

Load both the todo list AND the Sprint PRD for complete context:

**Todo List:**
```bash
ls -t *_todos.md | head -1
```

**Sprint PRD:**
```bash
PROJECT_NAME=$(basename "$PWD")
ls -t thoughts/sprint-plans/$PROJECT_NAME/*_prd_*.md | head -1
```

**Why both?**
- **Todos**: Task checklist (what needs to be done)
- **Sprint PRD**: Architecture, acceptance criteria, user stories, technical approach (how and why)

The job-creator agent needs BOTH to create well-defined job specifications that implementation agents can execute without ambiguity.

## Step 2: Invoke Job Creator Agent

Use the job-creator agent to analyze code co-location and group todos into jobs:

```
Task: job-creator
Input:
  - Todo list: {todos_file}
  - Sprint PRD: {prd_file}

Analyze:
  - Which todos modify the same codebase areas?
  - What's the natural grouping by code co-location?
  - Database migrations together
  - API endpoints together
  - Frontend components together
  - Configuration changes together

Output: Job groupings with specifications
```

The agent will use the Sprint PRD to understand:
- Architecture and technical approach
- Acceptance criteria for each feature
- Dependencies between components
- Risk areas and complexity

## Step 3: Create Job Specifications

For each job group, the job-creator agent generates a task file:
`tasks/{datetime}_{type}_{groupname}.md`

```markdown
# Job: {groupname}

## Overview
{description of job scope}

## Todos from Sprint
- [ ] Todo item 1 (from original list)
- [ ] Todo item 2
- [ ] Todo item 3

## Implementation Plan
1. Set up {component}
2. Implement {feature}
3. Add tests
4. Update documentation

## Files to Modify
- src/api/{endpoint}.js (new)
- src/models/{model}.js (modify)
- tests/{test}.spec.js (new)

## Success Criteria
- All todos complete
- Tests passing
- No regressions
```

## Step 4: Set Up Git Worktrees

For each job, create isolated development environment:

```bash
# Derive project root (ask if ambiguous)
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# For each job
JOB_NAME="auth-system"  # from groupname
BRANCH_NAME="feat/$JOB_NAME"

# Create branch and worktree
git fetch origin
git checkout -b $BRANCH_NAME origin/main
mkdir -p "$PROJECT_ROOT/worktrees"
git worktree add "$PROJECT_ROOT/worktrees/$BRANCH_NAME" $BRANCH_NAME

# Set up worktree
cd "$PROJECT_ROOT/worktrees/$BRANCH_NAME"
cp ../../.env .env 2>/dev/null || true
echo "Worktree ready at worktrees/$BRANCH_NAME"
```

## Step 5: Architecture Review & Feedback Loop

Before starting implementation, run gap-analyzer on each job specification:

```
Task: gap-analyzer
Input:
  - Job specification: tasks/{datetime}_{type}_{groupname}.md
  - Sprint PRD: {prd_file} (for context)

Validate:
  - Architecture patterns and best practices
  - Security considerations
  - Missing components or edge cases
  - Complexity assessment (story points)

Output: Gap analysis report with recommendations
```

**Critical Feedback Loop:**

1. **If gap-analyzer finds issues:**
   - Present findings to user
   - Ask: "Apply recommended changes to job specification? (yes/no/customize)"

2. **If yes:** Update the job specification file with:
   - Additional todos for missing components
   - Architectural improvements
   - Security hardening steps
   - Updated story point estimate

3. **Document changes:**
   - Add "Gap Analysis Updates" section to job spec
   - List what was added/changed and why
   - Update story point total

4. **Re-validate:** Optionally run gap-analyzer again on updated spec

This ensures job specifications are comprehensive BEFORE implementation begins.

## Step 6: Launch Sprint Coordinator

Spawn the sprint-coordinator agent to orchestrate parallel execution:

```
Task: sprint-coordinator
Input:
  - Job specifications: tasks/*.md
  - Sprint PRD: {prd_file}
  - Worktrees: worktrees/feat-*/
  - Agent pool size: {pool_size}

The coordinator will autonomously:

1. Parallel Implementation
   - Spawn implementation-agent for each job (parallel)
   - Monitor progress in sprint_status.md

2. Verification Feedback Loops (automatic)
   - When job completes → spawn verification-agent
   - If verification fails → spawn implementation-agent with feedback
   - Loop until verified OR max 5 iterations
   - Failed jobs logged to sprint_errors_*.md (sprint continues)

3. Branch Management (multi-repo aware, parallel)
   - Update branches from main
   - Auto-resolve conflicts where possible
   - Run tests before merging

4. Push/PR/Merge Strategy
   - IF repo has remote: push + create PR + auto-merge (if tests pass)
   - IF repo local only: merge to main locally
   - Cleanup merged worktrees

5. Error Handling (non-blocking)
   - Failed jobs logged, user notified
   - Sprint continues regardless of individual failures
   - Final report shows successes and failures

Monitor progress: /sprint-status (updates every 60 seconds)
```

**Note**: The coordinator runs autonomously. You can monitor with `/sprint-status` or review error reports in `sprint_errors_*.md` for any failed jobs.

## Output

```
Job Setup Complete!

📊 Jobs Created: {count}
🌳 Worktrees Set Up: {list}
✅ Architecture Validated
🤖 Sprint Coordinator: Launched

🚀 Parallel implementation started!

The sprint-coordinator is now running autonomously:
- Implementation agents spawned (parallel)
- Verification loops active (automatic)
- Progress tracked in sprint_status.md

Monitor:
- Real-time: `/sprint-status`
- Errors: sprint_errors_*.md
- Final report: Generated when all jobs complete

After sprint:
- Review final report from sprint-coordinator
- Check sprint_errors_*.md for any failed jobs
- Run `/sprint-retrospective` to document learnings
```

## Relationship to Workflow

```
[create-sprint] → [setup-jobs] → [sprint-coordinator (autonomous)] → [retrospective]
   (Sprint PRD)       ↓                      ↓
   (Todos)      [job-creator]     [parallel implementation]
                      ↓                      ↓
                [gap-analyzer]      [verification loops]
                      ↓                      ↓
                [feedback loop]       [branch management]
                      ↓                      ↓
             [updated job specs]      [push/PR/merge]
                                            ↓
                                   [final report + errors]
```

**setup-jobs agents:**
- job-creator: Groups todos into code-colocated jobs using Sprint PRD context
- gap-analyzer: Validates job specs and provides feedback for improvements

**sprint-coordinator spawns:**
- implementation agents (parallel, one per job)
- verification agents (per job, feedback loops)
- branch-manager agents (per repo, parallel)
- conflict-resolution agents (as needed)

**Autonomous execution**: Once setup-jobs completes, the sprint-coordinator runs the entire implementation autonomously with automatic verification, merging, and error handling.

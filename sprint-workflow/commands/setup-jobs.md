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

## Step 1: Read Todo List

Load todos from file or find most recent:
```bash
ls -t *_todos.md | head -1
```

## Step 2: Analyze Code Co-location

Group todos by where code changes cluster:
- Database migrations together
- API endpoints together  
- Frontend components together
- Configuration changes together
- Documentation updates together

## Step 3: Create Job Specifications

For each job group, create task file:
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

## Step 5: Architecture Review

Before starting implementation, run gap-analyzer on each job:

```
Task: gap-analyzer
Review job plan: tasks/{datetime}_{type}_{groupname}.md
Validate: architecture, libraries, patterns
Output: recommendations or approval
```

Present findings and get user approval for any changes.

## Step 6: Launch Parallel Implementation

**Note**: Parallel agent execution is conceptual in this workflow. Actual implementation depends on your Claude Code setup.

For manual execution:
```bash
# For each job, switch to its worktree and begin implementation
for job in jobs; do
  WORKTREE="worktrees/feat-${job}"
  echo "Ready to implement: $job in $WORKTREE"
  echo "Run: cd $WORKTREE && /implement_plan tasks/{datetime}_{type}_{job}.md"
done
```

For automated execution (if configured):
- Each agent receives its task specification
- Agents work independently in separate worktrees
- Progress tracked in sprint_status.md
- Use `/sprint-status` to monitor overall progress

## Step 7: Progress Tracking

Create sprint dashboard at `sprint_status.md`:

```markdown
# Sprint Status

## Jobs
- [>] auth-system (in progress - worktree: feat/auth-system)
- [ ] api-endpoints (queued)
- [ ] frontend-dashboard (queued)

## Progress
- Started: {timestamp}
- Agents active: 3
- Estimated completion: {estimate}
```

## Output

```
Job Setup Complete!

📊 Jobs Created: {count}
🌳 Worktrees Set Up: {list}
✅ Architecture Validated
🤖 Agent Pool Size: {pool}

Starting parallel implementation...

Next steps:
- Monitor progress with `/sprint-status`
- After completion: Use `/verify_implementation` for each completed task
- For PR creation: Use `/describe_pr` for each task branch
```

## Post-Implementation (Step 8-11)

After all jobs complete:

### Step 8: Merge and Create PRs
- Pull origin/main into each worktree
- Resolve any conflicts
- Push branches to origin
- Create GitHub PRs with traceability

### Step 9: Sprint Retrospective
Generate `{datetime}_sprint_retro.md`:
- Tasks completed vs planned
- Time estimates vs actual
- Issues encountered
- Improvements for next sprint

### Step 10: Unit Test Generation
Spawn test-automator agents:
- Create comprehensive test suites
- Achieve 80%+ coverage on critical paths
- Run tests until all pass

### Step 11: Final Validation
- All tests passing
- Documentation complete
- PRs merged to main
- Retrospective documented

## Relationship to Workflow

```
[create-sprint] → [setup-jobs] → [parallel implementation] → [verify_implementation]
                      ↓
              [job-creator agent]
              [gap-analyzer agent]
              [implementation agents]
```

This command orchestrates the entire sprint execution with parallel development.

# Sprint Workflow Plugin

Sprint planning, organization, tracking, and retrospectives with parallel development via git worktrees.

## Single Responsibility

This plugin does **ONE thing**: manages sprints from planning to completion.

**What it does:**
- Creates comprehensive sprint plans with multi-agent PRD
- Organizes todos into code-colocated jobs
- Sets up git worktrees for parallel development
- Tracks sprint progress in real-time
- Generates retrospectives with metrics

**What it does NOT do:**
- Implementation (use `implementation-workflow` plugin)
- Codebase research (use `codebase-research` plugin)
- Debugging or general dev support

## Installation

```bash
/plugin install sprint-workflow
```

## Commands (4)

### `/create-sprint` - Initialize Sprint

Creates comprehensive sprint plan with PRD, todos, and architecture validation.

**Usage:**
```bash
/create-sprint "User Authentication Sprint"
```

**What it does:**
1. Spawns parallel agents (PM, UX, Engineering) for PRD
2. Generates sprint plan in `thoughts/shared/plans/`
3. Creates phased todo list
4. Validates architecture
5. Sets up directory structure

**Output:**
- Sprint plan: `thoughts/shared/plans/{datetime}_sprint_{name}.md`
- Todo list: `{datetime}_todos.md`
- Architecture validation report

**Next:** Run `/setup-jobs`

---

### `/setup-jobs` - Organize & Setup Worktrees

Transforms todos into code-colocated jobs with git worktrees.

**Usage:**
```bash
/setup-jobs                    # Uses most recent todos
/setup-jobs sprint_todos.md    # Specific file
/setup-jobs --pool=5           # Custom pool size
```

**What it does:**
1. Analyzes todos for code co-location
2. Groups related todos into jobs
3. Creates job specs in `tasks/`
4. Sets up git worktrees
5. Validates architecture per job

**Example:**
```
10 todos → 3 jobs:
- auth-system (5 todos) → worktrees/feat-auth-system
- api-endpoints (3 todos) → worktrees/feat-api-endpoints
- frontend-ui (2 todos) → worktrees/feat-frontend-ui
```

**Next:** Implement each job (see `implementation-workflow` plugin)

---

### `/sprint-status` - Monitor Progress

Real-time sprint dashboard.

**Usage:**
```bash
/sprint-status
```

**Shows:**
- Sprint progress bars (tasks, todos)
- Active jobs with worktrees
- Recent activity
- Blockers
- Next milestones

Run anytime during sprint.

---

### `/sprint-retrospective` - Document Learnings

Generates comprehensive retrospective.

**Usage:**
```bash
/sprint-retrospective
```

**Generates:**
- Delivery metrics (planned vs actual)
- Code metrics (LOC, commits, PRs)
- Quality metrics (coverage, bugs)
- Timeline breakdown
- What went well / challenges
- Lessons learned
- Improvements for next sprint

**Output:** `{datetime}_sprint_retro.md`

---

## Included Agents (5)

**Planning Agents (Opus):**
- `product-manager` - User stories & acceptance criteria
- `ux-designer` - User flows & UI specifications
- `senior-engineer` - Technical architecture
- `gap-analyzer` - Architecture validation

**Execution Agent:**
- `job-creator` (Sonnet) - Code co-location analysis

All agents auto-invoked by commands.

---

## Complete Sprint Workflow

### 1. (Optional) Research First
```bash
/research_codebase "authentication"  # codebase-research plugin
```

### 2. Create Sprint
```bash
/create-sprint "Auth Sprint"
```

### 3. Organize Jobs
```bash
/setup-jobs
```
Creates job specs + worktrees.

### 4. Implement Jobs
```bash
cd worktrees/feat-auth-system
/implement_plan tasks/sprint_auth-system.md  # implementation-workflow plugin
/verify_implementation                        # implementation-workflow plugin
/commit                                       # implementation-workflow plugin
/describe_pr                                  # implementation-workflow plugin
```

### 5. Monitor
```bash
/sprint-status  # Run anytime
```

### 6. Complete
```bash
/sprint-retrospective  # After all PRs merged
```

---

## Directory Structure

```
your-project/
├── thoughts/shared/
│   ├── plans/          # Sprint plans
│   └── research/       # Research (from codebase-research plugin)
├── tasks/              # Job specifications
├── worktrees/          # Git worktrees (one per job)
│   ├── feat-auth/
│   ├── feat-api/
│   └── feat-ui/
├── *_todos.md          # Sprint todos
├── sprint_status.md    # Live dashboard
└── *_sprint_retro.md  # Retrospectives
```

Auto-created by session hook.

---

## Key Concepts

**Todo vs Job vs Task:**
- **Todo**: Single checklist item
- **Job**: Code-colocated group of todos
- **Task**: Job specification file in `tasks/`

**Code Co-location:**
Groups todos by where code changes occur:
- Database migrations → together
- API endpoints → together
- Frontend components → together

Minimizes merge conflicts, enables parallel work.

**Git Worktrees:**
Each job gets isolated directory:
- No branch switching
- Multiple jobs simultaneously
- No conflicts during development

---

## Best Practices

1. **Right-size sprints:** 3-10 jobs, 2-5 todos/job, 1-2 weeks
2. **Meaningful names:** "oauth-integration" not "task-1"
3. **Monitor regularly:** `/sprint-status` daily
4. **Always retrospective:** Even failed sprints have learnings

---

## Recommended Companion Plugins

- **implementation-workflow**: For implementing jobs
- **codebase-research**: For pre-sprint research

---

## Requirements

- Claude Code >=1.0.0
- Git >=2.0.0 with worktree support
- Bash

---

## License

MIT License

---

**Start sprinting:** `/create-sprint "Your Sprint Name"`

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

## Commands (5)

### `/plan-sprint` - Interactive Sprint Planning

Conversational sprint planning to create a Sprint Brief.

**Usage:**
```bash
/plan-sprint
```

**What it does:**
1. Guides you through interactive planning conversation
2. Auto-estimates story points based on complexity
3. Iteratively refines scope and priorities
4. Creates Sprint Brief document

**Output:**
- Sprint Brief: `thoughts/sprint-plans/{project_name}/{datetime}_brief_{name}.md`

**Next:** Run `/create-sprint`

---

### `/create-sprint` - Generate Sprint PRD

Creates comprehensive Sprint PRD with multi-agent analysis, todos, and architecture validation.

**Usage:**
```bash
/create-sprint "User Authentication Sprint"
```

**What it does:**
1. Spawns parallel agents (PM, UX, Engineering) for comprehensive PRD
2. Generates Sprint PRD in `thoughts/sprint-plans/{project_name}/`
3. Creates phased todo list
4. Validates architecture
5. Sets up directory structure

**Output:**
- Sprint PRD: `thoughts/sprint-plans/{project_name}/{datetime}_prd_{name}.md`
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

## Included Agents (6)

**Planning Agents (Opus):**
- `product-manager` - User stories & acceptance criteria
- `ux-designer` - User flows & UI specifications
- `senior-engineer` - Technical architecture
- `gap-analyzer` - Architecture validation

**Organization Agent:**
- `job-creator` (Sonnet) - Code co-location analysis

**Orchestration Agent:**
- `sprint-coordinator` (Opus) - Parallel implementation, verification loops, multi-repo management

All agents auto-invoked by commands.

---

## Complete Sprint Workflow

### 1. (Optional) Research First
```bash
/research_codebase "authentication"  # codebase-research plugin
```

### 2. (Optional) Plan Sprint
```bash
/plan-sprint
```
Interactive planning conversation → creates Sprint Brief.

### 3. Create Sprint PRD
```bash
/create-sprint "Auth Sprint"
```
Multi-agent PRD generation → creates Sprint PRD and todos.

### 4. Setup Jobs & Launch Sprint
```bash
/setup-jobs
```
Creates job specs + worktrees + launches sprint-coordinator.

**The sprint-coordinator autonomously:**
- Spawns implementation agents (parallel, one per job)
- Runs verification feedback loops (automatic)
- Manages branches across multiple repos
- Auto-merges PRs when tests pass
- Logs errors but continues sprint (non-blocking)

### 5. Monitor (During Autonomous Execution)
```bash
/sprint-status  # Real-time dashboard (updates every 60s)
```

Check `sprint_errors_*.md` for any job failures (sprint continues anyway).

### 6. Review & Retrospective (After Sprint Completes)
```bash
# Sprint-coordinator generates final report automatically
# Review it and any error reports

/sprint-retrospective  # Document learnings
```

---

## Directory Structure

```
your-project/
├── thoughts/
│   ├── sprint-plans/
│   │   └── your-project/     # All sprint artifacts (by project)
│   │       ├── {datetime}_brief_{name}.md   # Sprint Brief (from /plan-sprint)
│   │       └── {datetime}_prd_{name}.md     # Sprint PRD (from /create-sprint)
│   └── shared/
│       └── research/          # Research (from codebase-research plugin)
├── tasks/                     # Job specifications
├── worktrees/                 # Git worktrees (one per job)
│   ├── feat-auth/
│   ├── feat-api/
│   └── feat-ui/
├── *_todos.md                 # Sprint todos
├── sprint_status.md           # Live dashboard
└── *_sprint_retro.md         # Retrospectives
```

Auto-created by session hook with project-specific subdirectories.

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

1. **Right-size sprints:** 3-10 jobs, 2-5 todos/job, 20-40 story points
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

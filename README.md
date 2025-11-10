# Sprint Workflow Plugin

Manages sprints from planning to completion with parallel development via git worktrees.

**Architecture:**

**Phase 1: Planning (Claude Code Commands)**
- `/plan-sprint` - Interactive planning conversation → Sprint Brief
- `/create-sprint` - Multi-agent PRD generation → PRD + todos

**Phase 2: Execution (LangGraph State Machine)**
- Takes PRD + todos as input
- Handles gap analysis iteration, job creation, worktree setup, implementation, verification, and merging
- Deterministic, resumable execution via state machine
- **Why LangGraph?** The execution phase is too complex for prompt-based orchestration to handle reliably

### Workflow Diagram

The complete LangGraph state machine workflow:

![Sprint Workflow Diagram](docs/workflow-diagram.png)

**Key Features:**
- **Parallel planning** - PM, UX, Engineering agents run simultaneously from START
- **Feedback loops** - Gap analysis and job validation with max 3 retries each
- **Verification loop** - Retry failed jobs until all verified or failed
- **Conditional routing** - Dotted lines show decision points (approved/apply_feedback/retry)

## Installation

**Install LangGraph dependencies:**
```bash
bash scripts/install_langgraph.sh
export ANTHROPIC_API_KEY="your-api-key"
```

See [LANGGRAPH.md](LANGGRAPH.md) for details on the LangGraph execution engine.

## Commands

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

Creates comprehensive Sprint PRD with multi-agent analysis and todos. This is the **handoff point** from Claude Code to LangGraph.

**Usage:**
```bash
/create-sprint "User Authentication Sprint"
```

**What it does:**
1. Spawns parallel agents (PM, UX, Engineering) for comprehensive PRD
2. Generates Sprint PRD in `thoughts/sprint-plans/{project_name}/`
3. Creates phased todo list
4. **Hands off to LangGraph** with PRD + todos

**Output:**
- Sprint PRD: `thoughts/sprint-plans/{project_name}/{datetime}_prd_{name}.md`
- Todo list: `{datetime}_todos.md`

**Next:** LangGraph automatically executes the sprint (gap analysis → jobs → implementation → merge)

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

**Execution (LangGraph State Machine):**
- Gap analysis, job creation, implementation, verification handled by LangGraph nodes
- Uses `job-creator` agent (Sonnet) for code co-location analysis
- Deterministic execution with feedback loops and retry logic

Planning agents auto-invoked by commands. Execution handled by LangGraph.

---

## Complete Sprint Workflow

### 1. Plan Sprint
```bash
/plan-sprint  # Optional: Interactive planning conversation → Sprint Brief
```

### 2. Create Sprint PRD & Execute
```bash
/create-sprint "Auth Sprint"
```
Multi-agent PRD generation → creates Sprint PRD and todos → **hands off to LangGraph**.

**LangGraph automatically executes:**
- Gap analysis iteration (architecture validation with feedback loops)
- Code co-location analysis and job creation
- Git worktree setup (one per job)
- Parallel implementation (up to pool_size jobs simultaneously)
- Verification loops (retry up to 5 times per job)
- Branch management and conflict resolution
- PR creation and auto-merge
- Final execution report

**Non-blocking errors:** Failed jobs generate error reports but don't stop the sprint.

### 3. Monitor (During Execution)
```bash
/sprint-status  # Real-time dashboard
```

Check `sprint_status.md` for live updates and `sprint_errors_*.md` for failures.

### 4. Review & Retrospective (After Completion)
```bash
# LangGraph generates final report automatically
# Review sprint_report_*.md and any error reports

/sprint-retrospective  # Document learnings
```

---

## Directory Structure

The plugin creates the following directories during sprint execution:

```
your-project/
├── tasks/                     # Job specifications
├── worktrees/                 # Git worktrees (one per job)
│   ├── feat-auth/
│   ├── feat-api/
│   └── feat-ui/
├── *_todos.md                 # Sprint todos
├── sprint_status.md           # Live dashboard
└── *_sprint_retro.md         # Retrospectives
```

**Note:** Sprint planning artifacts (PRDs, briefs) are stored in a shared directory structure managed by a separate local plugin. This allows sprint documentation to be shared across multiple projects.

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

## Requirements

- Python 3.9+ with LangGraph dependencies

---

## Repository Structure

```
sprint-workflow/
├── agents/                  # Specialized agents (PM, UX, Engineer, etc.)
├── commands/                # Slash commands (/create-sprint, /setup-jobs, etc.)
├── hooks/                   # Session initialization hooks
├── mcp-servers/             # LangGraph sprint executor (optional)
├── scripts/                 # Setup and utility scripts
├── tests/                   # Test suite
├── tasks/                   # Example job specifications
├── graph/                   # LangGraph workflow definitions
├── plugin.json              # Plugin manifest
├── README.md                # This file
├── LANGGRAPH.md             # LangGraph integration documentation
└── 2025-11-09_langgraph_migration_todos.md  # Migration notes
```

---

## Additional Documentation

- **[LANGGRAPH.md](LANGGRAPH.md)** - LangGraph execution engine details
- **[docs/DIAGRAMS.md](docs/DIAGRAMS.md)** - Workflow diagram documentation

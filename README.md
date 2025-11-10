# Sprint Workflow

**Automated sprint execution with deterministic state machines.**

Transform a sprint theme into deployed code through parallel job execution, automatic verification, and merge orchestration—all managed by a LangGraph state machine that guarantees correct execution order and handles failures gracefully.

## The Problem

Sprint execution involves complex workflows: multi-perspective planning, architecture validation with feedback loops, job creation with code co-location analysis, parallel implementation, verification retries, and coordinated merging. Prompt-based orchestration fails at this complexity—agents skip steps, ignore feedback, or get stuck in loops.

## The Solution

![Workflow Diagram](docs/workflow-diagram.png)

LangGraph state machines provide:
- **Deterministic execution** - Every phase runs in the correct order
- **Guaranteed feedback loops** - Gap analysis and job validation with enforced retry limits
- **True parallelization** - Multiple jobs execute simultaneously in isolated git worktrees
- **Automatic recovery** - Resume from any point after crashes
- **Non-blocking failures** - Failed jobs don't stop the sprint

## How It Works

```bash
# 1. Define your sprint
/create-sprint "User Authentication"

# 2. LangGraph executes everything:
#    ✓ Parallel planning (PM, UX, Engineering perspectives)
#    ✓ Architecture gap analysis with feedback loops
#    ✓ Code co-location analysis and job creation
#    ✓ Git worktree setup for parallel development
#    ✓ Concurrent job implementation
#    ✓ Verification with automatic retries
#    ✓ Branch management and PR creation

# 3. Monitor progress
/sprint-status

# 4. Review results
/sprint-retrospective
```

## Quick Start

```bash
# Install dependencies
bash scripts/install_langgraph.sh
export ANTHROPIC_API_KEY="your-api-key"

# Run your first sprint
/create-sprint "API Rate Limiting"
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-agent planning** | PM, UX, and Engineering agents analyze requirements in parallel |
| **Gap analysis** | Validates architecture completeness with up to 3 feedback iterations |
| **Code co-location** | Groups related changes to minimize merge conflicts |
| **Parallel execution** | Runs multiple jobs simultaneously in isolated worktrees |
| **Verification loops** | Automatically retries failed jobs up to 5 times |
| **Non-blocking errors** | Continues sprint even when individual jobs fail |

## Commands

- `/plan-sprint` - Interactive planning session (optional pre-planning)
- `/create-sprint` - Launch sprint execution with LangGraph
- `/sprint-status` - Real-time progress dashboard
- `/sprint-retrospective` - Post-sprint metrics and analysis

## Architecture

The workflow is a single LangGraph state machine that handles the entire sprint lifecycle:

1. **Planning** - Parallel PM/UX/Engineering analysis
2. **Synthesis** - Combines perspectives into unified plan
3. **Gap Analysis** - Validates architecture (max 3 retry loops)
4. **Job Creation** - Analyzes code co-location and creates job specs
5. **Validation** - Ensures job specifications are sound (max 3 retry loops)
6. **Implementation** - Executes jobs in parallel worktrees
7. **Verification** - Tests and validates each job (max 5 retries per job)
8. **Integration** - Manages branches, creates PRs, and merges

See [LANGGRAPH.md](LANGGRAPH.md) for technical details, state schemas, and debugging tools.

## Documentation

- [LANGGRAPH.md](LANGGRAPH.md) - State machine architecture and technical reference
- [CLAUDE.md](CLAUDE.md) - Developer guide for contributing
- [docs/DIAGRAMS.md](docs/DIAGRAMS.md) - Workflow visualization

## Requirements

Python 3.9+ with LangGraph dependencies
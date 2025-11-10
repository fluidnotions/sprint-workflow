# LangGraph Sprint Executor

LangGraph is the **core execution engine** for sprint workflow. After `/create-sprint` generates the PRD and todos, LangGraph takes over to handle the entire execution phase.

## Why LangGraph?

Sprint execution (gap analysis → job creation → implementation → merge) is **too complex for prompt-based orchestration** to handle reliably. LangGraph provides:

✅ **Deterministic execution** - State machine guarantees correct phase ordering
✅ **Resumability** - Can resume from any point if crash/interruption
✅ **Explicit feedback loops** - Gap analysis and job validation loops guaranteed (max 3 retries each)
✅ **Verification retry loops** - Automatic retry up to 5 times per failed job
✅ **State inspection** - Can inspect workflow state at any node
✅ **Visualization** - Generate workflow diagrams
✅ **Better debugging** - See exactly where failures occur
✅ **Non-blocking errors** - Failed jobs generate reports but don't stop the sprint

## Architecture

### Workflow Overview

![Workflow Diagram](docs/workflow-diagram.png)

**Two-phase execution:**

1. **Planning Phase** - `/create-sprint` invokes parallel agents (PM, UX, Engineering) to generate comprehensive PRD and todos
2. **Execution Phase** - LangGraph state machine takes PRD + todos and executes the complete workflow with feedback loops and retry logic

**Key workflow features:**
- **Parallel planning** - PM, UX, Engineering nodes execute simultaneously from START
- **Gap analysis loop** - Validates architecture with up to 3 retry iterations
- **Job validation loop** - Ensures job specifications are sound with up to 3 retries
- **Verification loop** - Retries failed jobs up to 5 times each
- **Conditional routing** - Dotted edges in diagram show decision points

### State Structure

```python
class SprintState:
    # Input
    project_name: str
    sprint_prd_path: str
    todos_path: str
    pool_size: int

    # Jobs
    jobs: List[JobSpec]  # Full job specifications

    # Execution state
    phase: "init" | "implementing" | "verifying" | ...

    # Progress tracking
    jobs_verified: List[str]
    jobs_failed: List[str]

    # Error tracking
    errors: List[Dict]
```

## Installation

### 1. Install Python Dependencies

```bash
# Using the provided script
bash scripts/install_langgraph.sh

# Or manually
pip install --user langgraph langchain-anthropic
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 3. Enable MCP Server

The LangGraph executor is registered as an MCP server in `plugin.json`:

```json
{
  "mcpServers": {
    "langgraph-sprint-executor": {
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/langgraph_sprint_executor.py"]
    }
  }
}
```

## Usage

### Automatic Invocation (Default)

LangGraph is automatically invoked by `/create-sprint` after PRD and todos are generated:

```bash
/create-sprint "Auth Sprint"
# → Generates PRD + todos
# → Automatically invokes LangGraph MCP server
# → Sprint execution begins
```

### Manual Invocation (If Needed)

If you need to manually trigger LangGraph execution:

```bash
# Use the MCP tool directly
mcp__langgraph-sprint-executor__execute_sprint(
  project_name="my-project",
  sprint_prd_path="thoughts/sprint-plans/my-project/*_prd_*.md",
  todos_path="*_todos.md",
  pool_size=3
)
```

### Direct Python Execution (Advanced)

```bash
cd /path/to/project

python3 ~/.claude/plugins/local-dev/sprint-workflow/mcp-servers/langgraph_sprint_executor.py \
  --mode direct \
  --project my-project \
  --prd thoughts/sprint-plans/my-project/*_prd_*.md \
  --todos *_todos.md \
  --pool 3
```

## Features

### ✅ Parallel Execution

Jobs are executed truly in parallel (up to `pool_size`):

```python
async def spawn_implementation_agents(state: SprintState):
    # Batched parallel execution
    for batch in batched(pending_jobs, state['pool_size']):
        await asyncio.gather(*[
            implement_job(job) for job in batch
        ])
```

### ✅ Automatic Verification Loops

```python
def should_retry_or_continue(state: SprintState) -> "retry" | "continue":
    has_implementing = any(j['status'] == 'implementing' for j in state['jobs'])
    has_pending = any(j['status'] == 'pending' for j in state['jobs'])

    if has_implementing or has_pending:
        return "retry"  # Loop back to verify
    else:
        return "continue"  # Move to branch management
```

### ✅ State Persistence & Resumability

```python
# Checkpointing built-in
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Can resume from crash
config = {"configurable": {"thread_id": "sprint-my-project"}}
final_state = await app.ainvoke(initial_state, config)

# If crashes, just re-run with same thread_id
# It will resume from last checkpoint!
```

### ✅ Multi-Repo Awareness

```python
async def push_and_merge(state: SprintState):
    for repo in state['repos']:
        if repo['has_remote']:
            # Push + create PR + auto-merge
            await push_branch(job['branch'])
            await create_pr(job)
            await merge_pr(job)
        else:
            # Merge locally
            await merge_local(job['branch'])
```

### ✅ Non-Blocking Error Handling

```python
# Job fails verification after 5 retries
if job['retry_count'] >= 5:
    job['status'] = 'failed'
    error_file = write_error_report(job, details)
    state['errors'].append({'job': job['name'], 'report': error_file})

    # Notify user but DON'T pause sprint
    print(f"⚠️  Job failed: {job['name']}")
    print(f"📄 Error report: {error_file}")
    print("ℹ️  Sprint continues - other jobs proceeding")

    # Other jobs continue!
```

## Output Files

### sprint_status.md (Live Dashboard)

Updated every iteration:

```markdown
# Sprint Status - Live Dashboard
**Last Updated**: 2025-11-03T20:45:32

## Current Phase: VERIFYING

### Jobs Summary
- Total: 5
- Implementing: 2
- Verifying: 1
- Verified: 1
- Failed: 1

### Job Details
[✓] **auth-system** (verified)
[>] **api-endpoints** (verifying)
  - Retries: 2/5
[>] **dashboard-ui** (implementing)
[✗] **complex-feature** (failed)
  - Error: Max verification retries reached
```

### sprint_errors_{timestamp}_{job}.md

Detailed error report for each failed job:

```markdown
# Sprint Error Report: complex-feature

**Status**: failed
**Phase**: Verification
**Iterations Attempted**: 5

## Error Details
Tests failing:
- test_edge_case_1: Expected X, got Y
- test_integration: Connection timeout

## Job Specification
Path: tasks/2025-11-03_feat_complex-feature.md
Worktree: worktrees/feat-complex-feature
Branch: feat-complex-feature

## Next Steps for Manual Resolution
1. Check worktree: cd worktrees/feat-complex-feature
2. Run tests: npm test
3. Fix failures
4. Re-run verification
```

### sprint_report_{timestamp}.md

Final execution report:

```markdown
# Sprint Execution Report

## Overview
- Started: 2025-11-03T19:30:00
- Completed: 2025-11-03T20:45:32
- Total Jobs: 5

## Results
- ✅ Verified Complete: 4
- ⚠️ Failed: 1

### Story Points
- Total Planned: 45 points
- Delivered: 38 points
- Failed: 7 points
- Success Rate: 84%
```

## Visualization

The complete workflow graph is available in the repository:

![Sprint Workflow Diagram](docs/workflow-diagram.png)

Regenerate the diagram after modifying the workflow:

```bash
bash scripts/generate_diagram.sh
```

See [docs/DIAGRAMS.md](docs/DIAGRAMS.md) for more details.

## Debugging

### Inspect State at Any Point

```python
# Get current state
state = app.get_state(config)
print(f"Current phase: {state['phase']}")
print(f"Jobs verified: {state['jobs_verified']}")
print(f"Jobs failed: {state['jobs_failed']}")
```

### View Execution History

```python
# Get all checkpoints
for checkpoint in app.get_state_history(config):
    print(f"Phase: {checkpoint.values['phase']}")
    print(f"Jobs: {len(checkpoint.values['jobs'])}")
```

## Why LangGraph Instead of Agent-Based Orchestration?

Originally, sprint execution was attempted using a `sprint-coordinator` agent with prompt-based orchestration. This proved unreliable for the execution phase due to:

❌ Non-deterministic execution order
❌ No built-in resumability
❌ Fragile file-based state tracking
❌ Difficult to debug when things go wrong
❌ Verification loops not guaranteed
❌ No way to inspect workflow state

**LangGraph solves all of these:**

| Challenge | LangGraph Solution |
|-----------|-------------------|
| Execution reliability | State machine guarantees correct phase ordering |
| Crash recovery | Checkpoint-based resumability |
| Debugging | Direct state graph inspection |
| Feedback loops | Guaranteed by conditional edges (max retries enforced) |
| Parallelization | True async parallelization (not just "prompt says parallel") |
| State tracking | In-memory state (TypedDict) flows through nodes |
| Visualization | Generate workflow diagrams with get_graph().draw_mermaid_png() |
| Error recovery | Explicit error nodes with non-blocking behavior |

**Result:** LangGraph is now the **core execution engine**, not an optional alternative.

## Integration with /create-sprint

`/create-sprint` is the handoff point from Claude Code commands to LangGraph:

**What /create-sprint does:**
1. Spawns parallel agents (PM, UX, Engineering) for PRD generation
2. Synthesizes outputs into comprehensive Sprint PRD
3. Generates phased todo list
4. **Invokes LangGraph MCP server** with PRD + todos

**What LangGraph does (after handoff):**
1. Gap analysis iteration (validates architecture, max 3 retries)
2. Job creation (code co-location analysis)
3. Job validation (validates job specs, max 3 retries)
4. Worktree setup (one per job)
5. Parallel implementation (up to pool_size jobs)
6. Verification loops (retry failed jobs up to 5 times each)
7. Branch management (update from main, resolve conflicts)
8. Push and merge (PR creation and auto-merge)
9. Final report generation

**Note:** `/setup-jobs` command is **deprecated** - LangGraph handles all of this automatically.

## Troubleshooting

### Dependencies not installed
```bash
pip install --user langgraph langchain-anthropic
```

### API key not set
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### MCP server not starting
Check logs in `~/.claude/logs/` for errors

### State not persisting
Ensure `thread_id` is consistent across invocations

## Next Steps

1. Install dependencies: `bash scripts/install_langgraph.sh`
2. Set API key: `export ANTHROPIC_API_KEY="..."`
3. Try it: Run `/setup-jobs` (will use LangGraph if available)
4. Monitor: Check `sprint_status.md` for live updates
5. Debug: Inspect state with Python if needed

## References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)
- [Checkpointing](https://langchain-ai.github.io/langgraph/concepts/low_level/#checkpointer)

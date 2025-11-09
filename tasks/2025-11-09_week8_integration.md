# Job: Integration & Testing

## Overview
Integrate LangGraph workflow with MCP server and commands, perform end-to-end testing, create comprehensive documentation, and validate production readiness. Final phase ensuring the migration is complete and usable.

## Story Points
8

## Todos from Sprint
### MCP Server Updates
- [ ] Update mcp-servers/langgraph_sprint_executor.py
- [ ] Implement execute_planning tool (planning phase only)
- [ ] Implement execute_sprint tool (full workflow)
- [ ] Implement get_sprint_state tool (state inspection)
- [ ] Implement resume_sprint tool (checkpoint resumption)
- [ ] Add state visualization helper
- [ ] Test all MCP tools

### Command Updates
- [ ] Update commands/create-sprint.md to use execute_planning
- [ ] Update commands/setup-jobs.md to use execute_sprint
- [ ] Add --use-langgraph flag for opt-in
- [ ] Keep agent-based fallback working
- [ ] Test command integration
- [ ] Update command documentation

### End-to-End Testing
- [ ] Create test project for sprint execution
- [ ] Test full sprint workflow (planning → implementation → merge)
- [ ] Test multi-repo scenarios
- [ ] Test error recovery and resumption
- [ ] Test checkpoint-based resume
- [ ] Validate non-blocking failure handling
- [ ] Performance benchmark (parallel speedup)

### Documentation
- [ ] Update LANGGRAPH.md with new architecture
- [ ] Create migration guide for users
- [ ] Document all LangGraph nodes
- [ ] Add troubleshooting section
- [ ] Create developer guide for contributors
- [ ] Document MCP tool usage
- [ ] Add mermaid workflow diagrams
- [ ] Write release notes

## Implementation Plan
1. **Create MCP server** - Implement langgraph_sprint_executor.py with all tools
2. **Implement execute_planning** - Run planning phase only
3. **Implement execute_sprint** - Run full workflow
4. **Implement get_sprint_state** - State inspection tool
5. **Implement resume_sprint** - Checkpoint resumption tool
6. **Update commands** - Integrate LangGraph tools with opt-in flag
7. **Create test project** - Set up comprehensive test scenario
8. **Run end-to-end tests** - Validate full workflow
9. **Write documentation** - LANGGRAPH.md, migration guide, troubleshooting
10. **Performance benchmarking** - Measure parallel speedup
11. **Release preparation** - Final review, release notes

## Files to Create/Modify
- sprint-workflow/mcp-servers/langgraph_sprint_executor.py (new - MCP server)
- sprint-workflow/commands/create-sprint.md (modify - add LangGraph integration)
- sprint-workflow/commands/setup-jobs.md (modify - add LangGraph integration)
- sprint-workflow/plugin.json (modify - register MCP server)
- sprint-workflow/LANGGRAPH.md (new - architecture documentation)
- sprint-workflow/MIGRATION_GUIDE.md (new - migration guide)
- sprint-workflow/TROUBLESHOOTING.md (new - troubleshooting guide)
- sprint-workflow/tests/e2e/ (new - end-to-end test suite)
- sprint-workflow/RELEASE_NOTES.md (new)

## Success Criteria
- All todos complete
- MCP server exposes all LangGraph tools
- Commands updated to use LangGraph
- Agent-based fallback preserved
- End-to-end sprint execution tested
- Multi-repo scenarios validated
- Error recovery tested
- Documentation complete (LANGGRAPH.md, migration guide)
- Troubleshooting playbook created
- Performance benchmarks met (3x speedup with pool_size=3)
- Release notes written

## Dependencies
- Depends on: All jobs (1-7) - requires complete implementation
- Required by: None (final job)

## Technical Notes
### MCP Server Implementation
```python
#!/usr/bin/env python3
"""LangGraph Sprint Executor MCP Server."""
import asyncio
import json
import sys
from langgraph.workflow import build_workflow
from langgraph.checkpoint.memory import MemorySaver

async def execute_planning(sprint_theme: str, project_name: str) -> dict:
    """Execute planning phase only."""
    workflow = build_workflow()
    checkpointer = MemorySaver()

    initial_state = {
        "sprint_theme": sprint_theme,
        "project_name": project_name,
        "phase": "init"
    }

    config = {"configurable": {"thread_id": f"planning_{sprint_theme}"}}

    # Run until planning complete
    final_state = await workflow.ainvoke(
        initial_state,
        config,
        interrupt_before=["job_creation"]  # Stop after planning
    )

    return {
        "status": "planning_complete",
        "sprint_prd_path": final_state["sprint_prd_path"],
        "todos_path": final_state["todos_path"]
    }

async def execute_sprint(sprint_theme: str, project_name: str, pool_size: int = 3) -> dict:
    """Execute full sprint workflow."""
    workflow = build_workflow()
    checkpointer = MemorySaver()

    initial_state = {
        "sprint_theme": sprint_theme,
        "project_name": project_name,
        "pool_size": pool_size,
        "phase": "init"
    }

    config = {"configurable": {"thread_id": f"sprint_{sprint_theme}"}}

    # Run full workflow
    final_state = await workflow.ainvoke(initial_state, config)

    return {
        "status": "sprint_complete",
        "verified_jobs": len(final_state["verified_jobs"]),
        "failed_jobs": len(final_state["failed_jobs"]),
        "merge_status": final_state["merge_status"]
    }

async def get_sprint_state(thread_id: str) -> dict:
    """Inspect sprint state."""
    checkpointer = MemorySaver()
    config = {"configurable": {"thread_id": thread_id}}

    state = checkpointer.get(config)

    return {
        "phase": state["phase"],
        "jobs": state.get("jobs", []),
        "verified_jobs": state.get("verified_jobs", []),
        "failed_jobs": state.get("failed_jobs", [])
    }

async def resume_sprint(thread_id: str) -> dict:
    """Resume sprint from checkpoint."""
    workflow = build_workflow()
    checkpointer = MemorySaver()

    config = {"configurable": {"thread_id": thread_id}}

    # Resume from checkpoint
    final_state = await workflow.ainvoke(None, config)

    return {
        "status": "resumed",
        "phase": final_state["phase"]
    }
```

### Command Integration Pattern
```markdown
## Step 1: Choose Execution Mode

Ask user: "Use LangGraph deterministic execution? (recommended) [y/n]"

**If yes:**
Using mcp__langgraph_sprint_executor__execute_planning, execute planning phase:
- sprint_theme: {theme}
- project_name: {project}

**If no (fallback to agents):**
[Existing agent-based implementation]
```

### End-to-End Test Scenario
```python
# Test full sprint execution
async def test_full_sprint():
    """Test complete sprint workflow."""
    # Create test project
    setup_test_project()

    # Execute sprint
    result = await execute_sprint(
        sprint_theme="test_feature",
        project_name="test_project",
        pool_size=2
    )

    # Validate results
    assert result["status"] == "sprint_complete"
    assert len(result["verified_jobs"]) >= 1
    assert len(result["failed_jobs"]) == 0

    # Verify artifacts created
    assert os.path.exists("thoughts/sprint-plans/test_project/")
    assert os.path.exists("tasks/")

    # Verify branches merged
    branches = run_command("git branch")
    assert "feat/" not in branches  # Cleaned up

    # Cleanup
    teardown_test_project()
```

### Documentation Structure
**LANGGRAPH.md:**
- Architecture overview
- State machine diagram
- Node descriptions
- Workflow phases
- Integration points

**MIGRATION_GUIDE.md:**
- Why migrate to LangGraph
- Installation steps
- Usage examples
- Comparison with agent-based approach
- Troubleshooting common issues

**TROUBLESHOOTING.md:**
- Common errors and solutions
- Checkpoint inspection
- State debugging
- Performance tuning
- Recovery procedures

### Performance Benchmarking
```python
# Measure parallel speedup
async def benchmark_parallel_execution():
    """Benchmark parallel vs sequential execution."""
    # Sequential (pool_size=1)
    start = time.time()
    await execute_sprint("test", "bench", pool_size=1)
    sequential_time = time.time() - start

    # Parallel (pool_size=3)
    start = time.time()
    await execute_sprint("test", "bench", pool_size=3)
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time

    print(f"Sequential: {sequential_time}s")
    print(f"Parallel: {parallel_time}s")
    print(f"Speedup: {speedup}x")

    assert speedup >= 2.5  # Should be ~3x with pool_size=3
```

### Release Notes Template
```markdown
# LangGraph Migration Release v2.0.0

## Overview
Complete migration from agent-based orchestration to deterministic LangGraph state machine.

## Key Features
- 100% deterministic execution
- Checkpoint-based resumability
- Non-blocking error handling
- Parallel job execution
- Auto-merge verified jobs

## Migration Guide
See MIGRATION_GUIDE.md for detailed instructions.

## Breaking Changes
None - agent-based fallback preserved.

## Performance
- 3x speedup with parallel execution (pool_size=3)
- 95%+ resume success rate
- 90%+ sprint completion rate

## Documentation
- LANGGRAPH.md - Architecture documentation
- MIGRATION_GUIDE.md - Migration instructions
- TROUBLESHOOTING.md - Common issues and solutions
```

### Testing Strategy
- Unit tests for MCP tools
- Integration tests for command updates
- End-to-end sprint execution test
- Multi-repo scenario test
- Error recovery test
- Checkpoint resume test
- Performance benchmarks
- Documentation review

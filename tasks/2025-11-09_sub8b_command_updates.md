# Sub-Task 8B: Command Integration Updates

## Parent Job
Week 8: Integration & Testing

## Story Points
2

## Scope
Update /create-sprint and /setup-jobs commands to use LangGraph MCP tools with opt-in flag and fallback.

## Can Run in Parallel
YES - Fully parallel with 8A (MCP server), 8C (docs)

## Todos
- [ ] Update commands/create-sprint.md to use execute_planning
- [ ] Update commands/setup-jobs.md to use execute_sprint
- [ ] Add --use-langgraph flag for opt-in
- [ ] Keep agent-based fallback working
- [ ] Test command integration with MCP tools
- [ ] Update command documentation with examples
- [ ] Test both LangGraph and agent-based paths

## Files to Create/Modify
- sprint-workflow/commands/create-sprint.md (modify)
- sprint-workflow/commands/setup-jobs.md (modify)
- sprint-workflow/tests/commands/test_create_sprint.py (new)
- sprint-workflow/tests/commands/test_setup_jobs.py (new)

## Dependencies
- Sub-task 8A (needs MCP tools available)

## Blocks
- None (command updates independent)

## Implementation Notes
```markdown
# commands/create-sprint.md updates

## Step 1: Choose Execution Mode

Ask user: "Use LangGraph deterministic execution? (recommended) [y/n]"

**If yes (LangGraph path):**

### Step 2A: Execute Planning Phase

Using mcp__langgraph-sprint-executor__execute_planning, run planning:

```json
{
  "sprint_theme": "{user_provided_theme}",
  "project_name": "{detected_project_name}"
}
```

Store results:
- synthesis_output → planning summary
- gap_analysis_output → validation results

### Step 3A: Display Planning Results

Show user the planning synthesis and gap analysis recommendations.

Ask: "Approve planning and proceed to PRD generation? [y/n]"

If yes:
- Generate Sprint PRD from synthesis
- Generate todos from PRD
- Save to thoughts/sprint-plans/{project}/

**If no (Agent-based fallback):**

### Step 2B: Multi-Agent Planning (Original)

Task 1 - Product Manager:
Using product-manager agent...
[existing implementation]

Task 2 - UX Designer:
Using ux-designer agent...
[existing implementation]

Task 3 - Senior Engineer:
Using senior-engineer agent...
[existing implementation]

[... rest of original flow]
```

```markdown
# commands/setup-jobs.md updates

## Step 6: Execute Sprint Implementation

**If LangGraph available:**

Using mcp__langgraph-sprint-executor__execute_sprint:

```json
{
  "sprint_theme": "{sprint_theme}",
  "project_name": "{project}",
  "sprint_prd_path": "{prd_file_path}",
  "todos_path": "{todos_file_path}",
  "pool_size": 3
}
```

Monitor execution:
- Check sprint_status.md for live updates
- Wait for completion
- Display results (verified, failed, merged)

**If LangGraph not available (fallback):**

Using sprint-coordinator agent:
[existing implementation]
```

## Success Criteria
- create-sprint.md updated with LangGraph option
- setup-jobs.md updated with LangGraph option
- Opt-in flag working
- Agent-based fallback preserved
- Command tests passing
- Both execution paths tested
- Documentation updated with examples

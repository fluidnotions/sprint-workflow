---
description: Display current sprint progress and status
allowed-tools: Read, Grep, Bash
---

# Sprint Status

Display comprehensive sprint progress dashboard.

## Status Checks

1. **Find active sprint**:
   - Look for most recent sprint plan
   - Check for active worktrees
   - Read sprint_status.md if exists

2. **Analyze progress**:
   ```bash
   # Check worktrees
   git worktree list
   
   # Check todo completion
   grep -c "^\[x\]" *_todos.md
   grep -c "^\[ \]" *_todos.md
   
   # Check commits
   git log --oneline --since="1 week ago"
   ```

3. **Generate dashboard**:

```markdown
# Sprint Status Report
Generated: {timestamp}

## Active Sprint: {name}
- Started: {date}
- Target: {completion}
- Plan: {plan_path}

## Progress Overview
Tasks: ███████░░░ 70% (7/10)
Todos: ████████░░ 80% (16/20)

## Active Jobs
| Job | Status | Worktree | Agent | Progress |
|-----|--------|----------|-------|----------|
| auth-system | 🟢 Active | feat/auth | sonnet-1 | 85% |
| api-endpoints | 🟢 Active | feat/api | sonnet-2 | 60% |
| frontend | 🟡 Queued | - | - | 0% |

## Recent Activity
- [2h ago] Completed user authentication
- [4h ago] Fixed database migrations
- [6h ago] Updated API schemas

## Blockers
- ⚠️ Dependency issue with auth library
- ⚠️ Waiting for design approval on dashboard

## Next Milestones
- [ ] Complete API endpoints (today)
- [ ] Start frontend implementation
- [ ] Run integration tests
```

## Next Steps

Based on status:
- **In progress**: "Sprint active. Check individual jobs with `/worktree-status`"
- **Blocked**: "Blockers identified. Run `/debug` or consult team"
- **Near complete**: "Sprint nearly done. Use `/verify_implementation` for each completed task"
- **Complete**: "Sprint complete! Run `/sprint-retrospective`"

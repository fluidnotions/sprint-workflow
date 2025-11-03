---
description: Generate comprehensive sprint retrospective and lessons learned
allowed-tools: Read, Write, Grep, Bash
---

# Sprint Retrospective

Document sprint outcomes, metrics, and lessons learned.

## Data Collection

1. **Gather metrics**:
   ```bash
   # Count completed tasks
   grep -c "^\[x\]" *_todos.md
   
   # Count commits
   git log --oneline --since="{sprint_start}" | wc -l
   
   # Count files changed
   git diff --stat {sprint_start_ref}
   
   # Test coverage if available
   npm test -- --coverage 2>/dev/null || pytest --cov 2>/dev/null
   ```

2. **Analyze implementation**:
   - Review all task files in `tasks/`
   - Check PR descriptions in `docs/prs/`
   - Review validation reports

3. **Generate retrospective**:

Create `{datetime}_sprint_retro.md`:

```markdown
# Sprint Retrospective: {sprint_name}

## Overview
- Duration: {start} to {end} ({days} days)
- Team: Claude Code + {developer}
- Parallel Agents Used: {max_concurrent}

## Metrics
### Delivery
- Planned Tasks: {planned}
- Completed Tasks: {completed} ({percentage}%)
- Additional Tasks: {unplanned}

### Code Metrics
- Lines Added: {added}
- Lines Removed: {removed}
- Files Modified: {files}
- Commits: {commits}
- PRs Merged: {prs}

### Quality Metrics
- Test Coverage: {coverage}%
- Bugs Found: {bugs}
- Bugs Fixed: {fixed}
- Code Review Issues: {issues}

## Timeline
- Sprint Planning: {time}h
- Implementation: {time}h
- Testing: {time}h
- Documentation: {time}h
- Total: {total}h

## Completed Features
1. ✅ {feature_1}
   - Description
   - Impact
   
2. ✅ {feature_2}
   - Description
   - Impact

## What Went Well
- Parallel development with worktrees improved velocity
- Gap analysis caught architecture issues early
- Clear task organization reduced context switching

## Challenges Faced
- {challenge_1}: How we resolved it
- {challenge_2}: How we resolved it

## Lessons Learned
1. **Technical**: {learning}
2. **Process**: {learning}
3. **Architecture**: {learning}

## Improvements for Next Sprint
- [ ] {improvement_1}
- [ ] {improvement_2}
- [ ] {improvement_3}

## Documentation Created
- Sprint Plan: {path}
- Task Specifications: {count} files
- PR Documentation: {count} files
- Test Documentation: {path}
```

## Step 4: Generate Unit Tests

After retrospective, create comprehensive tests:

```
Spawn test-automator agents for each component:
- Unit tests for new functions
- Integration tests for workflows  
- E2E tests for critical paths
Target: 80% coverage on new code
```

## Next Steps

- **Success**: "Retrospective complete! Next sprint: Run `/create-sprint` with lessons learned"
- **Tests needed**: "Retrospective done. Manually create comprehensive test suite or add test generation to sprint plan"
- **Documentation**: "Update project documentation to reflect new features"

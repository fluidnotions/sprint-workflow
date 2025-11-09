# Sub-Task 8C: Documentation & Diagrams

## Parent Job
Week 8: Integration & Testing

## Story Points
2

## Scope
Create comprehensive documentation including architecture docs, migration guide, and troubleshooting playbook.

## Can Run in Parallel
YES - Fully parallel with 8A (MCP), 8B (commands)

## Todos
- [ ] Update LANGGRAPH.md with complete architecture
- [ ] Create migration guide for users
- [ ] Document all LangGraph nodes with examples
- [ ] Add troubleshooting section with common errors
- [ ] Create developer guide for contributors
- [ ] Document MCP tool usage with examples
- [ ] Add mermaid workflow diagrams
- [ ] Write release notes

## Files to Create/Modify
- sprint-workflow/LANGGRAPH.md (modify - complete architecture)
- sprint-workflow/MIGRATION_GUIDE.md (new)
- sprint-workflow/TROUBLESHOOTING.md (new)
- sprint-workflow/DEVELOPER_GUIDE.md (new)
- sprint-workflow/RELEASE_NOTES.md (new)

## Dependencies
- None (documentation can be written in parallel)

## Blocks
- None (docs independent)

## Implementation Notes
```markdown
# LANGGRAPH.md structure

## Architecture Overview
- State machine diagram (mermaid)
- Phase descriptions
- Node responsibility matrix

## State Schema Reference
- SprintWorkflowState fields
- JobSpec structure
- RepoInfo structure
- ErrorRecord structure

## Node Documentation
For each node:
- Purpose
- Inputs (state fields)
- Outputs (state updates)
- Side effects (files, git ops)
- Error handling

## Workflow Phases
1. Planning (PM → UX → Eng → Synthesis)
2. Gap Analysis (validation + feedback loop)
3. Job Creation (PRD → Jobs → Validation → Worktrees)
4. Implementation (parallel execution + verification)
5. Branch Management (update + conflicts + merge)

## Integration Points
- MCP server tools
- Command integration
- Checkpoint system
- Error reporting
```

```markdown
# MIGRATION_GUIDE.md structure

## Why Migrate?
- Deterministic execution
- Resumability
- Better debugging
- True parallelization

## Installation
1. Install dependencies
2. Set API key
3. Enable MCP server

## Usage Examples
- Planning only: execute_planning
- Full sprint: execute_sprint
- Inspect state: get_sprint_state
- Resume: resume_sprint

## Comparison Table
| Feature | Agent-based | LangGraph |
|---------|-------------|-----------|
| ... | ... | ... |

## Migration Checklist
- [ ] Install langgraph
- [ ] Set ANTHROPIC_API_KEY
- [ ] Test planning phase
- [ ] Test full sprint
- [ ] Verify resumability
```

```markdown
# TROUBLESHOOTING.md structure

## Common Errors

### "Module not found: langgraph"
**Solution**: Run `bash scripts/install_langgraph.sh`

### "ANTHROPIC_API_KEY not set"
**Solution**: `export ANTHROPIC_API_KEY="sk-ant-..."`

### "Verification loop hanging"
**Diagnosis**: Check implementing_jobs status
**Solution**: Inspect state with get_sprint_state

### "Branch conflicts not resolving"
**Diagnosis**: Complex code conflict
**Solution**: Manual resolution in worktree

## State Inspection
```python
# Get current state
state = get_sprint_state("sprint_my-feature")
print(state["phase"])
print(state["verified_jobs"])
```

## Recovery Procedures
1. Checkpoint corruption → restart with new thread_id
2. Failed job → check error report in sprint_errors_*.md
3. Stuck verification → manually verify in worktree
```

```mermaid
# Workflow diagram for LANGGRAPH.md

graph TD
    START([Start]) --> PM[PM Planning]
    START --> UX[UX Planning]
    START --> ENG[Engineering Planning]

    PM --> SYNTH[Synthesis]
    UX --> SYNTH
    ENG --> SYNTH

    SYNTH --> GAP[Gap Analysis]
    GAP -->|approved| PRD[Generate PRD]
    GAP -->|feedback| UPDATE[Update Planning]
    UPDATE --> PM

    PRD --> JOBS[Create Jobs]
    JOBS --> VALIDATE[Validate Jobs]
    VALIDATE -->|approved| WORKTREES[Setup Worktrees]
    VALIDATE -->|feedback| JOBS

    WORKTREES --> IMPL[Parallel Implementation]
    IMPL --> VERIFY[Verification Loop]
    VERIFY -->|retry| VERIFY
    VERIFY -->|complete| BRANCH[Branch Management]

    BRANCH --> MERGE[Push & Merge]
    MERGE --> CLEANUP[Cleanup]
    CLEANUP --> END([End])
```

## Success Criteria
- LANGGRAPH.md complete with architecture
- Migration guide created
- Troubleshooting playbook complete
- Developer guide for contributors
- Mermaid diagrams generated
- Release notes written
- All documentation reviewed
- Examples tested

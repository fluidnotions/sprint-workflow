# Sub-Task 1A: Dependencies & Installation

## Parent Job
Week 1: Infrastructure & State Schema

## Story Points
2

## Scope
Install LangGraph dependencies and create installation infrastructure. This is the foundational step that enables all other development.

## Can Run in Parallel
YES - Independent task, no dependencies

## Todos
- [ ] Install LangGraph dependencies (langgraph, langchain-anthropic, langchain-core)
- [ ] Update requirements.txt with new dependencies
- [ ] Create installation script for LangGraph (scripts/install_langgraph.sh)
- [ ] Verify ANTHROPIC_API_KEY environment variable setup
- [ ] Test dependency installation on clean environment

## Files to Create/Modify
- sprint-workflow/requirements.txt (modify - add dependencies)
- sprint-workflow/scripts/install_langgraph.sh (new)

## Dependencies
- None (foundation)

## Blocks
- Sub-task 1B (needs dependencies installed for testing)
- Sub-task 1C (needs dependencies for test infrastructure)

## Implementation Notes
```bash
# requirements.txt additions
langgraph>=0.0.20
langchain-anthropic>=0.1.0
langchain-core>=0.1.0

# Test installation
pip install --user -r requirements.txt
python3 -c "import langgraph; print('LangGraph installed successfully')"
```

## Success Criteria
- Dependencies installable via pip
- Installation script works on clean environment
- ANTHROPIC_API_KEY validation working
- All imports successful

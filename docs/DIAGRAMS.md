# Workflow Diagrams

LangGraph state machine visualization for the sprint workflow plugin.

## Files

### workflow-diagram.png
Visual diagram showing the complete 12-phase sprint workflow with:
- **Parallel execution**: PM, UX, Engineering planning nodes from START
- **Feedback loops**: Gap analysis and job validation with conditional routing
- **Retry logic**: Verification loop with retry/continue paths
- **Phase transitions**: Solid edges for direct transitions, dotted edges for conditionals

### workflow-diagram.mmd
Mermaid syntax for the workflow diagram, suitable for embedding in documentation or rendering with Mermaid.js.

## Regenerating Diagrams

If you modify the workflow in `graph/workflow.py`, regenerate the diagrams:

```bash
bash scripts/generate_diagram.sh
```

This generates both the PNG and Mermaid syntax files from the LangGraph state machine definition.

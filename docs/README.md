# Documentation Assets

This directory contains generated diagrams and visual documentation for the sprint workflow plugin.

## Files

### workflow-diagram.png
LangGraph state machine visualization showing the complete 12-phase sprint workflow.

**Generated with:**
```bash
python3 -c "
from graph.workflow import build_workflow
workflow = build_workflow()
app = workflow.compile()
graph = app.get_graph()
mermaid_png = graph.draw_mermaid_png()
with open('docs/workflow-diagram.png', 'wb') as f:
    f.write(mermaid_png)
"
```

### workflow-diagram.mmd
Mermaid syntax for the workflow diagram, suitable for embedding in documentation or rendering with Mermaid.js.

## Regenerating Diagrams

If you modify the workflow in `graph/workflow.py`, regenerate the diagrams:

```bash
# From repository root
python3 << 'EOF'
from graph.workflow import build_workflow

workflow = build_workflow()
app = workflow.compile()
graph = app.get_graph()

# PNG for README
mermaid_png = graph.draw_mermaid_png()
with open('docs/workflow-diagram.png', 'wb') as f:
    f.write(mermaid_png)

# Mermaid syntax for documentation
mermaid_syntax = graph.draw_mermaid()
with open('docs/workflow-diagram.mmd', 'w') as f:
    f.write(mermaid_syntax)

print("✓ Diagrams regenerated successfully")
EOF
```

## Diagram Features

The workflow diagram shows:

- **Nodes**: Each workflow phase (planning, gap analysis, job creation, etc.)
- **Solid edges**: Direct transitions between phases
- **Dotted edges**: Conditional routing (labeled with conditions)
- **Parallel execution**: PM, UX, Engineering planning nodes from START
- **Feedback loops**: Gap analysis and job validation loops
- **Retry logic**: Verification loop with retry/continue paths

## Usage in Documentation

The diagram is referenced in:
- `README.md` - Main plugin documentation
- `LANGGRAPH.md` - LangGraph execution engine details
- `CLAUDE.md` - Developer guidance (optional)

#!/bin/bash
# Generate LangGraph workflow diagram

set -e

cd "$(dirname "$0")/.."

echo "Generating workflow diagram from LangGraph state machine..."

python3 << 'EOF'
from graph.workflow import build_workflow

workflow = build_workflow()
app = workflow.compile()
graph = app.get_graph()

# Generate PNG
mermaid_png = graph.draw_mermaid_png()
with open('docs/workflow-diagram.png', 'wb') as f:
    f.write(mermaid_png)

# Generate Mermaid syntax
mermaid_syntax = graph.draw_mermaid()
with open('docs/workflow-diagram.mmd', 'w') as f:
    f.write(mermaid_syntax)

print("✓ PNG diagram: docs/workflow-diagram.png")
print("✓ Mermaid syntax: docs/workflow-diagram.mmd")
EOF

echo "✓ Diagrams generated successfully"

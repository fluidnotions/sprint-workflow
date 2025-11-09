# Sub-Task 8A: MCP Server Implementation

## Parent Job
Week 8: Integration & Testing

## Story Points
3

## Scope
Create MCP server exposing LangGraph workflow tools for integration with Claude Code commands.

## Can Run in Parallel
YES - Fully parallel with 8B (commands), 8C (docs)

## Todos
- [ ] Create mcp-servers/langgraph_sprint_executor.py
- [ ] Implement execute_planning tool (planning phase only)
- [ ] Implement execute_sprint tool (full workflow)
- [ ] Implement get_sprint_state tool (state inspection)
- [ ] Implement resume_sprint tool (checkpoint resumption)
- [ ] Add state visualization helper
- [ ] Register MCP server in plugin.json
- [ ] Test all MCP tools
- [ ] Test JSON-RPC protocol compliance

## Files to Create/Modify
- sprint-workflow/mcp-servers/langgraph_sprint_executor.py (new)
- sprint-workflow/plugin.json (modify - register MCP server)
- sprint-workflow/tests/mcp/test_langgraph_executor.py (new)

## Dependencies
- All Week 1-7 sub-tasks (needs complete workflow implementation)

## Blocks
- Sub-task 8D (E2E testing uses MCP tools)

## Implementation Notes
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
        interrupt_before=["generate_sprint_prd"]  # Stop after gap analysis
    )

    return {
        "status": "planning_complete",
        "synthesis_output": final_state.get("synthesis_output"),
        "gap_analysis_output": final_state.get("gap_analysis_output")
    }

async def execute_sprint(
    sprint_theme: str,
    project_name: str,
    sprint_prd_path: str,
    todos_path: str,
    pool_size: int = 3
) -> dict:
    """Execute full sprint workflow."""
    workflow = build_workflow()
    checkpointer = MemorySaver()

    initial_state = {
        "sprint_theme": sprint_theme,
        "project_name": project_name,
        "sprint_prd_path": sprint_prd_path,
        "todos_path": todos_path,
        "pool_size": pool_size,
        "phase": "init"
    }

    config = {"configurable": {"thread_id": f"sprint_{sprint_theme}"}}

    # Run full workflow
    final_state = await workflow.ainvoke(initial_state, config)

    return {
        "status": "sprint_complete",
        "verified_jobs": final_state.get("verified_jobs", []),
        "failed_jobs": final_state.get("failed_jobs", []),
        "merge_status": final_state.get("merge_status", [])
    }

async def get_sprint_state(thread_id: str) -> dict:
    """Inspect sprint state."""
    checkpointer = MemorySaver()
    config = {"configurable": {"thread_id": thread_id}}

    state = checkpointer.get(config)

    if not state:
        return {"error": "Sprint not found"}

    return {
        "phase": state.get("phase"),
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
        "phase": final_state.get("phase")
    }

# MCP Server JSON-RPC Handler
async def handle_request(request: dict) -> dict:
    """Handle MCP tool requests."""
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "execute_planning":
            result = await execute_planning(**arguments)
        elif tool_name == "execute_sprint":
            result = await execute_sprint(**arguments)
        elif tool_name == "get_sprint_state":
            result = await get_sprint_state(**arguments)
        elif tool_name == "resume_sprint":
            result = await resume_sprint(**arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }

    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": "execute_planning",
                    "description": "Execute planning phase only (PM + UX + Eng + Gap Analysis)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sprint_theme": {"type": "string"},
                            "project_name": {"type": "string"}
                        },
                        "required": ["sprint_theme", "project_name"]
                    }
                },
                {
                    "name": "execute_sprint",
                    "description": "Execute full sprint workflow",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sprint_theme": {"type": "string"},
                            "project_name": {"type": "string"},
                            "sprint_prd_path": {"type": "string"},
                            "todos_path": {"type": "string"},
                            "pool_size": {"type": "integer", "default": 3}
                        },
                        "required": ["sprint_theme", "project_name", "sprint_prd_path", "todos_path"]
                    }
                },
                {
                    "name": "get_sprint_state",
                    "description": "Inspect current sprint state",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "thread_id": {"type": "string"}
                        },
                        "required": ["thread_id"]
                    }
                },
                {
                    "name": "resume_sprint",
                    "description": "Resume sprint from checkpoint",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "thread_id": {"type": "string"}
                        },
                        "required": ["thread_id"]
                    }
                }
            ]
        }

    elif method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}}
        }

    return {"error": "Unknown method"}

# Main MCP server loop
async def main():
    while True:
        line = await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline
        )

        if not line:
            break

        request = json.loads(line)
        response = await handle_request(request)

        print(json.dumps(response))
        sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
```

## Success Criteria
- MCP server implemented
- All 4 tools working (execute_planning, execute_sprint, get_sprint_state, resume_sprint)
- JSON-RPC protocol compliant
- Registered in plugin.json
- Tools tested individually
- Integration with workflow verified

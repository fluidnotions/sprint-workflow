# Sub-Task 3A: Gap Analysis Node with Web Search

## Parent Job
Week 3: Gap Analysis & Feedback Loop

## Story Points
5

## Scope
Implement gap analysis validation node with web search integration for best practices research. Core validation logic.

## Can Run in Parallel
YES - Parallel with 3B (conditional edge logic is independent)

## Todos
- [ ] Create langgraph/nodes/validation.py module
- [ ] Extract gap analyzer prompt from agents/gap-analyzer.md
- [ ] Implement gap_analysis() node function
- [ ] Add web search integration for best practices research
- [ ] Create parse_gap_analysis() helper for recommendations
- [ ] Add gap_analysis_output to state schema
- [ ] Add gap_analysis_retry_count to state schema
- [ ] Write unit tests for gap analysis node
- [ ] Test web search integration with mocked results

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/validation.py (new)
- sprint-workflow/langgraph/state.py (modify - add gap analysis fields)
- sprint-workflow/tests/langgraph/test_validation_nodes.py (new)
- sprint-workflow/agents/gap-analyzer.md (read)

## Dependencies
- Sub-task 2D (needs synthesis output)

## Blocks
- Sub-task 3C (feedback application needs gap analysis results)
- Sub-task 3B (conditional edge uses gap analysis output for routing)

## Implementation Notes
```python
async def gap_analysis(state: SprintWorkflowState) -> dict:
    """Analyze planning outputs for gaps and inconsistencies."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Combine planning outputs
    planning_doc = combine_planning_outputs(
        state["pm_output"],
        state["ux_output"],
        state["engineering_output"],
        state["synthesis_output"]
    )

    # Web search for best practices
    search_results = await web_search_best_practices(state["sprint_theme"])

    prompt = load_gap_analyzer_prompt()
    context = f"""
Planning Document:
{planning_doc}

Best Practices Research:
{search_results}
"""

    response = await client.messages.create(
        model="claude-opus-4-20250514",
        messages=[{"role": "user", "content": f"{prompt}\n\n{context}"}],
        max_tokens=4000
    )

    recommendations = parse_gap_analysis(response.content[0].text)

    return {
        "gap_analysis_output": recommendations,
        "phase": "gap_analysis_complete"
    }

async def web_search_best_practices(sprint_theme: str) -> str:
    """Search web for best practices related to sprint theme."""
    # Use WebFetch or cached-web-fetch MCP tool
    queries = [
        f"{sprint_theme} best practices",
        f"{sprint_theme} architecture patterns",
        f"{sprint_theme} security considerations"
    ]
    results = []
    for query in queries:
        result = await fetch_web_content(query)
        results.append(result)
    return "\n\n".join(results)

def parse_gap_analysis(text: str) -> dict:
    """Parse gap analysis recommendations."""
    return {
        "severity": extract_severity(text),  # "none" | "minor" | "critical"
        "gaps": extract_gaps(text),
        "recommendations": extract_recommendations(text)
    }
```

## Success Criteria
- Gap analysis node implemented
- Web search integration working
- Recommendations parsed correctly
- gap_analysis_output in state schema
- Unit tests passing with mocked web search
- Severity levels correctly identified
- Node integrates with workflow

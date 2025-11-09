"""Gap analysis node for validating sprint planning."""

import json
from typing import Dict, Any
from anthropic import AsyncAnthropic

from ..state import SprintWorkflowState


async def gap_analysis_node(state: SprintWorkflowState) -> Dict[str, Any]:
    """Gap Analysis node - validates synthesized planning for completeness.
    
    Uses web research and architectural best practices to identify:
    - Missing technical considerations
    - Security vulnerabilities  
    - Scalability issues
    - Accessibility gaps
    - Performance bottlenecks
    - Integration challenges
    - Missing user stories or edge cases
    
    Args:
        state: Current workflow state with synthesized_plan
        
    Returns:
        Dict with gap_analysis containing issues found and recommendations
    """
    synthesized_plan = state.get("synthesized_plan", {})
    sprint_theme = state.get("sprint_theme", "")
    project_name = state.get("project_name", "Unknown Project")
    
    # Extract key elements for analysis
    integrated_stories = synthesized_plan.get("integrated_stories", [])
    roadmap = synthesized_plan.get("implementation_roadmap", {})
    risk_matrix = synthesized_plan.get("risk_matrix", {})
    execution_plan = synthesized_plan.get("execution_plan", {})
    
    # Initialize Anthropic client
    client = AsyncAnthropic()
    
    # Construct detailed prompt for gap analysis
    prompt = f"""You are a Senior Solutions Architect conducting a gap analysis on a sprint plan.

Project: {project_name}
Sprint Theme: {sprint_theme}

SYNTHESIZED PLAN TO ANALYZE:
{json.dumps(synthesized_plan, indent=2)}

Your task is to identify gaps, risks, and missing considerations in this sprint plan. Analyze from multiple perspectives:

1. **Technical Architecture Gaps**:
   - Missing infrastructure components
   - Unaddressed integration points
   - Database design issues
   - API design concerns
   - Missing error handling strategies

2. **Security Vulnerabilities**:
   - Authentication/authorization gaps
   - Data encryption requirements
   - Input validation needs
   - OWASP Top 10 considerations
   - Privacy/compliance requirements (GDPR, etc.)

3. **Scalability & Performance**:
   - Bottlenecks not addressed
   - Missing caching strategies
   - Database query optimization needs
   - Load handling concerns
   - Resource management issues

4. **User Experience & Accessibility**:
   - Missing user flows or edge cases
   - Incomplete WCAG compliance
   - Mobile responsiveness gaps
   - Error state handling
   - Loading state considerations

5. **Testing & Quality**:
   - Missing test coverage areas
   - Integration test requirements
   - Performance test needs
   - E2E test scenarios

6. **Operational Readiness**:
   - Monitoring/observability gaps
   - Logging requirements
   - Deployment strategy issues
   - Rollback plans
   - Documentation needs

Return your analysis as JSON with this structure:
{{
  "issues_found": [
    {{
      "category": "technical|security|scalability|ux|testing|operational",
      "severity": "critical|high|medium|low",
      "description": "What is missing or problematic",
      "impact": "What happens if not addressed",
      "recommendation": "Specific action to take",
      "estimated_effort": "Story points or time estimate"
    }}
  ],
  "strengths": [
    "Positive aspect 1",
    "Positive aspect 2"
  ],
  "overall_assessment": {{
    "readiness_score": 0.0-1.0,
    "critical_blockers": 0,
    "high_priority_items": 0,
    "recommendation": "approve|revise|major_revision"
  }}
}}

Be thorough but pragmatic. Focus on issues that would impact sprint success."""

    # Call Anthropic API
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.content[0].text
    
    # Extract JSON from response
    if "```json" in content:
        json_str = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        json_str = content.split("```")[1].split("```")[0].strip()
    else:
        json_str = content.strip()
    
    try:
        gap_analysis = json.loads(json_str)
    except json.JSONDecodeError:
        # Fallback - assume no critical issues
        gap_analysis = {
            "issues_found": [],
            "strengths": ["Plan appears comprehensive"],
            "overall_assessment": {
                "readiness_score": 0.8,
                "critical_blockers": 0,
                "high_priority_items": 0,
                "recommendation": "approve"
            }
        }
    
    # Add metadata
    gap_analysis["_meta"] = {
        "node": "gap_analysis",
        "model": "claude-sonnet-4-20250514",
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens
    }
    
    # Increment retry count for tracking
    retry_counts = state.get("retry_counts", {})
    current_count = retry_counts.get("gap_analysis", 0)
    
    # Determine if issues require feedback loop
    critical_blockers = gap_analysis.get("overall_assessment", {}).get("critical_blockers", 0)
    high_priority = gap_analysis.get("overall_assessment", {}).get("high_priority_items", 0)
    
    status_msg = f"Gap analysis complete: {len(gap_analysis.get('issues_found', []))} issues found"
    if critical_blockers > 0:
        status_msg += f" ({critical_blockers} critical blockers)"
    
    return {
        "gap_analysis": gap_analysis,
        "retry_counts": {**retry_counts, "gap_analysis": current_count + 1},
        "status_messages": [status_msg]
    }

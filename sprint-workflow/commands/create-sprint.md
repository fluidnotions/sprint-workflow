---
description: Initialize a new sprint from approved plans with comprehensive task breakdown
allowed-tools: Read, Write, Grep, Glob, Task
---

# Create Sprint

Initialize a comprehensive sprint with PRD creation, task decomposition, and todo generation.

## Step 1: Identify Sprint Scope

Check for arguments or ask:
- Sprint name/theme
- Target completion (e.g., "2 weeks", "Q1")
- Key features to include
- Reference to approved plan in `thoughts/shared/plans/`

## Step 2: Multi-Agent PRD Creation

Spawn parallel agents for comprehensive planning:

**Task 1 - Product Manager Agent:**
```
Using product-manager agent, define:
- User stories and acceptance criteria
- Business value and priorities
- Success metrics
Model: opus (for deep reasoning)
```

**Task 2 - UX Designer Agent:**
```
Using ux-designer agent, define:
- User flows and interactions
- UI states and components
- Accessibility requirements
Model: opus (for quality design)
```

**Task 3 - Senior Engineer Agent:**
```
Using senior-engineer agent, define:
- Technical architecture
- Implementation approach
- Risk assessment and mitigations
Model: opus (for architecture)
```

## Step 3: Generate Sprint Plan

Synthesize agent outputs into sprint plan at:
`thoughts/shared/plans/{datetime}_sprint_{name}.md`

Include:
- Executive summary
- Scope and objectives
- Task breakdown with priorities
- Technical requirements
- Timeline and milestones
- Success criteria

## Step 4: Create Todo List

Generate `{datetime}_todos.md` with all tasks:

```markdown
# Sprint: {name}
Generated: {datetime}
Plan: thoughts/shared/plans/{sprint_plan}.md

## Phase 1: Foundation
[ ] Set up database schema
[ ] Create API scaffolding
[ ] Initialize frontend structure

## Phase 2: Core Features
[ ] Implement authentication
[ ] Build user dashboard
[ ] Add data models

## Phase 3: Polish
[ ] Add error handling
[ ] Implement logging
[ ] Write documentation
```

## Step 5: Run Architecture Validation

Invoke gap-analyzer agent:
```
Using gap-analyzer agent with websearch-researcher:
- Validate architecture against best practices
- Check for missing components
- Identify technical risks
- Suggest improvements
Input: Sprint plan and todos
Output: Validation report with recommendations
```

## Step 6: Update Based on Validation

If gap-analyzer finds issues:
1. Present findings to user
2. Ask: "Apply recommended changes? (yes/no)"
3. If yes, update sprint plan and todos
4. Document changes in sprint plan

## Output

Display sprint summary:
```
Sprint "{name}" initialized successfully!

📋 Sprint Plan: thoughts/shared/plans/{datetime}_sprint_{name}.md
📝 Todo List: {datetime}_todos.md
✅ Architecture validated and optimized

Next step: Run `/setup-jobs` to organize tasks by code co-location
```

## Relationship to Workflow

```
[create-sprint] → [setup-jobs] → [implement] → [verify_implementation] → [retrospective]
        ↓
[gap-analyzer validation]
```

This command initiates the entire sprint workflow, setting up everything needed for parallel development.

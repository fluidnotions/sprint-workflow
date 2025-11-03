---
description: Initialize a new sprint from approved briefs with comprehensive Sprint PRD
allowed-tools: Read, Write, Grep, Glob, Task
---

# Create Sprint

Initialize a comprehensive sprint with Sprint PRD creation, task decomposition, and todo generation.

## Step 1: Identify Sprint Scope

Get the project name from the current working directory:
```bash
PROJECT_NAME=$(basename "$PWD")
```

Check for arguments or ask:
- Sprint name/theme
- Key features to include
- Reference to approved brief in `thoughts/sprint-plans/{project_name}/`

**IMPORTANT:** Do NOT ask about timeline, duration, or target completion dates. Use story points only for estimation.

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

## Step 3: Generate Sprint PRD

Synthesize agent outputs into Sprint PRD at:
`thoughts/sprint-plans/{project_name}/{datetime}_prd_{name}.md`

(Where `{project_name}` is the basename of the current working directory)

Include:
- Executive summary
- Scope and objectives
- Task breakdown with priorities (story points only)
- Technical requirements
- Success criteria
- Story point distribution by phase

**CRITICAL - DO NOT INCLUDE:**
- Duration estimates (weeks, days, hours)
- Timeline or target dates
- Time-based milestones
- Any time-to-completion estimates

**USE ONLY:** Story points for complexity estimation

## Step 4: Create Todo List

Generate `{datetime}_todos.md` with all tasks:

```markdown
# Sprint: {name}
Generated: {datetime}
Sprint PRD: thoughts/sprint-plans/{project_name}/{prd_file}.md

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
Input: Sprint PRD and todos
Output: Validation report with recommendations
```

## Step 6: Update Based on Validation

If gap-analyzer finds issues:
1. Present findings to user
2. Ask: "Apply recommended changes? (yes/no)"
3. If yes, update Sprint PRD and todos
4. Document changes in Sprint PRD

## Output

Display sprint summary:
```
Sprint "{name}" initialized successfully!

📋 Sprint PRD: thoughts/sprint-plans/{project_name}/{datetime}_prd_{name}.md
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

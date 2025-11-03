---
description: Interactive sprint planning through iterative conversation and refinement
allowed-tools: Read, Write, AskUserQuestion, Glob
---

# Plan Sprint

Collaboratively define sprint goals and scope through iterative conversation and refinement.

This command guides you through planning a sprint with clarifying questions, scope refinement, and multiple revisions until the plan is ready for implementation.

## Overview

**Purpose:** Create a well-defined sprint plan through conversation before generating the full PRD with `/create-sprint`.

**Output:** Sprint plan document in `thoughts/sprint-plans/{datetime}_plan_{name}.md`

**Next Step:** Use `/create-sprint` to generate comprehensive PRD, tasks, and architecture validation from this plan.

---

## Step 1: Check for Existing Plans

Look for existing draft plans in `thoughts/sprint-plans/`:

```bash
ls -t thoughts/sprint-plans/*.md 2>/dev/null | head -5
```

If drafts exist, ask user:
- "Found existing draft plans. Continue with latest draft or start fresh?"
- If continue: Load the latest draft
- If fresh: Proceed to Step 2

---

## Step 2: Initial Sprint Discovery

**DO NOT proceed to detailed planning yet.** Start with high-level conversation.

Ask the user these **open-ended questions** (use AskUserQuestion for the first one only, then conversational flow):

### Question 1: Sprint Purpose
"What's the main goal or purpose of this sprint? What problem are you trying to solve or what value are you creating?"

**Listen for:**
- Business objectives vs. technical debt
- User-facing features vs. internal improvements
- New functionality vs. enhancements

### Question 2: Feature Ideas
"What features or tasks are you considering for this sprint? (Don't worry about order or detail yet - just brain dump)"

**Note:** User may not have organized thoughts. Accept rough ideas.

### Question 3: Success Criteria
"How will you know this sprint was successful? What does 'done' look like?"

**Listen for:**
- Specific deliverables
- User outcomes
- Technical milestones

---

## Step 3: Initial Draft Creation

Based on initial conversation, create first draft:

**File:** `thoughts/sprint-plans/{datetime}_draft_v1_{name}.md`

**Structure:**

```markdown
# Sprint Plan: {name}

**Status:** Draft v1
**Created:** {datetime}
**Last Updated:** {datetime}

## Sprint Goal

{1-2 sentence summary of main purpose}

## Features & Tasks (Unrefined)

{List everything mentioned, unsorted, no detail yet}

- Feature/task 1
- Feature/task 2
- ...

## Success Criteria

{What "done" looks like}

- Criterion 1
- Criterion 2

## Open Questions

{Things that need clarification}

- Question 1
- Question 2

## Story Points Estimate

**Total (rough):** TBD
**Note:** No time estimates - using story points only

## Next Steps

- [ ] Clarify scope and priorities
- [ ] Add detail to tasks
- [ ] Estimate story points
- [ ] Order by dependencies and value
```

Display to user:
```
📝 Created initial draft: thoughts/sprint-plans/{filename}

This is a rough first pass. Let's refine it together.
```

---

## Step 4: Iterative Refinement

**This is the core of the command.** Go through multiple rounds of clarification.

### Round 1: Scope and Priority

Review the feature list and ask:

**Clarifying Questions:**

1. **Scope validation:**
   - "Looking at this list, is anything missing that's critical for the sprint goal?"
   - "Is anything here that's actually nice-to-have rather than essential?"

2. **Priority discovery:**
   - "Which of these features is most important for achieving the sprint goal?"
   - "Are there any dependencies - does X need to be done before Y?"

3. **Complexity check:**
   - "Which of these tasks seems most complex or risky?"
   - "Any tasks here that you're uncertain how to implement?"

**Update draft to v2:**
- Add missing features
- Remove nice-to-haves (move to "Future Sprints" section)
- Add priority markers (P0, P1, P2)
- Note dependencies
- Flag complex/risky items

### Round 2: Detail and Breakdown

For each feature/task, ask for detail:

1. **What does it involve?**
   - "For [feature X], what are the main sub-tasks or components?"
   - "Does this touch frontend, backend, database, all of the above?"

2. **Acceptance criteria:**
   - "How will you know [feature X] is complete?"
   - "What should it do (and not do)?"

3. **Story points:**
   - "On a scale of 1 (trivial) to 13 (huge/complex), how would you size [feature X]?"
   - "For reference: 1=hours, 3=day, 5=2-3 days, 8=week, 13=needs breakdown"

**IMPORTANT:** If user provides time estimates, convert to story points:
- "I notice you mentioned time - let's use story points instead. If that's about 2 days of work, that's typically a 5. Sound right?"

**Update draft to v3:**
- Add sub-tasks for each feature
- Add acceptance criteria
- Add story points per task
- Calculate total story points
- Group by phase (Foundation, Core, Polish)

### Round 3: Validation and Ordering

Present the refined plan and ask:

1. **Feasibility:**
   - "Looking at {total story points} points total, does this feel achievable for one sprint?"
   - If > 40 points: "This seems ambitious. Should we prioritize and move some to a future sprint?"

2. **Ordering:**
   - "What order should we tackle these in?"
   - "Should we do riskiest-first or foundation-first?"

3. **Missing pieces:**
   - "Is there anything about testing, documentation, or deployment we should include?"
   - "Any technical debt to address while we're in this area?"

**Update draft to v4:**
- Reorder tasks by implementation sequence
- Add testing/docs tasks
- Adjust scope if too large
- Create "Future Sprint Backlog" section for deferred items

---

## Step 5: Final Review

Display the refined plan and ask:

**Final Confirmation:**

Use AskUserQuestion:
```
Question: "Is this sprint plan ready to move forward?"
Options:
  - "Yes, create the full sprint" → Proceed to Step 6
  - "No, needs more refinement" → Back to Step 4
  - "Save draft for later" → Exit with draft saved
```

If "needs more refinement":
- Ask: "What would you like to adjust or clarify?"
- Make updates
- Return to final review

---

## Step 6: Finalize Plan

Create final version:

**File:** `thoughts/sprint-plans/{datetime}_plan_{name}.md`

**Structure:**

```markdown
# Sprint Plan: {name}

**Status:** ✅ Ready for Implementation
**Created:** {created_date}
**Finalized:** {datetime}
**Story Points:** {total} points

## Sprint Goal

{Clear, concise goal statement}

## Scope

### In Scope
- Feature 1 (5 points)
- Feature 2 (3 points)
- Feature 3 (8 points)

**Total:** {total} story points

### Out of Scope (Future Sprints)
- Deferred feature A
- Nice-to-have B

## Feature Breakdown

### Phase 1: Foundation ({points} points)

#### Feature: {Name} ({points} points)
**Priority:** P0
**Dependencies:** None

**Sub-tasks:**
- [ ] Task 1 (2 points)
- [ ] Task 2 (3 points)

**Acceptance Criteria:**
- Criterion 1
- Criterion 2

**Technical Notes:**
- Implementation notes
- Risk factors

---

### Phase 2: Core Features ({points} points)

{Similar structure for each feature}

---

### Phase 3: Polish ({points} points)

{Testing, docs, error handling, logging}

## Success Criteria

- [ ] All P0 features complete
- [ ] All acceptance criteria met
- [ ] Tests passing
- [ ] Documentation updated

## Technical Considerations

**Architecture:**
- Key architectural decisions
- Technology choices

**Risks:**
- Risk 1: {description} → Mitigation: {approach}
- Risk 2: {description} → Mitigation: {approach}

**Dependencies:**
- External dependencies
- Internal dependencies

## Story Points Summary

| Phase | Points | % of Total |
|-------|--------|------------|
| Foundation | {n} | {%} |
| Core | {n} | {%} |
| Polish | {n} | {%} |
| **Total** | **{total}** | **100%** |

## Next Steps

1. Review this plan one final time
2. Run `/create-sprint` to generate comprehensive PRD with agent analysis
3. Run `/setup-jobs` to organize tasks by code co-location
4. Begin implementation in parallel worktrees

## Revision History

- v1 ({date}): Initial draft
- v2 ({date}): Scope and priority refinement
- v3 ({date}): Detail and story points added
- v4 ({date}): Ordering and final adjustments
- Final ({date}): Ready for implementation
```

Delete draft versions:
```bash
rm thoughts/sprint-plans/*_draft_*.md 2>/dev/null
```

---

## Output

Display completion message:

```
✅ Sprint Plan Finalized!

📋 Plan: thoughts/sprint-plans/{datetime}_plan_{name}.md
📊 Story Points: {total} points
🎯 {feature_count} features across 3 phases

Sprint Summary:
{sprint_goal}

Ready to proceed:
1. Review the plan: thoughts/sprint-plans/{filename}
2. When ready, run: /create-sprint

The /create-sprint command will:
- Generate comprehensive PRD with PM, UX, and Engineering agent input
- Create detailed todo list
- Validate architecture
- Set up for parallel development

Would you like to review the plan now or proceed with /create-sprint?
```

---

## Key Principles

**Conversational, Not Interrogative:**
- Natural back-and-forth dialogue
- Ask follow-up questions based on answers
- Acknowledge and build on user input
- Don't rush through questions mechanically

**Iterative Refinement:**
- Multiple passes (v1 → v2 → v3 → v4 → final)
- Each version gets more detailed
- User sees progress at each stage
- Save drafts between sessions

**No Time Estimates:**
- Always use story points
- If user mentions time, gently redirect to story points
- Explain: "Story points help us focus on complexity, not hours"

**Story Point Guide:**
- 1 point: Trivial (minutes to hours)
- 2 points: Simple (few hours)
- 3 points: Moderate (half to full day)
- 5 points: Significant (2-3 days)
- 8 points: Large (week of work)
- 13 points: Extra large (needs breakdown into smaller tasks)
- 21+ points: Too large (must break down)

**Scope Management:**
- Better to plan less and succeed than overcommit
- Move nice-to-haves to future sprints
- Typical sprint: 20-40 story points (solo developer)

**Detail Level:**
- Enough detail to start work confidently
- Not so detailed it becomes prescriptive
- Leave room for implementation decisions
- Focus on WHAT and WHY, not HOW (that comes in /create-sprint)

---

## Workflow Integration

```
[plan-sprint]  →  [create-sprint]  →  [setup-jobs]  →  [implement]  →  [retrospective]
     ↓                   ↓
 (interactive)      (agent-driven)
 (human-led)        (AI synthesis)
 (scope & goals)    (PRD & tasks)
```

**Before this command:**
- Rough ideas about what to build
- Unclear priorities
- Mixed up features and tasks

**After this command:**
- Clear sprint goal
- Prioritized features
- Story points estimated
- Ready for detailed PRD generation

---

## Tips for Users

**Have a Sprint Goal:**
- One clear objective per sprint
- Focused > scattered
- "Add user authentication" not "improve everything"

**Be Honest About Scope:**
- Solo developer: 20-30 points realistic
- Small team: 40-60 points realistic
- Include buffer for unexpected issues

**Use Story Points, Not Hours:**
- Hours are estimates that are always wrong
- Story points reflect relative complexity
- No pressure to "finish in X hours"

**Iterate Until Clear:**
- Don't rush to finalize
- Save draft and sleep on it
- Come back and refine
- Better to spend time planning than reworking

**Focus on Value:**
- What creates most user value?
- What unlocks other features?
- What reduces risk?

---

## Example Session

**User:** "I want to add a blog to my website"

**Assistant:** "Great! Let me understand the goal. What's the main reason you want to add a blog? Are you looking to improve SEO, share tutorials, build community, or something else?"

**User:** "Mostly for tutorials and SEO"

**Assistant:** "Perfect. What features are you thinking about for the blog? Just brain dump - we'll organize it later."

**User:** "Posts with markdown, tags, search, RSS feed, comments maybe"

**Assistant:** "Good list! How will you know the blog feature is successful?"

**User:** "When I can publish posts, people can find them via search, and share them"

**Assistant:** *Creates v1 draft*

"I've created an initial draft. Looking at this list, I notice 'comments' was mentioned - is that essential for the first sprint or could that be added later?"

**User:** "Later is fine"

**Assistant:** "Great, I'll move that to future sprints. Of the remaining features - posts, tags, search, RSS - which is most critical?"

**User:** "Posts for sure. Then tags. Search and RSS would be nice but not critical."

**Assistant:** *Updates to v2 with priorities*

"Let's break down 'Posts with markdown'. What does that involve?"

**User:** "Database schema, markdown parser, post editor, post display page"

**Assistant:** "How would you size that? Remember: 1=trivial, 3=half day, 5=2-3 days, 8=week, 13=too big"

**User:** "Maybe 8 points total?"

**Assistant:** "Let's break it down: database schema (2), markdown parser (3), editor (5), display page (3). That's 13 points just for posts - want to keep all in one sprint or split it?"

**User:** "Let's do schema, parser, and display (8 points) this sprint. Editor next sprint."

**Assistant:** *Updates to v3, continues refining...*

{After several rounds}

**Assistant:** "Here's the refined plan: Blog foundation sprint - 24 story points total. Phase 1: schema and models (5 pts), Phase 2: markdown rendering and display (8 pts), Phase 3: tags and basic search (7 pts), polish (4 pts). Does this feel achievable?"

**User:** "Yes!"

**Assistant:** ✅ Finalized! Run `/create-sprint` when ready.

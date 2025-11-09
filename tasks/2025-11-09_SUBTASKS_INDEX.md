# Sub-Tasks Index - Quick Reference

## Overview
24 sub-tasks created from 7 original jobs, organized for parallel execution with 3-4 developers.

**Total Story Points**: 76
**Estimated Time**: 26 days with 3 developers (vs 60 days sequential)
**Speedup**: 2.3x

---

## Quick Navigation

### By Batch

#### Batch 1: Infrastructure (10 SP, 3 days)
- [Sub1A: Dependencies Install](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub1a_dependencies_install.md) - 2 SP
- [Sub1B: State Schema](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub1b_state_schema.md) - 3 SP
- [Sub1C: Testing Infrastructure](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub1c_testing_infra.md) - 2 SP
- [Sub1D: Workflow Skeleton](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub1d_workflow_skeleton.md) - 3 SP

#### Batch 2: Planning Nodes (13 SP, 3 days) - HIGHLY PARALLEL
- [Sub2A: PM Planning Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub2a_pm_node.md) - 3 SP
- [Sub2B: UX Planning Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub2b_ux_node.md) - 3 SP
- [Sub2C: Engineering Planning Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub2c_eng_node.md) - 3 SP
- [Sub2D: Synthesis Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub2d_synthesis_node.md) - 4 SP

#### Batch 3: Gap Analysis (13 SP, 4 days)
- [Sub3A: Gap Analysis Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub3a_gap_analysis_node.md) - 5 SP
- [Sub3B: Conditional Routing](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub3b_conditional_routing.md) - 3 SP
- [Sub3C: Feedback Application](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub3c_feedback_application.md) - 3 SP
- [Sub3D: User Approval](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub3d_user_approval.md) - 2 SP

#### Batch 4: Job Creation (13 SP, 4 days)
- [Sub4A: PRD Generation](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub4a_prd_generation.md) - 3 SP
- [Sub4B: Job Creator Node](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub4b_job_creator_node.md) - 5 SP
- [Sub4C: Job Validation](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub4c_job_validation.md) - 3 SP
- [Sub4D: Worktree Setup](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub4d_worktree_setup.md) - 2 SP

#### Batch 5: Implementation (16 SP, 5 days) - HIGHLY PARALLEL
- [Sub5A: Parallel Implementation](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub5a_parallel_implementation.md) - 5 SP
- [Sub5B: Verification Loop](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub5b_verification_loop.md) - 5 SP
- [Sub5C: Retry & Error Handling](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub5c_retry_error_handling.md) - 4 SP
- [Sub5D: Verification Conditional](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub5d_verification_conditional.md) - 2 SP

#### Batch 6: Branch Management (13 SP, 4 days)
- [Sub7A: Branch Management](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub7a_branch_management.md) - 4 SP
- [Sub7B: Conflict Resolution](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub7b_conflict_resolution.md) - 3 SP
- [Sub7C: PR Creation & Merge](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub7c_pr_creation_merge.md) - 4 SP
- [Sub7D: Cleanup](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub7d_cleanup.md) - 2 SP

#### Batch 7: Integration (10 SP, 3 days) - HIGHLY PARALLEL
- [Sub8A: MCP Server](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub8a_mcp_server.md) - 3 SP
- [Sub8B: Command Updates](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub8b_command_updates.md) - 2 SP
- [Sub8C: Documentation](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub8c_documentation.md) - 2 SP
- [Sub8D: E2E Testing](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_sub8d_e2e_testing.md) - 3 SP

---

## By Parallelization Type

### Fully Parallelizable (9 tasks, 30 SP)
Can run completely in parallel with other tasks:
- Sub1C: Testing Infrastructure (parallel with 1B)
- Sub2A: PM Planning Node
- Sub2B: UX Planning Node
- Sub2C: Engineering Planning Node
- Sub3B: Conditional Routing (parallel with 3A)
- Sub3D: User Approval (parallel with 3C)
- Sub5A: Parallel Implementation
- Sub5B: Verification Loop
- Sub5C: Retry & Error Handling
- Sub7B: Conflict Resolution (helpers, fully parallel)
- Sub8A: MCP Server
- Sub8B: Command Updates
- Sub8C: Documentation

### Partially Parallelizable (3 tasks, 10 SP)
Can start in parallel but need dependencies later:
- Sub1B: State Schema (after 1A, parallel with 1C)
- Sub4B: Job Creator Node (can start with 4A, needs PRD output)
- Sub4D: Worktree Setup (after 4B, parallel with 4C)
- Sub7D: Cleanup (after 7C, can run during)

### Sequential Only (12 tasks, 36 SP)
Must wait for dependencies:
- Sub1A: Dependencies Install (foundation)
- Sub1D: Workflow Skeleton (needs 1B+1C)
- Sub2D: Synthesis Node (needs 2A+2B+2C)
- Sub3A: Gap Analysis Node (needs 2D)
- Sub3C: Feedback Application (needs 3A)
- Sub4A: PRD Generation (needs 3A/3C)
- Sub4C: Job Validation (needs 4B)
- Sub5D: Verification Conditional (needs 5A+5B+5C)
- Sub7A: Branch Management (needs 5D)
- Sub7C: PR Creation & Merge (needs 7A)
- Sub8D: E2E Testing (needs 8A+8B+8C)

---

## By Skill Required

### Python/LangGraph Expertise
- Sub1B: State Schema (TypedDict definitions)
- Sub1D: Workflow Skeleton (StateGraph construction)
- Sub2D: Synthesis Node (data merging)
- Sub5D: Verification Conditional (decision logic)
- Sub8A: MCP Server (JSON-RPC protocol)

### Anthropic API Integration
- Sub2A: PM Planning Node
- Sub2B: UX Planning Node
- Sub2C: Engineering Planning Node
- Sub3A: Gap Analysis Node
- Sub4B: Job Creator Node

### Git/DevOps
- Sub4D: Worktree Setup
- Sub7A: Branch Management
- Sub7B: Conflict Resolution
- Sub7C: PR Creation & Merge
- Sub7D: Cleanup

### Testing/QA
- Sub1C: Testing Infrastructure
- Sub5B: Verification Loop
- Sub5C: Retry & Error Handling
- Sub8D: E2E Testing

### Documentation
- Sub8C: Documentation (LANGGRAPH.md, migration guide, etc.)

---

## Critical Path (Longest Chain)

**47 story points, 26 days with 3 developers**

```
1A (2) → 1B (3) → 1D (3) → 2A (3) → 2D (4) → 3A (5) → 3C (3) →
4A (3) → 4B (5) → 4C (3) → 5A (5) → 5D (2) → 7A (4) → 7C (4) →
8A (3) → 8D (3)
```

---

## Daily Assignments (3 Developers)

### Week 1: Days 1-7

**Day 1-2**:
- Dev 1: Sub1A → Sub1B (start)
- Dev 2: Sub1A → Sub1C (start)
- Dev 3: Standy / Review

**Day 3**:
- Dev 1: Sub1B (complete)
- Dev 2: Sub1C (complete)
- Dev 3: Sub1D (start, needs 1B+1C)

**Day 4-5**:
- Dev 1: Sub2A (PM node)
- Dev 2: Sub2B (UX node)
- Dev 3: Sub1D (complete) → Sub2C (Eng node)

**Day 6-7**:
- Dev 1: Sub2A (complete)
- Dev 2: Sub2B (complete)
- Dev 3: Sub2C (complete) → Sub2D (Synthesis)

### Week 2: Days 8-14

**Day 8-10**:
- Dev 1: Sub3A (Gap Analysis)
- Dev 2: Sub3B (Conditional Routing)
- Dev 3: Wait for 3A

**Day 11**:
- Dev 1: Sub3A (complete) → Sub4A (PRD Gen)
- Dev 2: Sub3B (complete)
- Dev 3: Sub3C (Feedback App) + Sub3D (User Approval)

**Day 12-13**:
- Dev 1: Sub4A (complete) → Sub4B (Job Creator)
- Dev 2: Wait for 4B
- Dev 3: Sub3C/3D (complete)

**Day 14**:
- Dev 1: Sub4B (complete)
- Dev 2: Sub4C (Job Validation)
- Dev 3: Sub4D (Worktree Setup)

### Week 3: Days 15-23

**Day 15-18**:
- Dev 1: Sub5A (Parallel Implementation)
- Dev 2: Sub5B (Verification Loop)
- Dev 3: Sub5C (Retry/Error Handling)

**Day 19**:
- Dev 1: Sub5A (complete)
- Dev 2: Sub5B (complete)
- Dev 3: Sub5C (complete) → Sub5D (Conditional)

**Day 20-21**:
- Dev 1: Sub7A (Branch Management)
- Dev 2: Sub7B (Conflict Resolution)
- Dev 3: Sub5D (complete) → Wait for 7A

**Day 22-23**:
- Dev 1: Sub7A (complete)
- Dev 2: Sub7B (complete)
- Dev 3: Sub7C (PR & Merge) + Sub7D (Cleanup)

### Week 4: Days 24-26

**Day 24-25**:
- Dev 1: Sub8A (MCP Server)
- Dev 2: Sub8B (Command Updates)
- Dev 3: Sub8C (Documentation)

**Day 26**:
- Dev 1: Sub8A (complete) → Sub8D (E2E Testing)
- Dev 2: Sub8B (complete) → Sub8D (assist)
- Dev 3: Sub8C (complete) → Sub8D (assist)

---

## File Checklist

All sub-task files are in: `/home/justin/Documents/dev/claude-code-plugins/tasks/`

**Infrastructure (Batch 1)**:
- [x] 2025-11-09_sub1a_dependencies_install.md
- [x] 2025-11-09_sub1b_state_schema.md
- [x] 2025-11-09_sub1c_testing_infra.md
- [x] 2025-11-09_sub1d_workflow_skeleton.md

**Planning (Batch 2)**:
- [x] 2025-11-09_sub2a_pm_node.md
- [x] 2025-11-09_sub2b_ux_node.md
- [x] 2025-11-09_sub2c_eng_node.md
- [x] 2025-11-09_sub2d_synthesis_node.md

**Gap Analysis (Batch 3)**:
- [x] 2025-11-09_sub3a_gap_analysis_node.md
- [x] 2025-11-09_sub3b_conditional_routing.md
- [x] 2025-11-09_sub3c_feedback_application.md
- [x] 2025-11-09_sub3d_user_approval.md

**Job Creation (Batch 4)**:
- [x] 2025-11-09_sub4a_prd_generation.md
- [x] 2025-11-09_sub4b_job_creator_node.md
- [x] 2025-11-09_sub4c_job_validation.md
- [x] 2025-11-09_sub4d_worktree_setup.md

**Implementation (Batch 5)**:
- [x] 2025-11-09_sub5a_parallel_implementation.md
- [x] 2025-11-09_sub5b_verification_loop.md
- [x] 2025-11-09_sub5c_retry_error_handling.md
- [x] 2025-11-09_sub5d_verification_conditional.md

**Branch Management (Batch 6)**:
- [x] 2025-11-09_sub7a_branch_management.md
- [x] 2025-11-09_sub7b_conflict_resolution.md
- [x] 2025-11-09_sub7c_pr_creation_merge.md
- [x] 2025-11-09_sub7d_cleanup.md

**Integration (Batch 7)**:
- [x] 2025-11-09_sub8a_mcp_server.md
- [x] 2025-11-09_sub8b_command_updates.md
- [x] 2025-11-09_sub8c_documentation.md
- [x] 2025-11-09_sub8d_e2e_testing.md

**Summary Documents**:
- [x] 2025-11-09_PARALLELIZATION_SUMMARY.md
- [x] 2025-11-09_EXECUTION_TIMELINE.md
- [x] 2025-11-09_SUBTASKS_INDEX.md (this file)

---

## Next Steps

1. **Review Strategy**: Read [PARALLELIZATION_SUMMARY.md](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_PARALLELIZATION_SUMMARY.md)
2. **Check Timeline**: Review [EXECUTION_TIMELINE.md](/home/justin/Documents/dev/claude-code-plugins/tasks/2025-11-09_EXECUTION_TIMELINE.md)
3. **Assign Developers**: Allocate sub-tasks based on skill matrix
4. **Start Batch 1**: Begin with Sub1A (dependencies install)
5. **Daily Standups**: Track progress against timeline
6. **Adjust as Needed**: Reallocate resources if bottlenecks appear

---

## Contact & Support

For questions about specific sub-tasks, refer to the individual task files linked above. Each file contains:
- Complete scope and todos
- Implementation notes and code examples
- Dependencies and blockers
- Success criteria
- Story point estimate

**Total Implementation**: 24 sub-tasks, 76 story points, 26 days (3 devs) = 2.3x faster than sequential

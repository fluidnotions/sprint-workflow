# Sprint: LangGraph Migration
Generated: 2025-11-09
Sprint PRD: thoughts/sprint-plans/claude-code-plugins/2025-11-09_prd_langgraph_migration.md

## Phase 1: Infrastructure (Week 1) - 8 Story Points

### Setup & Dependencies
- [ ] Install LangGraph dependencies (langgraph, langchain-anthropic, langchain-core)
- [ ] Update requirements.txt with new dependencies
- [ ] Create installation script for LangGraph (scripts/install_langgraph.sh)
- [ ] Verify ANTHROPIC_API_KEY environment variable setup

### State Schema
- [ ] Create langgraph/state.py module
- [ ] Define SprintWorkflowState TypedDict with all fields
- [ ] Define JobSpec TypedDict for job specifications
- [ ] Define RepoInfo TypedDict for repository information
- [ ] Define ErrorRecord TypedDict for error tracking
- [ ] Add type hints and documentation for all state fields

### Workflow Graph Skeleton
- [ ] Create langgraph/workflow.py module
- [ ] Implement build_workflow() function returning StateGraph
- [ ] Add all node definitions (stubs initially)
- [ ] Define edges between nodes
- [ ] Add conditional edges for feedback loops
- [ ] Configure MemorySaver checkpointing

### Testing Infrastructure
- [ ] Create tests/langgraph/ directory
- [ ] Set up pytest configuration
- [ ] Create test_state.py for state schema tests
- [ ] Create test_workflow.py for workflow graph tests
- [ ] Implement basic workflow execution test with dummy state
- [ ] Add CI/CD configuration for tests

## Phase 2: Planning Nodes (Week 2) - 13 Story Points

### Product Manager Node
- [ ] Create langgraph/nodes/planning.py module
- [ ] Extract PM prompt from agents/product-manager.md
- [ ] Implement pm_planning() node function
- [ ] Create parse_pm_response() helper for output parsing
- [ ] Add PM output to state schema
- [ ] Write unit tests for PM node

### UX Designer Node
- [ ] Extract UX prompt from agents/ux-designer.md
- [ ] Implement ux_planning() node function
- [ ] Create parse_ux_response() helper for output parsing
- [ ] Add UX output to state schema
- [ ] Write unit tests for UX node
- [ ] Test parallel execution with PM node

### Senior Engineer Node
- [ ] Extract Engineering prompt from agents/senior-engineer.md
- [ ] Implement engineering_planning() node function
- [ ] Create parse_engineering_response() helper for output parsing
- [ ] Add Engineering output to state schema
- [ ] Write unit tests for Engineering node
- [ ] Test parallel execution of all three planning nodes

### Synthesis Node
- [ ] Implement synthesize_planning() node function
- [ ] Combine PM + UX + Engineering outputs into unified plan
- [ ] Generate intermediate planning document
- [ ] Add synthesis output to state schema
- [ ] Write unit tests for synthesis node
- [ ] Test end-to-end planning phase (PM+UX+Eng → synthesis)

## Phase 3: Gap Analysis Loop (Week 3) - 13 Story Points

### Gap Analysis Node
- [ ] Create langgraph/nodes/validation.py module
- [ ] Extract gap analyzer prompt from agents/gap-analyzer.md
- [ ] Implement gap_analysis() node function
- [ ] Add web search integration for best practices research
- [ ] Create parse_gap_analysis() helper for recommendations
- [ ] Add gap_analysis output to state schema
- [ ] Write unit tests for gap analysis node

### Conditional Edge Logic
- [ ] Implement should_apply_gap_feedback() decision function
- [ ] Add retry_counts tracking to state schema
- [ ] Configure max retry limit (3 iterations)
- [ ] Add conditional edge to workflow graph
- [ ] Test conditional routing (approved vs apply_feedback vs max_retries)

### Feedback Application Node
- [ ] Implement update_planning_from_feedback() node function
- [ ] Merge gap analysis recommendations into PM output
- [ ] Merge recommendations into UX output
- [ ] Merge recommendations into Engineering output
- [ ] Track feedback history in state
- [ ] Write unit tests for feedback application

### User Approval Mechanism
- [ ] Add user interaction callback for feedback approval
- [ ] Implement approval prompt with recommendations display
- [ ] Handle user response (yes/no/customize)
- [ ] Add approval decision to state
- [ ] Test feedback loop with simulated issues
- [ ] Test max retry escape condition

## Phase 4: Job Creation (Week 4) - 13 Story Points

### PRD Generation Node
- [ ] Create langgraph/nodes/artifacts.py module
- [ ] Implement generate_sprint_prd() node function
- [ ] Synthesize PM + UX + Engineering + Gap Analysis into PRD
- [ ] Write PRD to thoughts/sprint-plans/{project}/ directory
- [ ] Generate todos from PRD user stories
- [ ] Add sprint_prd_path and todos_path to state schema

### Job Creator Node
- [ ] Create langgraph/nodes/jobs.py module
- [ ] Extract job creator prompt from agents/job-creator.md
- [ ] Implement create_jobs() node function
- [ ] Analyze code co-location for todo grouping
- [ ] Generate task files in tasks/ directory
- [ ] Add jobs list to state schema
- [ ] Write unit tests for job creation

### Job Validation Node
- [ ] Implement validate_jobs() node function
- [ ] Run gap analysis on each job specification
- [ ] Identify missing components per job
- [ ] Calculate story points per job
- [ ] Add job validation results to state
- [ ] Write unit tests for job validation

### Job Feedback Loop
- [ ] Implement should_apply_job_feedback() decision function
- [ ] Implement update_jobs_from_feedback() node function
- [ ] Add conditional edge for job validation loop
- [ ] Test job feedback loop with simulated issues
- [ ] Test max retry escape condition

### Worktree Setup Node
- [ ] Implement setup_git_worktrees() node function
- [ ] Create git branches for each job
- [ ] Set up worktrees in worktrees/ directory
- [ ] Detect repository roots for each worktree
- [ ] Copy environment files to worktrees
- [ ] Test worktree setup with multi-repo scenarios

## Phase 5-6: Implementation & Verification (Week 5-6) - 21 Story Points

### Parallel Implementation Node
- [ ] Create langgraph/nodes/execution.py module
- [ ] Implement parallel_implementation() node function
- [ ] Batch jobs by pool_size for parallel execution
- [ ] Spawn implementation agents using asyncio.gather()
- [ ] Track implementing jobs in state
- [ ] Write unit tests for parallel batching logic

### Implementation Agent Spawning
- [ ] Implement spawn_implementation_agent() async function
- [ ] Read job specification and Sprint PRD
- [ ] Construct implementation prompt with context
- [ ] Integrate with Claude Code agent spawning (via Task tool or API)
- [ ] Handle agent output and status updates
- [ ] Test implementation agent spawning

### Verification Loop Node
- [ ] Implement verification_loop() node function
- [ ] Define verify_job() async function for individual job verification
- [ ] Run tests in job worktree
- [ ] Check code quality standards
- [ ] Validate acceptance criteria completion
- [ ] Track verification results in state

### Retry Logic
- [ ] Implement retry counter per job
- [ ] Generate verification feedback for failed jobs
- [ ] Re-spawn implementation agent with feedback
- [ ] Track retry iterations (max 5)
- [ ] Test retry loop with simulated failures

### Error Handling
- [ ] Implement non-blocking failure handling
- [ ] Mark jobs as failed after max retries
- [ ] Generate error reports (write_error_report helper)
- [ ] Add errors to state.errors list
- [ ] Continue sprint execution despite failures
- [ ] Write unit tests for error handling

### Verification Conditional Edge
- [ ] Implement should_continue_verification() decision function
- [ ] Check for jobs still implementing or verifying
- [ ] Route to retry or continue to branch management
- [ ] Test verification loop termination conditions
- [ ] Test mixed scenarios (some verified, some failed, some implementing)

## Phase 7: Branch Management (Week 7) - 13 Story Points

### Branch Management Node
- [ ] Create langgraph/nodes/git.py module
- [ ] Implement manage_branches() node function
- [ ] Group jobs by repository root
- [ ] Spawn manage_repo_branches() per repo in parallel
- [ ] Track branch management status in state
- [ ] Write unit tests for branch management

### Repository Branch Updates
- [ ] Implement manage_repo_branches() async function
- [ ] Fetch latest from origin
- [ ] Rebase each branch on origin/main
- [ ] Detect merge conflicts
- [ ] Track branch update results

### Conflict Resolution
- [ ] Implement auto_resolve_conflicts() helper
- [ ] Handle non-code file conflicts (accept incoming)
- [ ] Apply conflict resolution heuristics for code
- [ ] Flag complex conflicts for manual intervention
- [ ] Add conflict errors to state
- [ ] Test conflict resolution with simulated conflicts

### PR Creation & Merging Node
- [ ] Implement push_and_merge() node function
- [ ] Detect repositories with remote vs local-only
- [ ] Push branches to origin for remote repos
- [ ] Create PRs using gh CLI (create_pr helper)
- [ ] Generate PR descriptions from job specs
- [ ] Write unit tests for PR creation

### Auto-Merge Logic
- [ ] Implement check_pr_tests() helper to wait for CI
- [ ] Auto-merge PRs when tests pass (merge_pr helper)
- [ ] Handle local-only repo merges (merge_local helper)
- [ ] Track merge status in state
- [ ] Flag failed tests for manual review
- [ ] Test auto-merge with simulated PR scenarios

### Cleanup
- [ ] Remove merged worktrees (git worktree remove)
- [ ] Delete merged branches (git branch -d)
- [ ] Track cleanup status
- [ ] Handle cleanup errors gracefully

## Phase 8: Integration & Testing (Week 8) - 8 Story Points

### MCP Server Updates
- [ ] Update mcp-servers/langgraph_sprint_executor.py
- [ ] Implement execute_planning tool (planning phase only)
- [ ] Implement execute_sprint tool (full workflow)
- [ ] Implement get_sprint_state tool (state inspection)
- [ ] Implement resume_sprint tool (checkpoint resumption)
- [ ] Add state visualization helper
- [ ] Test all MCP tools

### Command Updates
- [ ] Update commands/create-sprint.md to use execute_planning
- [ ] Update commands/setup-jobs.md to use execute_sprint
- [ ] Add --use-langgraph flag for opt-in
- [ ] Keep agent-based fallback working
- [ ] Test command integration
- [ ] Update command documentation

### End-to-End Testing
- [ ] Create test project for sprint execution
- [ ] Test full sprint workflow (planning → implementation → merge)
- [ ] Test multi-repo scenarios
- [ ] Test error recovery and resumption
- [ ] Test checkpoint-based resume
- [ ] Validate non-blocking failure handling
- [ ] Performance benchmark (parallel speedup)

### Documentation
- [ ] Update LANGGRAPH.md with new architecture
- [ ] Create migration guide for users
- [ ] Document all LangGraph nodes
- [ ] Add troubleshooting section
- [ ] Create developer guide for contributors
- [ ] Document MCP tool usage
- [ ] Add mermaid workflow diagrams
- [ ] Write release notes

---

**Total Tasks**: 120 tasks
**Story Points**: 89 points
**Estimated Completion**: 8 parallel jobs running simultaneously

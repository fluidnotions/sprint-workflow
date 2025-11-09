# Sub-Task 8D: End-to-End Testing & Validation

## Parent Job
Week 8: Integration & Testing

## Story Points
3

## Scope
Create comprehensive end-to-end test suite, test multi-repo scenarios, validate error recovery, and benchmark performance.

## Can Run in Parallel
NO - Depends on 8A, 8B, 8C (needs complete implementation + docs)

## Todos
- [ ] Create test project for sprint execution
- [ ] Test full sprint workflow (planning → implementation → merge)
- [ ] Test multi-repo scenarios
- [ ] Test error recovery and resumption
- [ ] Test checkpoint-based resume
- [ ] Validate non-blocking failure handling
- [ ] Performance benchmark (parallel speedup)
- [ ] Create automated test suite
- [ ] Document test scenarios

## Files to Create/Modify
- sprint-workflow/tests/e2e/test_full_sprint.py (new)
- sprint-workflow/tests/e2e/test_multi_repo.py (new)
- sprint-workflow/tests/e2e/test_error_recovery.py (new)
- sprint-workflow/tests/e2e/test_resumability.py (new)
- sprint-workflow/tests/e2e/benchmark.py (new)
- sprint-workflow/tests/e2e/README.md (new)

## Dependencies
- Sub-task 8A (needs MCP server)
- Sub-task 8B (needs command integration)
- Sub-task 8C (needs documentation for test scenarios)

## Blocks
- None (final validation step)

## Implementation Notes
```python
# tests/e2e/test_full_sprint.py

async def test_full_sprint_execution():
    """Test complete sprint workflow end-to-end."""
    # Setup test project
    test_project = create_test_project()

    # Execute planning
    planning_result = await execute_planning(
        sprint_theme="test_feature",
        project_name="test_project"
    )

    assert planning_result["status"] == "planning_complete"
    assert "synthesis_output" in planning_result

    # Generate PRD and todos (simulated)
    prd_path = "test_prd.md"
    todos_path = "test_todos.md"

    # Execute full sprint
    sprint_result = await execute_sprint(
        sprint_theme="test_feature",
        project_name="test_project",
        sprint_prd_path=prd_path,
        todos_path=todos_path,
        pool_size=2
    )

    # Validate results
    assert sprint_result["status"] == "sprint_complete"
    assert len(sprint_result["verified_jobs"]) >= 1
    assert len(sprint_result["failed_jobs"]) == 0

    # Verify artifacts created
    assert os.path.exists("thoughts/sprint-plans/test_project/")
    assert os.path.exists("tasks/")

    # Verify branches merged
    branches = subprocess.run(
        ["git", "branch"],
        capture_output=True,
        text=True
    ).stdout

    assert "feat/" not in branches  # Cleaned up

    # Cleanup
    cleanup_test_project(test_project)


# tests/e2e/test_multi_repo.py

async def test_multi_repo_sprint():
    """Test sprint with multiple repository roots."""
    # Setup project with multiple repos
    test_project = create_multi_repo_test_project()

    # Execute sprint
    sprint_result = await execute_sprint(
        sprint_theme="multi_repo_test",
        project_name="test_multi",
        sprint_prd_path="test_prd.md",
        todos_path="test_todos.md",
        pool_size=2
    )

    # Validate each repo handled correctly
    merge_status = sprint_result["merge_status"]

    repo1_merges = [m for m in merge_status if "repo1" in m.get("pr_url", "")]
    repo2_merges = [m for m in merge_status if "repo2" in m.get("pr_url", "")]

    assert len(repo1_merges) >= 1
    assert len(repo2_merges) >= 1

    # Cleanup
    cleanup_test_project(test_project)


# tests/e2e/test_error_recovery.py

async def test_error_recovery():
    """Test sprint handles job failures gracefully."""
    # Setup project with intentionally failing job
    test_project = create_test_project_with_failing_job()

    # Execute sprint
    sprint_result = await execute_sprint(
        sprint_theme="error_test",
        project_name="test_error",
        sprint_prd_path="test_prd.md",
        todos_path="test_todos.md",
        pool_size=2
    )

    # Validate non-blocking failure
    assert sprint_result["status"] == "sprint_complete"
    assert len(sprint_result["failed_jobs"]) >= 1
    assert len(sprint_result["verified_jobs"]) >= 1  # Other jobs succeeded

    # Verify error report generated
    error_reports = glob.glob("sprint_errors_*.md")
    assert len(error_reports) >= 1

    # Verify failed worktree preserved
    failed_job = sprint_result["failed_jobs"][0]
    worktree_path = f"worktrees/feat-{failed_job}"
    assert os.path.exists(worktree_path)

    # Cleanup
    cleanup_test_project(test_project)


# tests/e2e/test_resumability.py

async def test_checkpoint_resume():
    """Test sprint can resume from checkpoint."""
    # Setup project
    test_project = create_test_project()

    thread_id = "resume_test_sprint"

    # Start sprint
    workflow = build_workflow()
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "sprint_theme": "resume_test",
        "project_name": "test_resume",
        "sprint_prd_path": "test_prd.md",
        "todos_path": "test_todos.md",
        "pool_size": 2,
        "phase": "init"
    }

    # Run partially (interrupt during implementation)
    try:
        await workflow.ainvoke(
            initial_state,
            config,
            interrupt_before=["verification_loop"]
        )
    except Exception:
        pass  # Expected interruption

    # Get state
    state = await get_sprint_state(thread_id)
    assert state["phase"] in ["implementation_started", "implementing"]

    # Resume sprint
    resume_result = await resume_sprint(thread_id)

    assert resume_result["status"] == "resumed"
    assert resume_result["phase"] in ["sprint_complete", "merging_complete"]

    # Cleanup
    cleanup_test_project(test_project)


# tests/e2e/benchmark.py

async def benchmark_parallel_execution():
    """Benchmark parallel vs sequential execution."""
    test_project = create_benchmark_project()

    # Sequential (pool_size=1)
    start = time.time()
    await execute_sprint(
        sprint_theme="benchmark_seq",
        project_name="bench_seq",
        sprint_prd_path="bench_prd.md",
        todos_path="bench_todos.md",
        pool_size=1
    )
    sequential_time = time.time() - start

    # Parallel (pool_size=3)
    start = time.time()
    await execute_sprint(
        sprint_theme="benchmark_par",
        project_name="bench_par",
        sprint_prd_path="bench_prd.md",
        todos_path="bench_todos.md",
        pool_size=3
    )
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time

    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Parallel: {parallel_time:.2f}s")
    print(f"Speedup: {speedup:.2f}x")

    # Should achieve ~2.5x speedup with pool_size=3
    assert speedup >= 2.0, f"Expected >= 2x speedup, got {speedup:.2f}x"

    # Cleanup
    cleanup_test_project(test_project)
```

## Success Criteria
- Full sprint E2E test passing
- Multi-repo test passing
- Error recovery test passing
- Resumability test passing
- Performance benchmark >= 2x speedup
- All test scenarios documented
- Automated test suite complete
- CI/CD integration working

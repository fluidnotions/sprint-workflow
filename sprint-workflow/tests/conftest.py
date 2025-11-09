"""Root conftest.py for LangGraph sprint workflow tests.

Provides shared fixtures and configuration for all tests.
"""

import pytest
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock, patch


# ============================================================================
# STATE FIXTURES
# ============================================================================

@pytest.fixture
def sample_sprint_state() -> Dict[str, Any]:
    """Sample SprintWorkflowState for testing.

    Returns a minimal valid state that can be used as a starting point
    for tests. Tests can modify this as needed.
    """
    return {
        "sprint_theme": "Test Feature Sprint",
        "project_name": "test-project",
        "features": ["Feature A", "Feature B"],
        "pool_size": 3,
        "phase": "init",
        "retry_counts": {},
        "jobs": [],
        "jobs_implementing": [],
        "jobs_verifying": [],
        "jobs_verified": [],
        "jobs_failed": [],
        "repos": [],
        "worktrees": [],
        "branch_status": [],
        "merge_status": [],
        "errors": [],
        "started_at": datetime.now().isoformat(),
        "checkpoints": [],
        "status_messages": [],
    }


@pytest.fixture
def sample_job_spec() -> Dict[str, Any]:
    """Sample JobSpec for testing."""
    return {
        "name": "test-job",
        "task_file": "tasks/2025-11-09_test_job.md",
        "worktree": "worktrees/feat/test-job",
        "repo_root": "/fake/repo",
        "branch": "feat/test-job",
        "todos": [
            "Implement feature X",
            "Add tests for feature X",
            "Update documentation",
        ],
        "story_points": 5,
        "status": "pending",
        "retry_count": 0,
        "error_message": None,
        "files_to_modify": ["src/feature.py", "tests/test_feature.py"],
        "dependencies": [],
    }


@pytest.fixture
def sample_repo_info() -> Dict[str, Any]:
    """Sample RepoInfo for testing."""
    return {
        "path": "/fake/repo",
        "has_remote": True,
        "branches": ["main", "feat/test-job"],
        "default_branch": "main",
    }


# ============================================================================
# ANTHROPIC API MOCKS
# ============================================================================

@pytest.fixture
def mock_anthropic_response():
    """Mock response from Anthropic API."""
    return {
        "id": "msg_test123",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "This is a mock response from Claude."
            }
        ],
        "model": "claude-opus-4",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50
        }
    }


@pytest.fixture
def mock_anthropic_client(mock_anthropic_response):
    """Mock Anthropic AsyncAnthropic client.

    Returns a mock client where messages.create() returns a mock response.
    """
    mock_client = AsyncMock()
    mock_message = Mock()
    mock_message.content = [Mock(text="This is a mock response from Claude.")]
    mock_message.model = "claude-opus-4"
    mock_message.id = "msg_test123"

    mock_client.messages.create = AsyncMock(return_value=mock_message)

    with patch('anthropic.AsyncAnthropic', return_value=mock_client):
        yield mock_client


@pytest.fixture
def mock_anthropic_stream():
    """Mock streaming response from Anthropic API."""
    async def mock_stream():
        """Async generator for streaming response."""
        chunks = [
            "This ",
            "is ",
            "a ",
            "streaming ",
            "response."
        ]
        for chunk in chunks:
            yield Mock(content=[Mock(text=chunk)])

    return mock_stream


# ============================================================================
# WEB SEARCH MOCKS
# ============================================================================

@pytest.fixture
def mock_web_search():
    """Mock web search function for gap analysis.

    Returns a function that can be called with a search query
    and returns mock search results.
    """
    def _search(query: str) -> str:
        """Mock search function."""
        return f"""
        Mock search results for: "{query}"

        Result 1: Best practices for {query}
        Result 2: Common pitfalls in {query}
        Result 3: Latest trends in {query}
        """

    return _search


@pytest.fixture
def mock_brave_search():
    """Mock Brave Search MCP tool."""
    def _brave_search(query: str, count: int = 5) -> List[Dict[str, str]]:
        """Mock Brave search."""
        return [
            {
                "title": f"Result {i+1} for {query}",
                "url": f"https://example.com/result-{i+1}",
                "description": f"Mock description for result {i+1}"
            }
            for i in range(count)
        ]

    return _brave_search


# ============================================================================
# GIT MOCKS
# ============================================================================

@pytest.fixture
def mock_git_commands():
    """Mock git command execution.

    Returns a mock that simulates successful git operations.
    """
    mock_git = Mock()
    mock_git.return_value.returncode = 0
    mock_git.return_value.stdout = b"Success"
    mock_git.return_value.stderr = b""

    with patch('subprocess.run', mock_git):
        yield mock_git


@pytest.fixture
def mock_worktree_setup():
    """Mock git worktree setup operations."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = b"Worktree created successfully"
        yield mock_run


# ============================================================================
# FILE SYSTEM MOCKS
# ============================================================================

@pytest.fixture
def mock_file_operations(tmp_path):
    """Mock file operations using tmp_path.

    Provides a temporary directory for file operations during tests.
    """
    # Create test directories
    (tmp_path / "tasks").mkdir()
    (tmp_path / "worktrees").mkdir()
    (tmp_path / "thoughts/sprint-plans").mkdir(parents=True)

    return tmp_path


@pytest.fixture
def sample_task_file(mock_file_operations):
    """Create a sample task file for testing."""
    task_file = mock_file_operations / "tasks" / "2025-11-09_test_job.md"
    task_file.write_text("""# Job: test-job

## Overview
Test job specification for unit tests.

## Story Points
5

## Todos from Sprint
- [ ] Implement feature X
- [ ] Add tests for feature X
- [ ] Update documentation

## Success Criteria
- All todos complete
- Tests passing
""")
    return str(task_file)


# ============================================================================
# LANGGRAPH MOCKS
# ============================================================================

@pytest.fixture
def mock_state_graph():
    """Mock LangGraph StateGraph."""
    mock_graph = Mock()
    mock_graph.add_node = Mock()
    mock_graph.add_edge = Mock()
    mock_graph.add_conditional_edges = Mock()
    mock_graph.compile = Mock()

    with patch('langgraph.graph.StateGraph', return_value=mock_graph):
        yield mock_graph


@pytest.fixture
def mock_checkpointer():
    """Mock LangGraph MemorySaver checkpointer."""
    mock_checkpointer = Mock()
    mock_checkpointer.get = AsyncMock(return_value=None)
    mock_checkpointer.put = AsyncMock()

    with patch('langgraph.checkpoint.memory.MemorySaver', return_value=mock_checkpointer):
        yield mock_checkpointer


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (fast, no external deps)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "asyncio: mark test as using asyncio"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add 'unit' marker to all tests by default
        if not any(mark.name in ['integration', 'slow'] for mark in item.iter_markers()):
            item.add_marker(pytest.mark.unit)

        # Add 'asyncio' marker to async tests
        if "async" in item.name or "await" in str(item.function):
            item.add_marker(pytest.mark.asyncio)

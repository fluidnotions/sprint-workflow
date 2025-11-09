# Sub-Task 1C: Testing Infrastructure

## Parent Job
Week 1: Infrastructure & State Schema

## Story Points
2

## Scope
Set up pytest infrastructure, test directory structure, and CI/CD configuration for LangGraph testing.

## Can Run in Parallel
YES - Parallel with 1B completely, after 1A completes

## Todos
- [ ] Create tests/langgraph/ directory structure
- [ ] Set up pytest configuration (pytest.ini)
- [ ] Create conftest.py with fixtures for state mocking
- [ ] Configure test discovery patterns
- [ ] Add CI/CD configuration for tests
- [ ] Create mock factories for Anthropic API responses
- [ ] Test pytest execution with sample test

## Files to Create/Modify
- sprint-workflow/tests/pytest.ini (new)
- sprint-workflow/tests/conftest.py (new)
- sprint-workflow/tests/langgraph/conftest.py (new)
- sprint-workflow/.github/workflows/test.yml (new or modify)

## Dependencies
- Sub-task 1A (needs pytest dependency)

## Blocks
- All testing sub-tasks (2B, 2D, 3C, 4D, etc.)

## Implementation Notes
```python
# conftest.py key fixtures
@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic API client."""
    with patch('anthropic.AsyncAnthropic') as mock:
        yield mock

@pytest.fixture
def sample_state():
    """Sample SprintWorkflowState for testing."""
    return {
        "sprint_theme": "test_feature",
        "project_name": "test_project",
        "pool_size": 2,
        "phase": "init",
        "errors": []
    }

@pytest.fixture
def mock_web_search():
    """Mock web search results."""
    def _search(query):
        return f"Mock results for: {query}"
    return _search
```

## Success Criteria
- pytest runs successfully
- Test discovery working
- Fixtures available for all test files
- CI/CD pipeline configured
- Mock factories functional
- Sample test passes

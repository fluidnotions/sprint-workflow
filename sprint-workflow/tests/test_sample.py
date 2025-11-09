"""Sample test to verify pytest infrastructure is working."""

import pytest


class TestPytestInfrastructure:
    """Tests to verify pytest setup is working correctly."""

    def test_basic_assertion(self):
        """Test that basic assertions work."""
        assert True
        assert 1 + 1 == 2
        assert "hello".upper() == "HELLO"

    def test_fixture_loading(self, sample_sprint_state):
        """Test that fixtures from conftest.py load correctly."""
        assert sample_sprint_state is not None
        assert sample_sprint_state["project_name"] == "test-project"
        assert sample_sprint_state["pool_size"] == 3
        assert sample_sprint_state["phase"] == "init"

    def test_job_spec_fixture(self, sample_job_spec):
        """Test that job spec fixture works."""
        assert sample_job_spec["name"] == "test-job"
        assert sample_job_spec["story_points"] == 5
        assert len(sample_job_spec["todos"]) == 3

    def test_repo_info_fixture(self, sample_repo_info):
        """Test that repo info fixture works."""
        assert sample_repo_info["has_remote"] is True
        assert sample_repo_info["default_branch"] == "main"

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker is applied."""
        assert True

    @pytest.mark.asyncio
    async def test_async_support(self):
        """Test that async tests work."""
        import asyncio
        await asyncio.sleep(0.001)
        assert True

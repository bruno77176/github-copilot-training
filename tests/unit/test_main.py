import pytest

from app.models import DeveloperTask, ProductivityReport
from app.main import fetch_all_tasks, generate_productivity_report


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list() -> None:
    """Test that `fetch_all_tasks` returns a list of DeveloperTask objects."""
    tasks = await fetch_all_tasks()
    assert isinstance(tasks, list)
    assert all(isinstance(t, DeveloperTask) for t in tasks)


@pytest.mark.asyncio
async def test_generate_productivity_report_calculates_metrics() -> None:
    """Test that `generate_productivity_report` computes expected metrics."""
    report = await generate_productivity_report()
    assert isinstance(report, ProductivityReport)
    assert report.total_tasks >= 0
    assert isinstance(report.completion_rate, float)
    # Basic consistency: completed_tasks <= total_tasks
    assert report.completed_tasks <= report.total_tasks

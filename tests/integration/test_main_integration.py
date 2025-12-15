import pytest

from app.models import DeveloperTask, TaskStatus


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_returns_ok(client):
    resp = await client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_list(client):
    resp = await client.get("/tasks")
    assert resp.status_code == 200
    tasks = resp.json()
    assert isinstance(tasks, list)
    if tasks:
        assert "task_id" in tasks[0]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_returns_report(client):
    resp = await client.get("/report")
    assert resp.status_code == 200
    report = resp.json()
    assert "total_tasks" in report
    assert "completion_rate" in report


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_creates_new_task(client, reset_mock_tasks):
    new_task = {
        "task_id": 0,
        "title": "Integration test task",
        "status": "pending",
        "hours_spent": 2.5,
    }
    resp = await client.post("/log_task", json=new_task)
    assert resp.status_code == 200
    created = resp.json()
    assert created["title"] == new_task["title"]
    assert isinstance(created["task_id"], int)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_found_and_not_found(client):
    # existing task
    resp_ok = await client.get("/task/1/status")
    assert resp_ok.status_code == 200
    ok_data = resp_ok.json()
    assert "task_id" in ok_data
    # non-existent task should return an error payload (implementation detail)
    resp_nf = await client.get("/task/999/status")
    assert resp_nf.status_code == 200
    nf_data = resp_nf.json()
    assert ("error" in nf_data) or (nf_data.get("task_id") is None)


import task_tools


def test_create_task(monkeypatch):

    monkeypatch.setattr(
        task_tools,
        "tasks",
        {}
    )

    monkeypatch.setattr(
        task_tools,
        "save_tasks",
        lambda tasks: None
    )

    result = task_tools.create_task("学习 Python")

    assert result is not None
    assert len(task_tools.tasks) == 1


def test_list_tasks(monkeypatch):

    fake_tasks = {
        "1": {
            "title": "学习 Java",
            "status": "pending"
        }
    }

    monkeypatch.setattr(
        task_tools,
        "tasks",
        fake_tasks
    )

    result = task_tools.list_tasks()

    assert "1" in result
    assert result["1"]["title"] == "学习 Java"


def test_delete_nonexistent_task(monkeypatch):

    monkeypatch.setattr(
        task_tools,
        "tasks",
        {}
    )

    result = task_tools.delete_task("999")

    assert "error" in result

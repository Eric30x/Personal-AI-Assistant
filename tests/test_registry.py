
import registry


def test_delete_requires_approval():

    result = registry.execute_tool(
        "delete_task",
        {"task_id": "1"}
    )

    assert result["status"] == "error"

    assert (
        result["error_code"]
        == "APPROVAL_REQUIRED"
    )


def test_unknown_tool():

    result = registry.execute_tool(
        "unknown_tool",
        {}
    )

    assert result["status"] == "error"

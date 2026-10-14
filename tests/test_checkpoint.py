
import checkpoint


def test_checkpoint_save_and_load(
    monkeypatch,
    tmp_path
):

    test_file = tmp_path / "checkpoint.json"

    monkeypatch.setattr(
        checkpoint,
        "CHECKPOINT_FILE",
        test_file
    )

    messages = [
        {
            "role": "user",
            "content": "学习 Python"
        }
    ]

    checkpoint.save_checkpoint(
        messages,
        "TOOL_COMPLETED"
    )

    result = checkpoint.load_checkpoint()

    assert result["state"] == "TOOL_COMPLETED"

    assert result["messages"] == messages


def test_checkpoint_clear(
    monkeypatch,
    tmp_path
):

    test_file = tmp_path / "checkpoint.json"

    monkeypatch.setattr(
        checkpoint,
        "CHECKPOINT_FILE",
        test_file
    )

    checkpoint.save_checkpoint(
        [],
        "TOOL_COMPLETED"
    )

    assert test_file.exists()

    checkpoint.clear_checkpoint()

    assert not test_file.exists()

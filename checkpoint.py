
import json
import os
from pathlib import Path

CHECKPOINT_FILE = (
    Path(__file__).resolve().parent / "checkpoint.json"
)


def save_checkpoint(messages, state):

    data = {
        "state": state,
        "messages": messages
    }

    temp_file = CHECKPOINT_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temp_file, CHECKPOINT_FILE)


def load_checkpoint():

    if not CHECKPOINT_FILE.exists():
        return None

    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_checkpoint():

    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()

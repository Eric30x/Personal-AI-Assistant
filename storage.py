import json
from pathlib import Path

TASK_FILE=Path(__file__).resolve().parent / 'task.json'

def load_tasks():
    if not TASK_FILE.exists():
        return {}
    with open(TASK_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE,"w",encoding="utf-8") as f:
        json.dump(tasks,f,ensure_ascii=False,indent=2)

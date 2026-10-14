from storage import load_tasks,save_tasks
tasks = load_tasks()
def create_task(title):
    task_id = str(
        max(
            (int(k) for k in tasks.keys()),
            default=0
        )+1
    )
    tasks[task_id] = {
        'title': title,
        "status":"pending"
    }
    save_tasks(tasks)
    return {
        "task_id": task_id,
        "title": title,
        "message":"创建成功"
    }

def list_tasks():
    return tasks
def update_task(task_id, title):
    if task_id not in tasks:
        return {"error": "任务不存在"}
    tasks[task_id]["title"] = title
    save_tasks(tasks)
    return {
        "task_id": task_id,
        "title": title,
        "message": "修改成功"
    }
def delete_task(task_id):

    if task_id not in tasks:
        return {"error": "任务不存在"}

    deleted_task = tasks.pop(task_id)

    save_tasks(tasks)

    return {
        "task_id": task_id,
        "deleted_task": deleted_task,
        "message": "任务删除成功"
    }
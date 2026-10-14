
import uuid

tasks = {}
processed_requests = {}


def create_task(title, request_id):

    if request_id in processed_requests:
        print("检测到重复请求，返回已有结果")
        return processed_requests[request_id]

    task_id = str(len(tasks) + 1)

    tasks[task_id] = {
        "title": title,
        "status": "pending"
    }

    result = {
        "task_id": task_id,
        "title": title,
        "message": "创建成功"
    }

    processed_requests[request_id] = result

    return result


if __name__ == "__main__":

    request_id_1 = str(uuid.uuid4())

    print("第一次请求：")
    print(create_task("学习 Python", request_id_1))

    print("\n第二次请求（相同 ID）：")
    print(create_task("学习 Python", request_id_1))

    request_id_2 = str(uuid.uuid4())

    print("\n第三次请求（新 ID）：")
    print(create_task("学习 Python", request_id_2))

    print("\n最终任务列表：")
    print(tasks)

import os
import json
SIMULATE_FAILURE = False
from checkpoint import (
    save_checkpoint,
    load_checkpoint,
    clear_checkpoint
)
from openai import OpenAI
from registry import execute_tool, SENSITIVE_TOOLS

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
    timeout=30.0
)

tools = [

    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "删除指定任务，执行前需要用户确认",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "要删除的任务ID"
                    }
                },
                "required": ["task_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "创建一个新的待办任务",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "任务标题"
                    }
                },
                "required": ["title"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "查询所有待办任务",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "修改指定任务的标题",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "要修改的任务ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "修改后的任务标题"
                    }
                },
                "required": ["task_id", "title"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前本地日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    }
]

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "你是一个个人任务管理 AI 助手。"
        "涉及任务操作时，必须使用工具获取真实结果。"
        "不得编造工具执行成功的结果。"
        "删除任务必须经过程序中的用户确认。"
    )
}

messages = [SYSTEM_MESSAGE]


def restore_messages():

    checkpoint = load_checkpoint()

    if checkpoint is None:
        return False

    if checkpoint.get("state") != "TOOL_COMPLETED":
        return False

    saved_messages = checkpoint.get("messages")

    if not isinstance(saved_messages, list):
        return False

    messages.clear()
    messages.extend(saved_messages)

    return True


def agent_loop():
    MAX_ROUNDS = 8

    for round_number in range(1, MAX_ROUNDS + 1):

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content or ""

            messages.append({
                "role": "assistant",
                "content": answer
            })
            clear_checkpoint()

            return answer

        messages.append(
            message.model_dump(exclude_none=True)
        )

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                if function_name in SENSITIVE_TOOLS:

                    print("\n=== 危险操作确认 ===")
                    print("工具名称：", function_name)
                    print("操作参数：", arguments)

                    # 对删除任务，展示即将删除的任务内容
                    if function_name == "delete_task":
                        current = execute_tool("list_tasks", {})

                        if current["status"] == "success":
                            task_id = arguments.get("task_id")
                            task = current["data"].get(task_id)

                            if task is not None:
                                print("即将删除：", task)
                            else:
                                print("未找到对应任务")

                    confirmation = input(
                        "是否确认执行？输入 yes 确认："
                    ).strip().lower()

                    if confirmation == "yes":

                        result = execute_tool(
                            function_name,
                            arguments,
                            approved=True
                        )

                    else:

                        result = {
                            "status": "error",
                            "error_code": "USER_REJECTED",
                            "message": "用户拒绝执行该操作"
                        }

                else:

                    result = execute_tool(
                        function_name,
                        arguments
                    )


            except json.JSONDecodeError:
                result = {
                    "status": "error",
                    "error_code": "INVALID_JSON",
                    "message": "工具参数不是合法的JSON"
                }

            except Exception:
                result = {
                    "status": "error",
                    "error_code": "EXECUTION_ERROR",
                    "message": "工具执行时发生内部错误"
                }

            tool_result = json.dumps(
                result,
                ensure_ascii=False
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        save_checkpoint(
            messages=messages,
            state="TOOL_COMPLETED"
        )
        if SIMULATE_FAILURE:
            raise ConnectionError("模拟 DeepSeek API 连接中断")


def run_agent(user_input):

    messages.append({
        "role": "user",
        "content": user_input
    })

    return agent_loop()
def resume_agent():

    restored = restore_messages()

    if not restored:
        return "没有可恢复的 Agent 任务"

    return agent_loop()

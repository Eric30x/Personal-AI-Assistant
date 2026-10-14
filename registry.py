import logging

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    ValidationError
)

from task_tools import (
    create_task,
    list_tasks,
    update_task,
    delete_task
)
from time_tools import get_time


class CreateTaskArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1)


class ListTaskArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UpdateTaskArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_id: str
    title: str = Field(min_length=1)


class GetTimeArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

class DeleteTaskArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_id: str


TOOLS_REGISTRY = {
    "create_task": {
        "function": create_task,
        "schema": CreateTaskArgs
    },
    "list_tasks": {
        "function": list_tasks,
        "schema": ListTaskArgs
    },
    "update_task": {
        "function": update_task,
        "schema": UpdateTaskArgs
    },
    "get_time": {
        "function": get_time,
        "schema": GetTimeArgs
    },
    "delete_task": {
        "function": delete_task,
        "schema": DeleteTaskArgs
    }
}


logger = logging.getLogger(__name__)
SENSITIVE_TOOLS = {"delete_task"}

def execute_tool(function_name,arguments,approved=False):
    if function_name in SENSITIVE_TOOLS and not approved:
        return {
            "status": "error",
            "error_code": "APPROVAL_REQUIRED",
            "message": "该操作需要用户确认"
        }
    if function_name not in TOOLS_REGISTRY:
        return{
            "status": "error",
            "error_code": "UNKNOWN_TOOL",
            "message": "未知工具"
        }
    tool_info = TOOLS_REGISTRY[function_name]
    function = tool_info["function"]
    schema = tool_info["schema"]
    try:
        validated = schema.model_validate(arguments)
        safe_arguments = validated.model_dump()
    except ValidationError:
        return {
            "status": "error",
            "error_code": "INVALID_ARGUMENT",
            "message": "参数验证失败"
        }
    try:
        result = function(**safe_arguments)
        if isinstance(result, dict) and "error" in result:
            return {
                "status": "error",
                "error_code": "BUSINESS_ERROR",
                "message": str(result["error"])
            }
        return {
            "status": "success",
            "data": result
        }
    except OSError:
        logger.exception("工具执行发生系统错误")

        return {
            "status": "error",
            "error_code": "STORAGE_ERROR",
            "message": "存储操作失败"
        }

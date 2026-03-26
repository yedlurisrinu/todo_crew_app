"""
@Author: Srini Yedluri
@Date: 3/21/26
@File: main_test.py
"""

import os
from agents import Agent, FunctionTool, RunContextWrapper
from pydantic import BaseModel
from enum import Enum
from typing import Any
import json
import httpx
import logging

logger = logging.getLogger(__name__)
TODOS_API = os.getenv("TODOS_API")
class Action(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    description: str

class TodoItemArgs(BaseModel):
    action: Action
    task: TodoItem

class TodoAPI:
    BASE_URL = TODOS_API+"/todos"

    @classmethod
    def get_tasks(cls):
        logger.info(' Get tasks got called ')
        response = httpx.get(cls.BASE_URL)
        response.raise_for_status()
        return [TodoItem(**item) for item in response.json()]

    @classmethod
    def create_task(cls, task: TodoItem):
        logger.info(f' Create tasks got called : {task.id}')
        response = httpx.post(cls.BASE_URL, json=task.model_dump())
        logger.info(response)
        logger.info(response.content)
        logger.info(response.text)

        response.raise_for_status()
        return TodoItem(**response.json())

    @classmethod
    def update_task(cls, task: TodoItem):
        logger.info(f' Update tasks got called for id : {task.id}')
        response = httpx.put(f"{cls.BASE_URL}/{task.id}", json=task.model_dump())
        response.raise_for_status()
        return TodoItem(**response.json())

    @classmethod
    def delete_task(cls, task: TodoItem):
        logger.info(f' Delete tasks got called for id : {task.id}')
        response = httpx.delete(f"{cls.BASE_URL}/{task.id}")
        response.raise_for_status()
        return {"message": "Task deleted successfully"}

    @classmethod
    def handle_request(cls, action, task):
        if action == Action.GET:
            tasks = cls.get_tasks()
            return [t.model_dump() for t in tasks]
        elif action == Action.POST:
            return cls.create_task(task).model_dump()
        elif action == Action.PUT:
            return cls.update_task(task).model_dump()
        elif action == Action.DELETE:
            return cls.delete_task(task)
        else:
            raise ValueError(f"Unknown action: {action}")

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    logger.info(f"Todo agent called with {args}")
    parsed = TodoItemArgs.model_validate_json(args)
    result = TodoAPI.handle_request(parsed.action, parsed.task)
    return json.dumps({"result": result})

model_json_schema = TodoItemArgs.model_json_schema()
model_json_schema["additionalProperties"] = False
model_json_schema["$defs"]["TodoItem"]["additionalProperties"] = False

todos_api_tool = FunctionTool(
    name="todos_api",
    description="A tool for interacting with the Todo API",
    params_json_schema=model_json_schema,
    on_invoke_tool=run_function
)

TODO_AGENT = Agent(
    name="Todo Manager",
    instructions=(
        "You are a Todo API agent. "
        "You can create, read, update, and delete tasks using the Todo API. "
        "Use the todos_api tool to interact with the API. "
        "For GET and PUT actions: always first list all tasks (use GET), then proceed with the requested operation (for PUT, update the task after listing). "
        "For DELETE action: you must first list all the tasks, identify the ID of the task you need to remove and then use the tool to delete the task."
    ),
    tools=[todos_api_tool]
)
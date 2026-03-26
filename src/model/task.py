"""
@Author: Srini Yedluri
@Date: 3/22/26
@Time: 3:40 PM
@File: task.py
"""
from pydantic import BaseModel

class Task(BaseModel):
    task_details: str

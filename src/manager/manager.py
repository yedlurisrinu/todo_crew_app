"""
@Author: Srini Yedluri
@Date: 3/21/26
@File: main_test.py
"""

from todo_agent.todo_agent import TODO_AGENT
from search_agent.rag_agent import RAG_AGENT
from agents import Runner, Agent
import logging

logger = logging.getLogger(__name__)

MANAGER_AGENT = Agent(
    name="Manager Agent",
    instructions=(
        "You are a manager agent that orchestrates multiple agents. "
        "You can delegate tasks to the Todo Agent and the Learn Agent. "
        "Use the Todo Agent for task management and the Learn Agent for retrieving learning items and returning it to the user."
    ),
    tools=[TODO_AGENT.as_tool(
            tool_name="todo_agent",
            tool_description="A tool for managing tasks using the Todo API"
        ),
        RAG_AGENT.as_tool(
            tool_name="rag_agent",
            tool_description="A tool for providing answers regarding user's learning items"
        )
    ]
)

def run_manager_agent(requests):
    logger.info(" calling manager agent with request details ")
    try:
        result = Runner.run_sync(MANAGER_AGENT, requests)
        logging.info(f"Manager Agent: {result.final_output}")
        return result.final_output
    except Exception as e:
        logger.error(f" Exception occurred while executing agent {e}", exc_info=True)

    return ""
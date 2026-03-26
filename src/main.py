"""
@Author: Srini Yedluri
@Date: 3/21/26
@File: main_test.py
"""
from config.secret_loader import load_secrets
load_secrets()
import json
import logging.config

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from search_builder.rag_builder import build_rag
from pathlib import Path
import logging
from manager import manager
from model.task import Task
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()          # 👈 this is what "app" refers to
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )
app.mount("/static", StaticFiles(directory="static"), name="static")

def setup_logging(config_file="logging_config.json"):
    path = str(Path(__name__).parent.parent)
    try:
        with open(path+"/"+config_file) as file_handler:
            config = json.load(file_handler)
        logging.config.dictConfig(config)
    except FileNotFoundError as fe:
        logging.basicConfig(level=logging.INFO)
        print(" exception while loading log config file ", fe)

setup_logging()
build_rag()

chat_ui_path = Path(__name__).parent.parent

""" End point that will render chat ui html for chat interaction, this is context less """
@app.get("/")
def serve_ui():
    return FileResponse(str(chat_ui_path)+"/static/chat-ui.html")

@app.get("/health")
def health_check():
    logger.debug(" health check ")
    return {"status": "ok"}

""" The chat endpoint that will accept user input and replies task completion task and AI summary response"""
@app.post("/todos/")
def manage_todos(task : Task):
    logger.info(f"user question {task}", )
    return manager.run_manager_agent(task.task_details)

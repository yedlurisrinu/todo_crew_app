from typing import Any
from pydantic import BaseModel
from agents import Agent, FunctionTool, RunContextWrapper
from search_builder.rag_builder import load_collection
import logging

logger = logging.getLogger(__name__)

def retrieve_top_chunks(user_query, top_k=1):
    collection = load_collection()
    results = {}
    try:
        results = collection.query(
            query_texts=[user_query],
            n_results=top_k
        )
    except Exception as e:
        logger.error(f" Exception while trying to access collection {e}")

    retrieved_chunks = []
    if results:
        for i in range(len(results['documents'][0])):
            retrieved_chunks.append({
                "chunk": results['documents'][0][i],
                "id": results['metadatas'][0][i],
                "distance": results['distances'][0][i]
            })
    return retrieved_chunks

class FunctionArgs(BaseModel):
    user_query: str

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    logger.info(f" Rag Agent got called with {args}")
    parsed = FunctionArgs.model_validate_json(args)
    chunks = retrieve_top_chunks(parsed.user_query)
    return "\n".join([c["chunk"] for c in chunks])

rag_retrieval_tool = FunctionTool(
    name="rag_retrieval_tool",
    description="A tool to retrieve the learning items of the user",
    params_json_schema={
        "type": "object",
        "properties": {
            "user_query": {"type": "string"},
        },
        "required": ["user_query"],
        "additionalProperties": False
    },
    on_invoke_tool=run_function
)

RAG_AGENT = Agent(
    name="Learning Assistant",
    instructions=(
        "You are a personal learning assistant with access to rag tool. "
        "Whenever asked a question about learning item, use the RAG retrieval tool to get context from the DB and return the learning items of the user along with plan how to tackle it."
    ),
    tools=[rag_retrieval_tool]
)
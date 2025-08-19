# backend/agents/agent.py
import logging
from graph import run_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_agent(input_data):
    logger.info("🤖 Agent starting...")
    result = run_graph(input_data)
    return {
        "message": "Chatbot 4 Agentic AI completed.",
        "result": result
    }

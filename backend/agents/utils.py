# backend/agents/utils.py

import logging

logger = logging.getLogger(__name__)

def ask_llm(prompt):
    logger.info(f"[LOG] Asking LLM with prompt: {prompt}")
    if "shortlist the best candidates" in prompt.lower():
        return "[1, 2]"  # Return a string representation of a list for shortlist
    elif "should we send an offer or regret" in prompt.lower():
        return "offer"
    elif "Would you approve this request?" in prompt:
        return "approve"
    else:
        return "Generated 3 technical and 2 behavioral questions."
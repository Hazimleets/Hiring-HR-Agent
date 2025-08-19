
import logging
import json
from agents.prompts import shortlist_prompt
from agents.utils import ask_llm

logger = logging.getLogger(__name__)

def shortlist_applicants(context):
    applicants = context.get("applicants", [])
    if not applicants or not context.get("description"):
        context.update({
            "status": "error",
            "reason": "Missing applicants or job description in context"
        })
        logger.error(context["reason"])
        return context

    try:
        prompt = shortlist_prompt.format(
            applicants=str(applicants),
            description=context["description"],
            requirements="\n".join(context.get("requirements", []))
        )
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to format shortlist prompt: {str(e)}"
        })
        logger.error(context["reason"])
        return context

    shortlist_result = ask_llm(prompt)
    logger.info(f"LLM shortlist response: {shortlist_result}")

    try:
        # Try parsing as JSON first, then fall back to eval for compatibility
        try:
            shortlisted_ids = json.loads(shortlist_result)
        except json.JSONDecodeError:
            shortlisted_ids = eval(shortlist_result)
        
        if not isinstance(shortlisted_ids, list):
            raise ValueError(f"Expected a list from LLM, got {type(shortlisted_ids)}: {shortlist_result}")
        
        valid_ids = [a["id"] for a in applicants]
        shortlisted_ids = [id for id in shortlisted_ids if id in valid_ids]
        if not shortlisted_ids:
            raise ValueError("No valid candidate IDs in shortlist result")
        
        context.update({
            "shortlisted_applicants": shortlisted_ids
        })
        logger.info(f"Shortlisted candidates: {shortlisted_ids}")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to shortlist applicants: {str(e)}"
        })
        logger.error(context["reason"])

    return context
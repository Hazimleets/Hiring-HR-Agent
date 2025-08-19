# nodes/decision.py
import logging
from agents.utils import ask_llm

logger = logging.getLogger(__name__)

def make_decision(context):
    interview_results = context.get("interview_simulation_results", [])
    shortlisted = context.get("shortlisted_applicants", [])
    job_description = context.get("description", "")

    if not interview_results or not shortlisted or not job_description:
        context.update({
            "status": "error",
            "reason": "Missing interview results, shortlisted applicants, or job description in context"
        })
        logger.error(context["reason"])
        return context

    try:
        prompt = f"""
        Given the feedback: {context}, should we send an offer or regret?
        """
        decision = ask_llm(prompt)
        logger.info(f"LLM decision response: {decision}")

        if decision.lower() not in ["offer", "regret"]:
            context.update({
                "status": "error",
                "reason": f"Invalid decision from LLM: {decision}"
            })
            logger.error(context["reason"])
            return context

        context.update({
            "decision": decision.lower()
        })
        logger.info(f"Decision made: {decision.lower()}")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to make decision: {str(e)}"
        })
        logger.error(context["reason"])

    return context
# backend/graph.py

import logging
from nodes.create_request import create_request
from nodes.post_jd import post_job
from nodes.monitor import monitor_applicants
from nodes.shortlist import shortlist_applicants
from nodes.schedule import schedule_interview
from nodes.interview import simulate_interview
from nodes.decision import make_decision
from nodes.offer import send_offer
from nodes.regret import send_regret
from nodes.onboard import onboarding_instructions
from db.schema import Job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_graph(input_data):
    steps = [
        create_request,
        post_job,
        monitor_applicants,
        shortlist_applicants,
        schedule_interview,
        simulate_interview,
        make_decision,
        send_offer,
        send_regret,
        onboarding_instructions
    ]

    context = input_data.copy()
    logger.info("🚀 Starting Agentic Hiring Workflow...\n")

    if context.get("job_id"):
        try:
            job = Job.query.get_or_404(context["job_id"])
            context.update({
                "title": job.title,
                "description": job.description,
                "requirements": job.requirements.split("\n") if job.requirements else []
            })
            logger.info(f"Fetched job details for job_id: {context['job_id']} - {job.title}")
        except Exception as e:
            logger.error(f"Failed to fetch job: {str(e)}")
            context.update({
                "status": "error",
                "reason": f"Job not found for job_id: {context['job_id']}"
            })
            return context

    start_index = 0
    if context.get("job_id"):
        logger.info(f"Using existing job_id: {context['job_id']}. Skipping create_request and post_job.")
        start_index = 2

    for i, step in enumerate(steps[start_index:], start_index + 1):
        if context.get("skip_candidate_steps") and step.__name__ in [
            "shortlist_applicants",
            "schedule_interview",
            "simulate_interview",
            "make_decision",
            "send_offer",
            "send_regret",
            "onboarding_instructions"
        ]:
            logger.info(f"Skipping step {i}: `{step.__name__}` due to no applicants")
            continue

        try:
            context = step(context)
            logger.info(f"✅ Step {i}: `{step.__name__}` completed.")

            if not isinstance(context, dict):
                logger.error(f"Context is not a dictionary after step `{step.__name__}`: {type(context)}")
                context = {"status": "error", "reason": f"Invalid context type {type(context)} after step `{step.__name__}`"}
                return context

            logger.info("Current context state:")
            for k, v in context.items():
                logger.info(f"   - {k}: {v}")

            if context.get("status") in ["error", "rejected"]:
                logger.error(f"❌ Stopping after step `{step.__name__}`: {context.get('reason')}")
                context["final_status"] = context.get("status")
                return context

            if context.get("status") == "warning":
                logger.warning(f"⚠️ Warning after step `{step.__name__}`: {context.get('reason')}")
        except Exception as e:
            logger.exception(f"Exception during step `{step.__name__}`")
            context = {
                "status": "error",
                "reason": f"Step `{step.__name__}` failed: {str(e)}"
            } if not isinstance(context, dict) else context
            context.update({
                "status": "error",
                "reason": f"Step `{step.__name__}` failed: {str(e)}"
            })
            return context

    context["final_status"] = "completed"
    logger.info("\n🎯 Agentic Workflow Completed Successfully!\n")
    logger.info("📦 Final Context Summary:")
    for k, v in context.items():
        logger.info(f"   - {k}: {v}")

    return context
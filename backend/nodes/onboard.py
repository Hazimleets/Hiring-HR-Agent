# nodes/onboard.py
import logging
from tools.gmail_api import send_email

logger = logging.getLogger(__name__)

def onboarding_instructions(context):
    shortlisted = context.get("shortlisted_applicants", [])
    if not shortlisted:
        context.update({
            "status": "error",
            "reason": "No shortlisted candidates found for onboarding"
        })
        logger.error(context["reason"])
        return context

    applicants = context.get("applicants", [])
    onboarding_results = []

    try:
        for candidate_id in shortlisted:
            candidate = next((a for a in applicants if a["id"] == candidate_id), None)
            if not candidate:
                onboarding_results.append({
                    "candidate_id": candidate_id,
                    "status": "error",
                    "reason": "Candidate not found"
                })
                continue

            email_result = send_email(
                to=candidate["email"],
                subject="Onboarding Steps",
                content=f"Dear {candidate['name']},\n\nWelcome onboard! Here's what to do next:\n1. Complete the attached forms.\n2. Attend orientation on 2025-07-20.\n3. Contact HR for any questions."
            )
            onboarding_results.append({
                "candidate_id": candidate_id,
                "candidate_name": candidate["name"],
                "status": email_result.get("status")
            })

        context.update({
            "onboarding_status": "sent",
            "onboarding_results": onboarding_results
        })
        logger.info(f"Sent onboarding emails to {len(onboarding_results)} candidates")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to send onboarding instructions: {str(e)}"
        })
        logger.error(context["reason"])

    return context
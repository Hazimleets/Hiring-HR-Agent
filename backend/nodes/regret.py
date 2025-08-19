# nodes/regret.py
import logging
from tools.gmail_api import send_email

logger = logging.getLogger(__name__)

def send_regret(context):
    shortlisted = context.get("shortlisted_applicants", [])
    applicants = context.get("applicants", [])
    if not applicants:
        context.update({
            "status": "error",
            "reason": "No applicants found to send regret emails"
        })
        logger.error(context["reason"])
        return context

    rejected = [a for a in applicants if a["id"] not in shortlisted]
    if not rejected:
        context.update({
            "regret_status": "skipped",
            "reason": "No candidates to reject"
        })
        logger.info(context["reason"])
        return context

    try:
        regret_results = []
        for candidate in rejected:
            email_result = send_email(
                to=candidate["email"],
                subject="Regarding your job application",
                content=f"Dear {candidate['name']},\n\nThank you for applying. Unfortunately, you were not selected."
            )
            regret_results.append({
                "candidate_id": candidate["id"],
                "candidate_name": candidate["name"],
                "status": email_result.get("status")
            })

        context.update({
            "regret_status": "sent",
            "regret_results": regret_results
        })
        logger.info(f"Sent regret emails to {len(regret_results)} candidates")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to send regret emails: {str(e)}"
        })
        logger.error(context["reason"])

    return context

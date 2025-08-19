# nodes/offer.py
import logging
from tools.offer_letter import generate_offer_letter
from tools.gmail_api import send_email

logger = logging.getLogger(__name__)

def send_offer(context):
    shortlisted = context.get("shortlisted_applicants", [])
    if not shortlisted:
        context.update({
            "status": "error",
            "reason": "No shortlisted candidates found"
        })
        logger.error(context["reason"])
        return context

    applicants = context.get("applicants", [])
    offer_results = []

    try:
        for candidate_id in shortlisted:
            candidate = next((a for a in applicants if a["id"] == candidate_id), None)
            if not candidate:
                offer_results.append({
                    "candidate_id": candidate_id,
                    "status": "error",
                    "reason": "Candidate not found"
                })
                continue

            offer_letter = generate_offer_letter(
                name=candidate["name"],
                position=context.get("title", "Software Engineer"),
                company="YourCompany",
                skills=context.get("requirements", "Python, Flask"),
                hr_name="HR Bot"
            )
            email_result = send_email(
                to=candidate["email"],
                subject=f"Offer Letter for {context.get('title', 'Software Engineer')}",
                content=offer_letter
            )

            offer_results.append({
                "candidate_id": candidate_id,
                "candidate_name": candidate["name"],
                "status": email_result.get("status"),
                "offer_letter": offer_letter
            })

        context.update({
            "offer_status": "sent",
            "offer_results": offer_results
        })
        logger.info(f"Sent offers to {len(offer_results)} candidates")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to send offers: {str(e)}"
        })
        logger.error(context["reason"])

    return context
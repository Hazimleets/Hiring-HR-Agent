# nodes/schedule.py
import logging
from tools.calendar_api import schedule_interview as schedule_api
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def schedule_interview(context):
        shortlisted = context.get("shortlisted_applicants", [])
        if not shortlisted:
            context.update({
                "status": "error",
                "reason": "No shortlisted candidates found"
            })
            logger.error(context["reason"])
            return context

        applicants = context.get("applicants", [])
        results = []

        try:
            for candidate_id in shortlisted:
                candidate = next((a for a in applicants if a["id"] == candidate_id), None)
                if not candidate:
                    results.append({
                        "candidate_id": candidate_id,
                        "status": "error",
                        "reason": "Candidate not found"
                    })
                    continue

                # Set interview time to next business day, 10:00 AM PKT (UTC+5)
                interview_time = (datetime.now() + timedelta(days=1)).replace(
                    hour=10, minute=0, second=0, microsecond=0
                ).strftime("%Y-%m-%d %I:%M %p")
                result = schedule_api(candidate["name"], interview_time)
                results.append({
                    "candidate_id": candidate_id,
                    "candidate_name": candidate["name"],
                    "status": result.get("status"),
                    "interview_time": interview_time
                })

            context.update({
                "interview_status": "scheduled",
                "interview_results": results
            })
            logger.info(f"Scheduled interviews for {len(results)} candidates")
        except Exception as e:
            context.update({
                "status": "error",
                "reason": f"Failed to schedule interviews: {str(e)}"
            })
            logger.error(context["reason"])

        return context

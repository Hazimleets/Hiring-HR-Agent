# nodes/monitor.py
import logging
from db.schema import Candidate

logger = logging.getLogger(__name__)

def monitor_applicants(context):
    try:
        job_id = context.get("job_id")
        if not job_id:
            context.update({
                "status": "error",
                "reason": "Missing job_id in context"
            })
            logger.error(context["reason"])
            return context

        logger.info(f"Querying candidates for job_id: {job_id}")
        applicants = Candidate.query.filter_by(job_id=job_id).all()
        logger.info(f"Found {len(applicants)} candidates for job_id: {job_id}")

        if not applicants:
            context.update({
                "status": "warning",
                "reason": f"No applicants found for job_id: {job_id}",
                "applicants": [],
                "skip_candidate_steps": True
            })
            logger.warning(context["reason"])
            return context

        context.update({
            "applicants": [
                {
                    "id": c.id,
                    "name": c.name,
                    "email": c.email,
                    "resume_link": c.resume_link,
                    "score": c.score
                }
                for c in applicants
                if c.name and c.email and c.resume_link
            ]
        })
        logger.info(f"Loaded {len(context['applicants'])} valid applicants")
    except Exception as e:
        logger.exception("Failed in monitor_applicants")
        context.update({
            "status": "error",
            "reason": f"Step monitor_applicants failed: {str(e)}"
        })

    return context

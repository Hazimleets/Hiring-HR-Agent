# backend/tools/linkedin_api.py

import logging

logger = logging.getLogger(__name__)

def post_job_to_linkedin(title, description):
    logger.info(f"Posting job to LinkedIn: {title}")
    return {
        "status": "posted",
        "url": f"https://linkedin.com/jobs/view/dummy-job-id-for-{title.replace(' ', '-')}"
    }


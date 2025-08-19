# nodes/post_jd.py
from db.schema import Job, db
from tools.linkedin_api import post_job_to_linkedin

def post_job(context):
    if not context.get("job_id"):
        context.update({
            "post_status": "skipped",
            "reason": "No job_id found. Skipping LinkedIn posting."
        })
        return context

    try:
        job_id = int(context.get("job_id"))
        job = db.get_or_404(Job, job_id)
        result = post_job_to_linkedin(job.title, job.description)
        context.update({
            "post_status": result.get("status"),
            "posting_url": result.get("url")
        })
    except Exception as e:
        context.update({
            "post_status": "error",
            "reason": str(e)
        })

    return context

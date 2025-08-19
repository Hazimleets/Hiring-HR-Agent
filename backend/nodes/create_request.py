#nodes/create_request.py

import logging
from agents.prompts import job_request_prompt
from agents.utils import ask_llm
from db.schema import Job, db
from memory_manager import save_to_memory

logger = logging.getLogger(__name__)

def create_request(context):
    title = context.get("title")
    description = context.get("description")
    requirements = context.get("requirements")
    role = context.get("role", "Hiring Manager")

    if not all([title, description, requirements]):
        context.update({
            "status": "error",
            "reason": "Missing required fields: title, description, or requirements"
        })
        logger.error(context["reason"])
        return context

    existing_job = Job.query.filter_by(title=title).first()
    if existing_job:
        context.update({
            "status": "error",
            "reason": f"Job with title '{title}' already exists (job_id: {existing_job.id})"
        })
        logger.error(context["reason"])
        return context

    formatted_requirements = "\n".join(requirements) if isinstance(requirements, list) else str(requirements)

    try:
        full_prompt = job_request_prompt.format(
            title=title,
            description=description,
            requirements=formatted_requirements,
            role=role
        )
    except KeyError as e:
        context.update({
            "status": "error",
            "reason": f"Prompt formatting failed. Missing field: {e}"
        })
        logger.error(context["reason"])
        return context

    approval = ask_llm(full_prompt)
    logger.info(f"LLM approval response: {approval}")

    if "approve" in approval.lower():
        try:
            job = Job(title=title, description=description, requirements=formatted_requirements)
            db.session.add(job)
            db.session.commit()
            save_to_memory("job_request", f"{title} - {description}")
            context.update({
                "status": "approved",
                "job_id": job.id
            })
            logger.info(f"Job created: {title} (ID: {job.id})")
        except Exception as e:
            db.session.rollback()
            context.update({
                "status": "error",
                "reason": f"Failed to save job to database: {str(e)}"
            })
            logger.error(context["reason"])
    else:
        context.update({
            "status": "rejected",
            "reason": f"Job request not approved by LLM: {approval}"
        })
        logger.info(f"Job rejected: {approval}")

    return context

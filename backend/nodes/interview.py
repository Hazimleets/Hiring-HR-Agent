import logging
from agents.utils import ask_llm

logger = logging.getLogger(__name__)

def simulate_interview(context):
    shortlisted = context.get("shortlisted_applicants", [])
    applicants = context.get("applicants", [])
    job_description = context.get("description", "")

    if not shortlisted or not applicants or not job_description:
        context.update({
            "status": "error",
            "reason": "Missing shortlisted applicants, applicants, or job description in context"
        })
        logger.error(context["reason"])
        return context

    interview_results = []
    try:
        for candidate_id in shortlisted:
            candidate = next((c for c in applicants if c["id"] == candidate_id), None)
            if not candidate:
                interview_results.append({
                    "candidate_id": candidate_id,
                    "status": "error",
                    "reason": "Candidate not found"
                })
                logger.error(f"Candidate ID {candidate_id} not found in applicants")
                continue

            prompt = f"""
            Simulate an interview for {candidate['name']} for a Software Engineer position.
            Job Description: {job_description}
            Candidate Resume: {candidate['resume_link']}
            Generate 3 technical and 2 behavioral questions.
            """
            response = ask_llm(prompt)
            interview_results.append({
                "candidate_id": candidate_id,
                "candidate_name": candidate["name"],
                "status": "completed",
                "questions": response
            })
            logger.info(f"Simulated interview for {candidate['name']}: {response}")

        context.update({
            "interview_simulation_status": "completed",
            "interview_simulation_results": interview_results
        })
        logger.info(f"Completed interview simulations for {len(interview_results)} candidates")
    except Exception as e:
        context.update({
            "status": "error",
            "reason": f"Failed to simulate interviews: {str(e)}"
        })
        logger.error(context["reason"])

    return context
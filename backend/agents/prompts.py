# backend/agents/prompts.py

job_request_prompt = """
You are a {role}. Please review the following job request.

Title: {title}
Description: {description}
Requirements: {requirements}

Would you approve this request? Please explain why or why not.
"""

shortlist_prompt = """
Shortlist the best candidates for the following job:
Job Description: {description}
Requirements: {requirements}
Applicants: {applicants}
Return a list of candidate IDs for the top candidates.
"""

PROMPTS = {
    "interview": job_request_prompt,
    "shortlist": shortlist_prompt
}
# backend/tools/offer_letter.py
OFFER_TEMPLATE = """
Dear {name},

We are thrilled to offer you the position of {position} at {company}.
Your skills in {skills} are a great match for our team.

Sincerely,
{hr_name}
"""

def generate_offer_letter(name, position, company, skills, hr_name):
    return OFFER_TEMPLATE.format(
        name=name,
        position=position,
        company=company,
        skills=skills,
        hr_name=hr_name
    )
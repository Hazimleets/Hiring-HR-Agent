# backend/tools/gmail_api.py

import logging

logger = logging.getLogger(__name__)

def send_email(to, subject, content):
    logger.info(f"Sending email to {to}: {subject}\n{content}")
    with open(f"email_{to}.txt", "w") as f:
        f.write(f"Subject: {subject}\n\n{content}")
    return {"status": "sent"}
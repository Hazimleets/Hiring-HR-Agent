# backend/tools/calendar_api.py

import logging

logger = logging.getLogger(__name__)

def schedule_interview(candidate, datetime):
    logger.info(f"Interview for {candidate} scheduled at {datetime}.")
    return {"status": "scheduled"}
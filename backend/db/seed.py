# backend/db/seed.py

import logging
from db.schema import Candidate, Job, db

logger = logging.getLogger(__name__)

def seed_data(db):
    try:
        # Clear existing data to avoid conflicts
        db.session.query(Candidate).delete()
        db.session.query(Job).delete()
        db.session.commit()
        logger.info("Cleared existing jobs and candidates")

        # Create a sample job
        job = Job(
            title="Software Engineer",
            description="Develop and maintain web applications.",
            requirements="Python, Flask, SQLAlchemy"
        )
        db.session.add(job)
        db.session.commit()
        logger.info(f"✅ Seeded job: Software Engineer (ID: {job.id})")

        # Create multiple sample candidates
        candidates = [
            Candidate(
                name="Alice",
                email="alice@example.com",
                score=87.5,
                resume_link="https://example.com/resume/alice.pdf",
                job_id=job.id
            ),
            Candidate(
                name="Bob",
                email="bob@example.com",
                score=92.0,
                resume_link="https://example.com/resume/bob.pdf",
                job_id=job.id
            ),
            Candidate(
                name="Charlie",
                email="charlie@example.com",
                score=78.0,
                resume_link="https://example.com/resume/charlie.pdf",
                job_id=job.id
            )
        ]
        db.session.add_all(candidates)
        db.session.commit()
        logger.info(f"✅ Seeded {len(candidates)} candidates")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to seed database: {str(e)}")
        raise
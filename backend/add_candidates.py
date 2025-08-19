# backend/add_candidates.py

from flask import Flask
from db.schema import db, Candidate, Job
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    job = Job.query.filter_by(id=3).first()
    if job:
        candidates = [
            Candidate(
                name="Eve",
                email="eve@example.com",
                score=85.0,
                resume_link="https://example.com/resume/eve.pdf",
                job_id=job.id
            ),
            Candidate(
                name="Frank",
                email="frank@example.com",
                score=90.0,
                resume_link="https://example.com/resume/frank.pdf",
                job_id=job.id
            )
        ]
        db.session.add_all(candidates)
        db.session.commit()
        print(f"Added {len(candidates)} candidates for job_id: {job.id}")
    else:
        print("Job not found")
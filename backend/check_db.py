# backend/check_db.py

from flask import Flask
from db.schema import db, Job, Candidate
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    jobs = Job.query.all()
    print("Jobs:")
    for job in jobs:
        print(f"ID: {job.id}, Title: {job.title}, Description: {job.description}, Requirements: {job.requirements}")
    candidates = Candidate.query.all()
    print("\nCandidates:")
    for candidate in candidates:
        print(f"ID: {candidate.id}, Name: {candidate.name}, Email: {candidate.email}, Job ID: {candidate.job_id}")
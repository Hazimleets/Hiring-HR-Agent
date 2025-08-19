# backend/db/scheme.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    score = db.Column(db.Float)
    resume_link = db.Column(db.String(255))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    candidates = db.relationship('Candidate', backref='job', lazy=True)
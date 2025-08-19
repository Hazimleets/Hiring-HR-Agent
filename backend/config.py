# backend/config.py

import os

class Config:
    DB_URI = os.getenv("DB_URI", "sqlite:///chatbot4.db")
    DEBUG = True
import firebase_admin
from firebase_admin import credentials
import os
from core.config.settings import settings

# Load credentials from an environment variable
# CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "backend/src/core/config/quiz_auth.json")

# Initialize Firebase app
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)


def verify_user_token(id_token: str):
    return firebase_admin.auth.verify_id_token(id_token)

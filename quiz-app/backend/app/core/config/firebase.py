import firebase_admin
from firebase_admin import credentials,auth
from .settings import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)


def verify_firebase_token(token: str):
    return auth.verify_id_token(token)

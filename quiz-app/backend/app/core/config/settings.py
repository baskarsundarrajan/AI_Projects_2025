import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Quizzy"
    VERSION = "1.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Firebase
    FIREBASE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Celery
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    # weaviate
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

    # Temp folder
    TMP_FOLDER = os.getenv("TMP_FOLDER")

    # API Key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


settings = Settings()

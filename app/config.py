import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.environ["API_KEY"]

CELERY_BACKEND: str = os.environ["CELERY_BACKEND"]
CELERY_BROKER: str = os.environ["CELERY_BROKER"]

POSTGRES_DB: str = os.environ["POSTGRES_DB"]
POSTGRES_USER: str = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]

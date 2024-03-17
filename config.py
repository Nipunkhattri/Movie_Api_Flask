from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class AppConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 1)))  # Read expiration time from environment variable

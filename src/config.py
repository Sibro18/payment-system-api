import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_KEY_WEBHOOK = os.getenv("SECRET_KEY_WEBHOOK")
    
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
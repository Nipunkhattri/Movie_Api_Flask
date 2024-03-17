import bcrypt
from app import app

def get_hashed_password(password:str)->bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password:bytes, hashed_password:bytes)->bool:
    return bcrypt.checkpw(password, hashed_password)

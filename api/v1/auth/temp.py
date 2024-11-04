import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from itsdangerous import URLSafeTimedSerializer
from passlib.context import CryptContext

load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from jose import jwt
from dotenv import load_dotenv
import os

from core.auth import (
    bcrypt_context,
    s,
)
from .models import (
    Users,
    PasswordReset,
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def send_mail(to: str, msg):
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL(
            os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")), timeout=5
        ) as server:
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(msg["From"], [to], msg.as_string())
    except Exception as e:
        print(e)


def send_verification_email(user_email: str):
    token = s.dumps(user_email, salt="email-verify")
    # to be changed
    verification_link = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"
    msg = MIMEText(f"Click the link to verify your email: {verification_link}")
    msg["Subject"] = "Verify your email"
    send_mail(user_email, msg)


def send_reset_email(user_email: str, otp: int):
    msg = MIMEText(f"Your one time password is: {otp}")
    msg["Subject"] = "Reset your password"
    send_mail(user_email, msg)


def check_otp(otp: int, db):
    obj = db.query(PasswordReset).filter(PasswordReset.otp == otp).first()
    if not obj:
        return False
    if obj.expires_date < datetime.now(timezone.utc) or obj.used:
        return False
    return obj


def authenticate_user(email: str, password: str, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(email: str, user_id: int) -> str:
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS"))
    )
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(email: str, user_id: int) -> str:
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + timedelta(
        days=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
    )
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

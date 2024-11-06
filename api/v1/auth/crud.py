from core.auth import bcrypt_context
from .models import Users, PasswordReset
from ..profile import Profile


def create_user(email: str, password: str):
    user = Users(
        email=email,
        hashed_password=bcrypt_context.hash(password),
    )

    return user


def create_password_reset(email: str, otp: int):
    password_reset = PasswordReset(
        email=email,
        otp=otp,
    )

    return password_reset


def create_profile(email: str, id: int):
    profile = Profile(
        username=email[: email.find("@")],
        id=id,
    )

    return profile


def get_user(email: str, db):
    return db.query(Users).filter(Users.email == email).first()


def get_profile(id: int, db):
    return db.query(Profile).filter(Profile.id == id).first()

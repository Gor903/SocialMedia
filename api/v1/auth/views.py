import random

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from itsdangerous import SignatureExpired, BadSignature
from jose import JWTError

from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.dependencies.utils import get_current_user
from .auth import (
    create_access_token,
    authenticate_user,
    send_verification_email,
    create_refresh_token,
    send_reset_email,
    check_otp,
)
from .schemas import (
    CreateUserRequest,
    Token,
    ChangePassword,
    PasswordResetForm,
)
from .temp import bcrypt_context, s
from .models import Users, PasswordReset
from api.v1.profile import Profile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        hashed_password=bcrypt_context.hash(create_user_request.password),
        email=create_user_request.email,
    )

    send_verification_email(create_user_request.email)
    db.add(create_user_model)
    db.commit()


@router.get("/verify-email")
async def verify_email(token: str, db: db_dependency):
    try:
        email = s.loads(
            token, salt="email-verify", max_age=3600
        )  # Token expires in 1 hour
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Verification token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    profile = db.query(Profile).filter(Profile.id == user.id).first()
    if not profile:
        profile = Profile(
            username=email[: email.find("@")],
            id=user.id,
        )
    db.add(profile)
    db.commit()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

    if not user.email_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token: str = create_access_token(user.email, user.id)
    refresh_token: str = create_refresh_token(user.email, user.id)

    user.refresh_token = refresh_token
    db.commit()

    return {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str, db: db_dependency):
    try:
        # Decode the refresh token
        payload = await get_current_user(token=refresh_token)
        email = payload.get("email")
        id = payload.get("id")

        # Validate user and refresh token
        user = db.query(Users).filter(Users.email == email).first()

        if not user or user.refresh_token != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Generate a new access token
        new_access_token = create_access_token(email=email, user_id=id)
        new_refresh_token = create_refresh_token(email=email, user_id=id)

        user.refresh_token = new_refresh_token
        db.commit()

        return {
            "refresh_token": new_refresh_token,
            "access_token": new_access_token,
            "token_type": "bearer",
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.patch(
    "/change_password",
    status_code=status.HTTP_201_CREATED,
)
async def change_password(
    db: db_dependency, request: ChangePassword, user: user_dependency
):
    user = authenticate_user(user["email"], request.current_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password!!!"
        )

    new_hashed_password = bcrypt_context.hash(request.new_password)
    user.hashed_password = new_hashed_password
    db.add(user)
    db.commit()
    return {"message": "Password updated successfully"}


@router.post("/forgot-password/")
async def forgot_password(email: str, db: db_dependency):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    otp = random.randint(1000000, 9999999)
    password_reset = PasswordReset(
        email=email,
        otp=otp,
    )
    db.add(password_reset)
    db.commit()
    send_reset_email(email, otp)
    return {"message": "Password reset email sent"}


@router.post("/reset-password/")
async def reset_password(data: PasswordResetForm, db: db_dependency):
    otp = check_otp(data.otp, db)
    if not otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    otp.used = True
    user = db.query(Users).filter(Users.email == otp.email).first()

    user.hashed_password = bcrypt_context.hash(data.new_password)
    db.commit()

    return {"message": "Password reseted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette import status
from typing import Annotated, Dict
from itsdangerous import SignatureExpired, BadSignature
import random

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.dependencies.utils import (
    get_current_user,
)
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
from core.auth import (
    bcrypt_context,
    s,
)
from . import crud


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    db: db_dependency,
    user: CreateUserRequest,
) -> None:
    user = crud.create_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not register user",
        )

    send_verification_email(user.email)

    db.add(user)
    db.commit()


@router.get(
    path="/verify-email",
)
async def verify_email(
    token: str,
    db: db_dependency,
) -> None:
    try:
        email = s.loads(
            token,
            salt="email-verify",
            max_age=3600,
        )
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Verification token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud.get_user(
        email=email,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.email_verified = True
    profile = crud.get_profile(
        id=user.id,
        db=db,
    )
    if not profile:
        profile = crud.create_profile(
            email=email,
            id=user.id,
        )

    db.add(profile)
    db.commit()


@router.post(
    path="/login",
    response_model=Token,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
) -> Dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=400,
            detail="Email not verified",
        )

    access_token: str = create_access_token(user.email, user.id)
    refresh_token: str = create_refresh_token(user.email, user.id)

    user.refresh_token = refresh_token

    db.commit()

    return {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    path="/refresh",
)
async def refresh_token(
    refresh_token: str,
    db: db_dependency,
) -> Dict[str, str]:
    payload = await get_current_user(token=refresh_token)
    email = payload.get("email")
    id = payload.get("id")

    user = crud.get_user(
        email=email,
        db=db,
    )

    if not user or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(email=email, user_id=id)
    new_refresh_token = create_refresh_token(email=email, user_id=id)

    user.refresh_token = new_refresh_token

    db.commit()

    return {
        "refresh_token": new_refresh_token,
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.patch(
    path="/change_password",
    status_code=status.HTTP_201_CREATED,
)
async def change_password(
    db: db_dependency,
    request: ChangePassword,
    user: user_dependency,
) -> None:
    user = authenticate_user(user["email"], request.current_password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password!!!"
        )

    new_hashed_password = bcrypt_context.hash(request.new_password)
    user.hashed_password = new_hashed_password

    db.add(user)
    db.commit()


@router.post(
    path="/forgot-password/",
)
async def forgot_password(
    email: str,
    db: db_dependency,
) -> None:
    user = crud.get_user(
        email=email,
        db=db,
    )
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    otp = random.randint(1000000, 9999999)

    password_reset = crud.create_password_reset(
        email=email,
        otp=otp,
    )

    db.add(password_reset)

    db.commit()
    send_reset_email(email, otp)


@router.post(
    path="/reset-password/",
)
async def reset_password(
    data: PasswordResetForm,
    db: db_dependency,
) -> None:
    otp = check_otp(data.otp, db)
    if not otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    otp.used = True

    user = crud.get_user(
        email=otp.email,
        db=db,
    )

    user.hashed_password = bcrypt_context.hash(data.new_password)

    db.commit()

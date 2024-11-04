from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from datetime import datetime, timedelta, timezone


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped[str | None] = mapped_column(String, nullable=True)


class PasswordReset(Base):
    __tablename__ = "passwordreset"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    otp: Mapped[int] = mapped_column(nullable=False)
    expires_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    used: Mapped[bool] = mapped_column(Boolean, default=False)

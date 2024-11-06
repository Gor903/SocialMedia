from datetime import datetime, timezone, timedelta

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from api.v1.profile.models import Profile


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))

    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    owner: Mapped[Profile] = relationship(
        "Profile", back_populates="activities", cascade="all, delete"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="activity",
        cascade="all, delete",
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    commenter_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))
    activity_id: Mapped[int] = mapped_column(Integer, ForeignKey("activities.id"))
    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    commenter: Mapped[Profile] = relationship("Profile", back_populates="comments")
    activity: Mapped["Talk"] = relationship("Activity", back_populates="comments")


class Talk(Activity):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(ForeignKey("activities.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])

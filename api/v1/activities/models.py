from datetime import datetime, timezone, timedelta

from rich.containers import Lines
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
        "Profile",
        back_populates="activities",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="activity",
        cascade="all, delete",
    )
    tagged_people: Mapped[list["ActivityTag"]] = relationship(
        "ActivityTag",
        back_populates="activity",
        cascade="all, delete",
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    commenter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
    )
    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id"), nullable=True
    )
    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id"), nullable=True
    )
    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    commenter: Mapped[Profile] = relationship(
        "Profile",
        back_populates="comments",
    )
    activity: Mapped["Talk"] = relationship(
        "Activity",
        back_populates="comments",
    )
    parent_comment: Mapped["Comment"] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="child_comments",
    )
    child_comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent_comment",
    )


class Talk(Activity):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(ForeignKey("activities.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])


class Post(Activity):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(ForeignKey("activities.id"), primary_key=True)
    content: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    audio: Mapped[str] = mapped_column(String, nullable=True)
    geo_location: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)


class ActivityTag(Base):
    __tablename__ = "activitytags"

    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id"), primary_key=True
    )
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), primary_key=True
    )

    activity: Mapped[Activity] = relationship(
        "Activity",
        foreign_keys=[activity_id],
        back_populates="tagged_people",
    )
    profile: Mapped[Profile] = relationship(
        "Profile",
        foreign_keys=[profile_id],
        back_populates="activities_tagged",
    )


class Reel(Activity):
    __tablename__ = "reels"

    id: Mapped[int] = mapped_column(ForeignKey("activities.id"), primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

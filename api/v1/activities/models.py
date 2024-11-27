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
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True
    )
    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
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
        cascade="all, delete",
    )


class Talk(Activity):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])


class Post(Activity):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    content: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    audio: Mapped[str] = mapped_column(String, nullable=True)
    geo_location: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)


class ActivityTag(Base):
    __tablename__ = "activitytags"

    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True
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

    id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)


class Story(Activity):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    audio: Mapped[str] = mapped_column(String, nullable=True)
    geo_location: Mapped[str] = mapped_column(String, nullable=True)

    _highlight: Mapped["HighlightStories"] = relationship(
        "HighlightStories",
        back_populates="story",
        cascade="all, delete",
    )


class Highlight(Activity):
    __tablename__ = "highlights"

    id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String, default="Highlight")
    avatar: Mapped[str] = mapped_column(String, default="No data image")

    stories: Mapped[list["HighlightStories"]] = relationship(
        "HighlightStories",
        back_populates="highlight",
        cascade="all, delete",
    )


class HighlightStories(Base):
    __tablename__ = "highlight_stories"

    highlight_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("highlights.id", ondelete="CASCADE"), primary_key=True
    )
    story_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True
    )

    highlight: Mapped[Activity] = relationship(
        "Highlight",
        foreign_keys=[highlight_id],
        back_populates="stories",
    )
    story: Mapped[Profile] = relationship(
        "Story",
        foreign_keys=[story_id],
        back_populates="_highlight",
    )

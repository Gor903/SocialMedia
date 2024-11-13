from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from api.v1.activities import Comment, Activity, PostTag


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    bio: Mapped[str | None] = mapped_column(String, nullable=True)
    social_links: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    followers: Mapped[list["Follows"]] = relationship(
        "Follows",
        foreign_keys="Follows.followee_id",
        back_populates="followee",
        cascade="all, delete",  # Optional: Define cascading behavior
    )
    following: Mapped[list["Follows"]] = relationship(
        "Follows",
        foreign_keys="Follows.follower_id",
        back_populates="follower",
        cascade="all, delete",  # Optional: Define cascading behavior
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="commenter",
        cascade="all, delete",
    )

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="owner",
        cascade="all, delete",
    )

    posts_tagged: Mapped[list["PostTag"]] = relationship(
        "PostTag",
        back_populates="profile",
        cascade="all, delete"
    )


class Follows(Base):
    __tablename__ = "follows"

    follower_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), primary_key=True
    )
    followee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), primary_key=True
    )

    follower: Mapped[Profile] = relationship(
        "Profile", foreign_keys=[follower_id], back_populates="following"
    )
    followee: Mapped[Profile] = relationship(
        "Profile", foreign_keys=[followee_id], back_populates="followers"
    )

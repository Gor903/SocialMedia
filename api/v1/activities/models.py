from datetime import datetime, timezone, timedelta

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from api.v1.profile.models import Profile


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    commenter_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))
    talk_id: Mapped[int] = mapped_column(Integer, ForeignKey("talks.id"))
    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    commenter: Mapped[Profile] = relationship("Profile", back_populates="comments")
    talk: Mapped["Talk"] = relationship("Talk", back_populates="comments")


class Talk(Base):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])
    talker_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))
    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    talker: Mapped[Profile] = relationship(
        "Profile", back_populates="talks", cascade="all, delete"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="talk",
        cascade="all, delete",
    )

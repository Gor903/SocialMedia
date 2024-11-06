from pydantic import BaseModel

from datetime import datetime
from typing import List, Annotated

from api.v1.profile.schemas import (
    ProfileDemoResponse,
)


class CommentResponse(BaseModel):
    id: int
    text: str
    commenter: ProfileDemoResponse
    date: datetime


class CommentRequest(BaseModel):
    text: str


class CommentRequestTalk(CommentRequest):
    talk_id: int


class TalkRequest(BaseModel):
    title: str
    text: str
    links: List[str]


class TalkUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    links: List[str] | None = None


class TalkResponse(BaseModel):
    id: int
    title: str
    text: str
    links: Annotated[List[str], None]
    date: datetime
    talker: ProfileDemoResponse
    comments: Annotated[List[CommentResponse], None]

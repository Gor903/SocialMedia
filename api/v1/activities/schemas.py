from pydantic import BaseModel

from datetime import datetime
from typing import List, Annotated

from api.v1.profile.schemas import (
    ProfileDemoResponse,
)


class CommentDemoResponse(BaseModel):
    id: int
    text: str
    date: datetime
    commenter: ProfileDemoResponse


class CommentDetailResponse(CommentDemoResponse):
    talk: "TalkDemoResponse"


class CommentRequest(BaseModel):
    text: str


class CommentRequestTalk(CommentRequest):
    talk_id: int


class TalkRequest(BaseModel):
    title: str
    text: str
    links: List[str] | None = []


class TalkUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    links: List[str] | None = None


class TalkDemoResponse(BaseModel):
    id: int
    title: str
    text: str
    date: datetime
    talker: ProfileDemoResponse


class TalkDetailResponse(TalkDemoResponse):
    links: Annotated[List[str], None]
    comments: Annotated[List[CommentDemoResponse], None]

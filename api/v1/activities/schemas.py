from pydantic import BaseModel

from datetime import datetime
from typing import List, Annotated

from api.v1.profile.schemas import (
    ProfileDemoResponse,
)


class ActivityRequest(BaseModel): ...


class TalkRequest(ActivityRequest):
    title: str
    text: str
    links: List[str] | None = []


class ActivityResponse(BaseModel):
    id: int
    owner: ProfileDemoResponse
    date: datetime


class TalkDemoResponse(ActivityResponse):
    title: str
    text: str
    date: datetime


class TalkDetailResponse(TalkDemoResponse):
    links: Annotated[List[str], None]
    comments: List["CommentDemoResponse"]


class TalkUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    links: List[str] | None = None


class CommentDemoResponse(BaseModel):
    id: int
    text: str
    date: datetime
    commenter: ProfileDemoResponse


class CommentDetailResponse(CommentDemoResponse):
    activity: ActivityResponse


class CommentRequest(BaseModel):
    activity_id: int
    text: str


# class CommentRequestTalk(CommentRequest):
#     talk_id: int

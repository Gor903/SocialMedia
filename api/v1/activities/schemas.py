from datetime import datetime
from typing import List

from pydantic import BaseModel
from api.v1.profile.schemas import ProfileResponse


class CommentBase(BaseModel):
    text: str


class CommentResponse(CommentBase):
    id: int
    date: datetime


class CommentRequest(CommentBase): ...


class CommentRequestTalk(CommentRequest):
    talk_id: int


class TalkRequest(BaseModel):
    text: str


class TalkResponse(BaseModel):
    id: int
    text: str
    date: datetime
    talker: ProfileResponse
    comments: List[CommentResponse]

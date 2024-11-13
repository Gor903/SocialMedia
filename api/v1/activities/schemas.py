from pydantic import BaseModel, model_validator

from datetime import datetime
from typing import List, Annotated, Self


class ActivityRequest(BaseModel): ...


class TalkRequest(ActivityRequest):
    title: str
    text: str
    links: List[str] | None = []


class ActivityResponse(BaseModel):
    id: int
    owner_id: int
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
    commenter_id: int
    parent_comment_id: int | None = None


class CommentDetailResponse(CommentDemoResponse):
    activity_id: int | None = None
    child_comments: List[CommentDemoResponse]


class CommentRequest(BaseModel):
    parent_comment_id: int | None = None
    activity_id: int | None = None
    text: str

    @model_validator(mode="before")
    def check_passwords_match(self) -> Self:
        if len(self.keys()) > 2:
            raise ValueError("One field must be empty")
        return self


class PostRequest(ActivityRequest):
    content: List[str]
    audio: Annotated[str, None] = None
    geo_location: Annotated[str, None] = None
    description: Annotated[str, None] = None

    tagged_people: Annotated[List[int], None] = None
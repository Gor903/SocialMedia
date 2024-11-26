from pydantic import BaseModel, model_validator

from datetime import datetime
from typing import List, Annotated, Self


# activities
class ActivityRequest(BaseModel):
    tagged_people: List[int] | None = None


class ActivityTagResponse(BaseModel):
    profile_id: int


class ActivityResponse(BaseModel):
    id: int
    owner_id: int
    date: datetime


# talks
class TalkRequest(ActivityRequest):
    title: str
    text: str
    links: List[str] | None = []


class TalkDemoResponse(ActivityResponse):
    title: str
    text: str
    date: datetime


class TalkDetailResponse(TalkDemoResponse):
    links: Annotated[List[str], None]
    comments: List["CommentDemoResponse"]
    tagged_people: List["ActivityTagResponse"]


class TalkUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    links: List[str] | None = None
    tagged_people: List[int] | None = None


# comments
class CommentRequest(BaseModel):
    parent_comment_id: int | None = None
    activity_id: int | None = None
    text: str

    @model_validator(mode="before")
    def check_passwords_match(self) -> Self:
        if len(self.keys()) > 2:
            raise ValueError("One field must be empty")
        return self


class CommentDemoResponse(BaseModel):
    id: int
    text: str
    date: datetime
    commenter_id: int
    parent_comment_id: int | None = None
    activity_id: int | None = None


class CommentDetailResponse(CommentDemoResponse):
    child_comments: List[CommentDemoResponse]


# posts
class PostRequest(ActivityRequest):
    content: List[str]
    audio: Annotated[str, None] = None
    geo_location: Annotated[str, None] = None
    description: Annotated[str, None] = None


class PostDemoResponse(ActivityResponse):
    content: List[str]
    description: str | None = None


class PostDetailResponse(PostDemoResponse):
    geo_location: str | None = None
    tagged_people: List["ActivityTagResponse"]
    audio: str | None = None
    comments: List["CommentDemoResponse"]


class PostUpdate(BaseModel):
    content: List[str] | None = None
    audio: str | None = None
    geo_location: str | None = None
    description: str | None = None
    tagged_people: List[int] | None = None


# reels
class ReelRequest(ActivityRequest):
    content: str
    description: Annotated[str, None] = None


class ReelDemoResponse(ActivityResponse):
    content: str
    description: str | None = None


class ReelDetailResponse(ReelDemoResponse):
    tagged_people: List["ActivityTagResponse"]
    comments: List["CommentDemoResponse"]


class ReelUpdate(BaseModel):
    content: str | None = None
    description: str | None = None
    tagged_people: List[int] | None = None


# stories
class StoryRequest(ActivityRequest):
    content: str
    audio: Annotated[str, None] = None
    geo_location: Annotated[str, None] = None


class StoryResponse(ActivityResponse):
    content: str
    geo_location: str | None = None
    tagged_people: List["ActivityTagResponse"]
    audio: str | None = None
    comments: List["CommentDemoResponse"]


class StoryUpdate(BaseModel):
    tagged_people: List[int] | None = None


# highlights
class HighlightRequest(ActivityRequest):
    title: str
    stories: List[int]
    avatar: str


class HighlightResponse(ActivityResponse):
    id: int
    title: str
    stories: List["HighlightStoriesResponse"]
    avatar: str


class HighlightUpdate(BaseModel):
    title: str | None = None
    stories: List[int] | None = None
    avatar: str | None = None
    tagged_people: List[int] | None = None


# highlight_stories
class HighlightStoriesResponse(BaseModel):
    story_id: int

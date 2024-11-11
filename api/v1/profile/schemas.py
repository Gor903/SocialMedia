from pydantic import BaseModel

from typing import List, TYPE_CHECKING

from api.v1.activities.schemas import ActivityResponse


class FollowManagerRequest(BaseModel):
    id: int


class ProfileDemoResponse(BaseModel):
    id: int
    username: str
    name: str | None
    surname: str | None

    class Config:
        from_attributes = True


class ProfileDetailResponse(ProfileDemoResponse):
    bio: str | None
    social_links: List[str] | None
    activities: List["ActivityResponse"] | None


class ProfileUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    bio: str | None = None
    social_links: List[str] | None = None

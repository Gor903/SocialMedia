from typing import List

from pydantic import BaseModel


class FollowManagerRequest(BaseModel):
    id: int


class ProfilesResponse(BaseModel):
    id: int
    username: str
    name: str | None
    surname: str | None

    class Config:
        from_attributes = True


class ProfileResponse(ProfilesResponse):
    bio: str | None
    social_links: List[str] | None


class ProfileUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    bio: str | None = None
    social_links: List[str] | None = None

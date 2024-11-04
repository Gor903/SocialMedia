from typing import Annotated, List
from unittest.mock import patch

from starlette import status

from fastapi import APIRouter, HTTPException

from api.v1.dependencies import db_dependency, user_dependency
from api.v1.profile.crud import (
    get_followees_from_db,
    get_followers_from_db,
    follow_in_db,
    unfollow_in_db,
)
from api.v1.profile.schemas import ProfilesResponse, FollowManagerRequest

router = APIRouter(prefix="/follows", tags=["profiles->follows"])


@router.get(
    path="/followers/self",
    response_model=Annotated[List[ProfilesResponse], None],
)
async def get_my_followers(db: db_dependency, user: user_dependency):
    profiles = get_followers_from_db(user["id"], db)

    return [
        {
            "id": profile.id,
            "username": profile.username,
            "name": profile.name,
            "surname": profile.surname,
        }
        for profile in profiles
    ]


@router.get(
    path="/followees/self",
    response_model=Annotated[List[ProfilesResponse], None],
)
async def get_my_followers(db: db_dependency, user: user_dependency):
    profiles = get_followees_from_db(user["id"], db)

    return [
        {
            "id": profile.id,
            "username": profile.username,
            "name": profile.name,
            "surname": profile.surname,
        }
        for profile in profiles
    ]


@router.get(
    path="/followers/{profile_id}",
    response_model=Annotated[List[ProfilesResponse], None],
)
async def get_my_followers(profile_id: int, db: db_dependency, user: user_dependency):
    profiles = get_followers_from_db(profile_id, db)

    return [
        {
            "id": profile.id,
            "username": profile.username,
            "name": profile.name,
            "surname": profile.surname,
        }
        for profile in profiles
    ]


@router.get(
    path="/followees/{profile_id}",
    response_model=Annotated[List[ProfilesResponse], None],
)
async def get_my_followers(profile_id: int, db: db_dependency, user: user_dependency):
    profiles = get_followees_from_db(profile_id, db)

    return [
        {
            "id": profile.id,
            "username": profile.username,
            "name": profile.name,
            "surname": profile.surname,
        }
        for profile in profiles
    ]


@router.post(
    path="/follow",
    status_code=status.HTTP_201_CREATED,
)
async def follow(
    db: db_dependency, user: user_dependency, followee: FollowManagerRequest
):
    if not follow_in_db(user["id"], followee.id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't follow!!!"
        )
    return True


@router.delete(
    path="/unfollow",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unfollow(
    db: db_dependency, user: user_dependency, followee: FollowManagerRequest
):
    unfollow_in_db(user["id"], followee.id, db)

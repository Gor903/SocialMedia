from math import trunc

from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.profile.schemas import (
    ProfileDemoResponse,
    FollowManagerRequest,
)
from . import crud


router = APIRouter(prefix="/follows", tags=["Profiles->Follows"])


@router.get(
    path="/followers/self",
    response_model=Annotated[List[ProfileDemoResponse], None],
)
async def get_my_followers(
    db: db_dependency,
    user: user_dependency,
) -> List[ProfileDemoResponse]:
    profiles = crud.get_followers(
        id=user["id"],
        db=db,
    )

    return [profile for profile in profiles]


@router.get(
    path="/followees/self",
    response_model=Annotated[List[ProfileDemoResponse], None],
)
async def get_my_followers(
    db: db_dependency,
    user: user_dependency,
) -> List[ProfileDemoResponse]:
    profiles = crud.get_followees(user["id"], db)

    return [profile for profile in profiles]


@router.post(
    path="/follow",
    status_code=status.HTTP_201_CREATED,
)
async def follow(
    db: db_dependency, user: user_dependency, followee: FollowManagerRequest
) -> bool:
    if not crud.follow(user["id"], followee.id, db):
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
) -> None:
    follow = crud.unfollow(
        follower_id=user["id"],
        followee_id=followee.id,
        db=db,
    )

    db.delete(follow)
    db.commit()

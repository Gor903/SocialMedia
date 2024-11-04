from typing import Annotated, List

from fastapi import APIRouter, HTTPException
from starlette import status

from .follows_views import router as follows_router

from api.v1.profile.schemas import (
    ProfilesResponse,
    ProfileResponse,
    ProfileUpdate,
)
from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from .crud import (
    get_profiles_from_db,
    get_profile_from_db,
    update_profile_in_db,
)


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get(path="/all", response_model=Annotated[List[ProfilesResponse], None])
async def get_profiles(db: db_dependency, user: user_dependency):
    profiles = get_profiles_from_db(db)

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
    path="/{profile_id}",
    response_model=Annotated[ProfileResponse, None],
)
async def get_profile(profile_id: int, db: db_dependency, user: user_dependency):
    profile = get_profile_from_db(profile_id, db)

    if not profile:
        raise HTTPException(
            status_code=404, detail=f"User by id: {profile_id} not found!!"
        )

    return profile


@router.patch(
    path="/update",
    status_code=status.HTTP_201_CREATED,
    response_model=Annotated[ProfileResponse, None],
)
async def update_profile(
    user: user_dependency, db: db_dependency, profile_update: ProfileUpdate
):
    profile = update_profile_in_db(
        user["id"], profile_update.model_dump(exclude_unset=True), db
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not update profile!!"
        )
    db.commit()
    return profile

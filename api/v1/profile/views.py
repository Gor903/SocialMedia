from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.profile.schemas import (
    ProfileDemoResponse,
    ProfileDetailResponse,
    ProfileUpdate,
)
from .models import (
    Profile,
)
from . import crud


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get(
    path="/all",
    response_model=Annotated[List[ProfileDemoResponse], None],
)
async def get_profiles(
    db: db_dependency,
    user: user_dependency,
) -> List[ProfileDemoResponse]:
    profiles = crud.get_profiles(db)

    return [profile for profile in profiles]


@router.get(
    path="/{profile_id}",
    response_model=Annotated[ProfileDetailResponse, None],
)
async def get_profile(
    profile_id: int,
    db: db_dependency,
    user: user_dependency,
) -> ProfileDemoResponse:
    if profile_id <= 0:
        profile_id = user["id"]

    profile = crud.get_profile(
        profile_id=profile_id,
        db=db,
    )

    if not profile:
        raise HTTPException(
            status_code=404, detail=f"User by id: {profile_id} not found!!"
        )

    return profile


@router.patch(
    path="/update",
    status_code=status.HTTP_201_CREATED,
    response_model=Annotated[ProfileDetailResponse, None],
)
async def update_profile(
    user: user_dependency,
    db: db_dependency,
    profile_update: ProfileUpdate,
) -> Profile:
    profile = crud.update_profile(
        profile_id=user["id"],
        update_fields=profile_update.model_dump(exclude_unset=True),
        db=db,
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not update profile!!"
        )

    db.commit()

    return profile

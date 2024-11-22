from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    ReelDemoResponse,
    ReelDetailResponse,
    ReelUpdate,
    ReelRequest,
)
from . import crud


router = APIRouter(prefix="/reels", tags=["Activities->Reels"])


@router.get(
    path="/all/{owner_id}",
    response_model=Annotated[List[ReelDemoResponse], None],
)
async def get_reels(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List[ReelDemoResponse]:
    if owner_id <= 0:
        owner_id = user["id"]

    reels = crud.get_reels(owner_id, db)

    return reels


@router.get(
    path="/{reel_id}",
    response_model=Annotated[ReelDetailResponse, None],
)
async def get_reel(
    db: db_dependency,
    user: user_dependency,
    reel_id: int,
) -> ReelDetailResponse:
    reel = crud.get_reel(reel_id, db)

    return reel


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_reel(
    db: db_dependency,
    user: user_dependency,
    reel: ReelRequest,
):
    reel = reel.model_dump(exclude_none=True)

    tagged_people = []
    if reel.get("tagged_people"):
        tagged_people = reel.pop("tagged_people")

    reel = crud.create_reel(user_id=user["id"], reel=reel)

    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create reel",
        )

    db.add(reel)
    db.commit()

    reel_tags = crud.create_tags(reel.id, tagged_people)

    [db.add(reel_tag) for reel_tag in reel_tags]

    db.commit()

    return reel


@router.patch(
    path="/update/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_post(
    db: db_dependency,
    user: user_dependency,
    id: int,
    reel: ReelUpdate,
) -> ReelDetailResponse:
    reel = reel.model_dump(exclude_none=True)

    tagged_people = []
    if reel.get("tagged_people"):
        tagged_people = reel.pop("tagged_people")

    reel = crud.update_reel(
        id=id,
        update_fields=reel,
        db=db,
    )

    crud.update_tags(
        activity_id=id,
        db=db,
        tags=tagged_people,
    )

    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not update reel",
        )

    db.commit()

    return reel


@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reel(
    db: db_dependency,
    user: user_dependency,
    reel_id: int,
) -> None:
    reel = crud.get_reel(
        id=reel_id,
        db=db,
    )

    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find reel"
        )

    db.delete(reel)
    db.commit()

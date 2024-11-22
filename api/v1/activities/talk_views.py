from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    TalkRequest,
    TalkDemoResponse,
    TalkDetailResponse,
    TalkUpdate,
)
from . import crud

from api.v1.activities.models import Activity, Talk

router = APIRouter(prefix="/talks", tags=["Activities->Talks"])


@router.get(
    path="/all/{owner_id}",
    response_model=Annotated[List[TalkDemoResponse], None],
)
async def get_talks(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List[TalkDemoResponse]:
    if owner_id <= 0:
        owner_id = user["id"]

    talks = crud.get_talks(owner_id, db)

    return [talk for talk in talks]


@router.get(
    path="/{talk_id}",
    response_model=Annotated[TalkDetailResponse, None],
)
async def get_talk(
    db: db_dependency,
    user: user_dependency,
    talk_id: int,
) -> TalkDetailResponse:
    talk = crud.get_talk(talk_id, db)
    return talk


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_talk(
    db: db_dependency,
    user: user_dependency,
    talk: TalkRequest,
) -> TalkDetailResponse:
    talk_dict = talk.model_dump()

    talk = crud.create_talk(
        owner_id=user["id"],
        talk=talk_dict,
    )

    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create talk",
        )

    db.add(talk)
    db.commit()

    return talk


@router.patch(
    path="/update/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_talk(
    db: db_dependency,
    user: user_dependency,
    id: int,
    talk: TalkUpdate,
) -> TalkDetailResponse:
    talk = talk.model_dump(exclude_none=True)

    tagged_people = []
    if talk.get("tagged_people"):
        tagged_people = talk.pop("tagged_people")

    talk = crud.update_talk(
        id=id,
        update_fields=talk,
        db=db,
    )

    crud.update_tags(
        activity_id=id,
        db=db,
        tags=tagged_people,
    )

    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create talk",
        )

    db.commit()

    return talk


@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_talk(
    db: db_dependency,
    user: user_dependency,
    talk_id: int,
) -> None:
    talk = crud.get_talk(
        id=talk_id,
        db=db,
    )

    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find talk"
        )

    db.delete(talk)
    db.commit()

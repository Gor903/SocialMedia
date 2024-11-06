from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    TalkRequest,
    TalkResponse,
    TalkUpdate,
)
from . import crud


router = APIRouter(prefix="/talks", tags=["talks"])


@router.get(
    path="/talks/{owner_id}",
    response_model=Annotated[List[TalkResponse], None],
)
async def get_talks(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List[TalkResponse]:
    if owner_id <= 0:
        owner_id = user["id"]

    talks = crud.get_talks(owner_id, db)

    return [talk for talk in talks]


@router.get(
    path="/talks/{talk_id}",
    response_model=Annotated[TalkResponse, None],
)
async def get_talk(
    db: db_dependency,
    user: user_dependency,
    talk_id: int,
) -> TalkResponse:
    talk = crud.get_talk(talk_id, db)

    return talk


@router.post(
    path="/create/talk",
    status_code=status.HTTP_201_CREATED,
)
async def create_talk(
    db: db_dependency,
    user: user_dependency,
    talk: TalkRequest,
) -> TalkResponse:
    talk = crud.create_talk(
        talker_id=user["id"],
        talk=talk.model_dump(),
    )

    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not create talk"
        )

    db.add(talk)
    db.commit()

    return talk


@router.patch(
    path="/update/talk/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_talk(
    db: db_dependency,
    user: user_dependency,
    id: int,
    talk: TalkUpdate,
) -> TalkResponse:
    talk = crud.update_talk(
        id=id,
        update_fields=talk.model_dump(exclude_none=True),
        db=db,
    )

    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create talk",
        )

    db.commit()

    return talk

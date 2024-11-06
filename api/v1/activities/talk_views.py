from xml.dom.minicompat import NodeList

from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from fastapi.dependencies.utils import get_typed_return_annotation
from starlette import status

from api.v1.activities.models import Comment, Talk
from api.v1.activities.schemas import (
    CommentRequestTalk,
    TalkRequest,
    TalkResponse,
    TalkUpdate,
)
from api.v1.dependencies import db_dependency, user_dependency

from .crud import create_talk, get_talks_from_db, get_talk_from_db, update_talk_in_db

router = APIRouter(prefix="/talks", tags=["talks"])


@router.get(
    path="/talks/{owner_id}",
    response_model=Annotated[List[TalkResponse], None],
)
async def get_my_talks(db: db_dependency, user: user_dependency, owner_id: int):
    if owner_id <= 0:
        owner_id = user["id"]
    print(owner_id)
    talks = get_talks_from_db(owner_id, db)
    return [
        {
            "id": talk.id,
            "title": talk.title,
            "text": talk.text,
            "links": [link for link in talk.links] if talk.links else [],
            "date": talk.date,
            "talker": talk.talker,
            "comments": [comment for comment in talk.comments],
        }
        for talk in talks
    ]


@router.get(
    path="/talks/{owner_id}/{talk_id}",
    response_model=Annotated[TalkResponse, None],
)
async def get_my_talks(db: db_dependency, user: user_dependency, talk_id: int):
    talk = get_talk_from_db(talk_id, db)
    return {
        "id": talk.id,
        "title": talk.title,
        "text": talk.text,
        "links": [link for link in talk.links] if talk.links else [],
        "date": talk.date,
        "talker": talk.talker,
        "comments": [comment for comment in talk.comments],
    }


@router.post(
    path="/add/talk",
    status_code=status.HTTP_201_CREATED,
)
async def add_talk(db: db_dependency, user: user_dependency, talk: TalkRequest):
    talk = create_talk(
        title=talk.title,
        text=talk.text,
        talker_id=user["id"],
        db=db,
    )
    if talk.id:
        return talk
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Could not create talk"
    )


@router.patch(
    path="/update/talk/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_talk(
    db: db_dependency, user: user_dependency, id: int, talk: TalkUpdate
):
    talk = update_talk_in_db(
        id=id,
        update_fields=talk.model_dump(exclude_none=True),
        db=db,
    )
    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not create talk"
        )
    db.commit()
    return talk

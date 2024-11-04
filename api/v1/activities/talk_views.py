from xml.dom.minicompat import NodeList

from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from fastapi.dependencies.utils import get_typed_return_annotation
from starlette import status

from api.v1.activities.models import Comment, Talk
from api.v1.activities.schemas import CommentRequestTalk, TalkRequest, TalkResponse
from api.v1.dependencies import db_dependency, user_dependency

from .crud import create_talk, get_my_talks_from_db, get_my_talk_from_db

router = APIRouter(prefix="/talks", tags=["talks"])


@router.get(
    path="/my_talks",
    response_model=Annotated[List[TalkResponse], None],
)
async def get_my_talks(db: db_dependency, user: user_dependency):
    talks = get_my_talks_from_db(user["id"], db)
    print(talks[0].talker.username)
    return [
        {
            "id": talk.id,
            "text": talk.text,
            "date": talk.date,
            "talker": talk.talker,
            "comments": [comment for comment in talk.comments],
        }
        for talk in talks
    ]


@router.get(
    path="/my_talks/{id}",
    # response_model=Annotated[List[TalkResponse], None],
)
async def get_my_talks(id: int, db: db_dependency, user: user_dependency):
    talk = get_my_talk_from_db(id, user["id"], db)
    return {
        "id": talk.id,
        "text": talk.text,
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
        text=talk.text,
        talker_id=user["id"],
        db=db,
    )
    if talk.id:
        return talk
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Could not create talk"
    )

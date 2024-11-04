from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from fastapi.dependencies.utils import get_typed_return_annotation
from starlette import status

from api.v1.activities.models import Comment, Talk
from api.v1.activities.schemas import CommentRequestTalk, TalkRequest
from api.v1.dependencies import db_dependency, user_dependency

from .crud import create_talk

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/")
async def hello(db: db_dependency, user: user_dependency):
    com = db.query(Comment).first()
    return com


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

from sndhdr import tests
from sys import prefix

from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from fastapi.dependencies.utils import get_typed_return_annotation
from starlette import status

from api.v1.activities.models import Comment, Talk
from api.v1.activities.schemas import CommentRequestTalk, TalkRequest
from api.v1.dependencies import db_dependency, user_dependency

from .crud import create_comment_to_talk

router = APIRouter(prefix="/comment", tags=["Activities->Comments"])


@router.post(
    path="/add",
    status_code=status.HTTP_201_CREATED,
)
async def add_comment_to_talk(
    db: db_dependency, user: user_dependency, comment: CommentRequestTalk
):
    comment = create_comment_to_talk(
        text=comment.text,
        user_id=user["id"],
        talk_id=comment.talk_id,
        db=db,
    )
    print(comment)
    if comment.id:
        return comment
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Could not create comment"
    )

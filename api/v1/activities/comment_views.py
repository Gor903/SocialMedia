from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    CommentRequest,
    CommentDemoResponse,
    CommentDetailResponse,
)
from . import crud


router = APIRouter(prefix="/comment", tags=["Activities->Comments"])


@router.get(
    path="/",
    response_model=Annotated[List[CommentDemoResponse], None],
)
async def get_comments(
    db: db_dependency, user: user_dependency
) -> List[CommentDemoResponse]:
    comments = crud.get_comments(
        user_id=user["id"],
        db=db,
    )

    return comments


@router.get(
    path="/{comment_id}",
    response_model=Annotated[List[CommentDetailResponse], None],
)
async def get_comment(
    comment_id: int, db: db_dependency, user: user_dependency
) -> CommentDetailResponse:
    comment = crud.get_comment(
        comment_id=comment_id,
        db=db,
    )

    return comment


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=Annotated[CommentDemoResponse, None],
)
async def add_comment_to_talk(
    db: db_dependency,
    user: user_dependency,
    comment: CommentRequest,
) -> CommentDemoResponse:
    comment = crud.create_comment(
        commenter_id=user["id"],
        comment=comment.model_dump(),
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create comment",
        )

    db.add(comment)
    db.commit()

    return comment

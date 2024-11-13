from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    PostRequest
)
from . import crud


router = APIRouter(prefix="/posts", tags=["Activities->Posts"])


@router.post(
    path="/create/talk",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    db: db_dependency,
    user: user_dependency,
    post: PostRequest,
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="create post then posttags",
    )

    post = crud.create_post(
        user_id=user["id"],
        post=post.model_dump(exclude_none=True)
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create talk",
        )
    db.add(post)
    db.commit()

    return post
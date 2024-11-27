from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    PostRequest,
    PostDemoResponse,
    PostDetailResponse,
    PostUpdate,
)
from . import crud


router = APIRouter(prefix="/posts", tags=["Activities->Posts"])


@router.get(
    path="/all/{owner_id}",
    response_model=Annotated[List[PostDemoResponse], None],
)
async def get_talks(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List[PostDemoResponse]:
    if owner_id <= 0:
        owner_id = user["id"]

    posts = crud.get_posts(owner_id, db)

    return posts


@router.get(
    path="/{post_id}",
    response_model=Annotated[PostDetailResponse, None],
)
async def get_post(
    db: db_dependency,
    user: user_dependency,
    post_id: int,
) -> PostDetailResponse:
    post = crud.get_post(post_id, db)

    return post


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    db: db_dependency,
    user: user_dependency,
    post: PostRequest,
):
    post = post.model_dump(exclude_none=True)

    tagged_people = post.pop("tagged_people") if post.get("tagged_people") else []

    post = crud.create_post(user_id=user["id"], post=post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create post",
        )

    db.add(post)
    db.commit()

    post_tags = crud.create_tags(post.id, tagged_people)

    [db.add(post_tag) for post_tag in post_tags]

    db.commit()

    return post


@router.patch(
    path="/update/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_post(
    db: db_dependency,
    user: user_dependency,
    id: int,
    post: PostUpdate,
) -> PostDetailResponse:
    post = post.model_dump(exclude_none=True)

    tagged_people = post.pop("tagged_people") if post.get("tagged_people") else []

    post = crud.update_post(
        id=id,
        update_fields=post,
        db=db,
    )

    crud.update_tags(
        activity_id=id,
        db=db,
        tags=tagged_people,
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not update post",
        )

    db.commit()

    return post


@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    db: db_dependency,
    user: user_dependency,
    post_id: int,
) -> None:
    post = crud.get_post(
        id=post_id,
        db=db,
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find post"
        )

    db.delete(post)
    db.commit()

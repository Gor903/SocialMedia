from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    StoryResponse,
    StoryRequest,
    StoryUpdate,
)
from . import crud


router = APIRouter(prefix="/stories", tags=["Activities->Stories"])


@router.get(
    path="/available/{owner_id}",
    response_model=Annotated[List, None],
)
def get_available_stories(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List:
    if owner_id <= 0:
        owner_id = user["id"]

    stories = crud.get_available_stories(
        user_id=owner_id,
        db=db,
    )

    return stories


@router.get(
    path="/{story_id}",
    response_model=Annotated[StoryResponse, None],
)
async def get_story(
    db: db_dependency,
    user: user_dependency,
    story_id: int,
) -> StoryResponse:
    story = crud.get_story(story_id, db)

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find story."
        )

    return story


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_story(
    db: db_dependency,
    user: user_dependency,
    story: StoryRequest,
):
    story = story.model_dump(exclude_none=True)

    tagged_people = []
    if story.get("tagged_people"):
        tagged_people = story.pop("tagged_people")

    story = crud.create_story(user_id=user["id"], story=story)

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create reel",
        )

    db.add(story)
    db.commit()

    story_tags = crud.create_tags(story.id, tagged_people)

    [db.add(story_tag) for story_tag in story_tags]

    db.commit()

    return story


@router.patch(
    path="/update/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_story(
    db: db_dependency,
    user: user_dependency,
    id: int,
    story: StoryUpdate,
) -> StoryResponse:
    story = story.model_dump(exclude_none=True)

    tagged_people = []
    if story.get("tagged_people"):
        tagged_people = story.pop("tagged_people")

    story = crud.update_story(
        id=id,
        update_fields=story,
        db=db,
    )

    crud.update_tags(
        activity_id=id,
        db=db,
        tags=tagged_people,
    )

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create story",
        )

    db.commit()

    return story


@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_story(
    db: db_dependency,
    user: user_dependency,
    story_id: int,
) -> None:
    story = crud.get_story(
        id=story_id,
        db=db,
    )

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find story"
        )

    db.delete(story)
    db.commit()

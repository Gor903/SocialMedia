from fastapi import APIRouter, HTTPException

from starlette import status
from typing import Annotated, List

from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)
from api.v1.activities.schemas import (
    HighlightRequest,
    HighlightResponse,
    HighlightUpdate,
)

from . import crud


router = APIRouter(prefix="/highlights", tags=["Activities->Highlights"])


@router.get(
    path="/all/{owner_id}",
    response_model=Annotated[List[HighlightResponse], None],
)
async def get_highlights(
    db: db_dependency,
    user: user_dependency,
    owner_id: int,
) -> List[HighlightResponse]:
    if owner_id <= 0:
        owner_id = user["id"]

    highlights = crud.get_highlights(owner_id, db)

    return highlights


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_highlight(
    db: db_dependency,
    user: user_dependency,
    highlight: HighlightRequest,
):
    highlight = highlight.model_dump(exclude_none=True)

    tagged_people = (
        highlight.pop("tagged_people") if highlight.get("tagged_people") else []
    )
    stories = highlight.pop("stories") if highlight.get("stories") else []

    highlight = crud.create_highlight(owner_id=user["id"], highlight=highlight)

    if not highlight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create highlight",
        )

    db.add(highlight)
    db.commit()

    highlight_tags = crud.create_tags(highlight.id, tagged_people)

    [db.add(highlight_tag) for highlight_tag in highlight_tags]

    stories = crud.create_highlight_stories(highlight.id, stories)

    [db.add(story) for story in stories]

    db.commit()

    return highlight


@router.patch(
    path="/update/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_post(
    db: db_dependency,
    user: user_dependency,
    id: int,
    highlight: HighlightUpdate,
) -> HighlightResponse:
    highlight = highlight.model_dump(exclude_none=True)

    tagged_people = (
        highlight.pop("tagged_people") if highlight.get("tagged_people") else []
    )
    stories = highlight.pop("stories") if highlight.get("stories") else []

    highlight = crud.update_highlight(
        id=id,
        update_fields=highlight,
        db=db,
    )

    crud.update_tags(
        activity_id=id,
        db=db,
        tags=tagged_people,
    )

    highlight_stories = crud.update_highlight_stories(
        highlight_id=id,
        stories=stories,
        db=db,
    )

    if not highlight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not update highlight",
        )

    [db.add(highlight_story) for highlight_story in highlight_stories]
    db.commit()

    return highlight


@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_highlight(
    db: db_dependency,
    user: user_dependency,
    highlight_id: int,
) -> None:
    highlight = crud.get_highlight(
        id=highlight_id,
        db=db,
    )

    if not highlight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find highlight"
        )

    db.delete(highlight)
    db.commit()

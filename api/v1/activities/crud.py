from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from .models import Comment, Talk


def create_talk(text: str, talker_id: int, db):
    talk = Talk(
        text=text,
        talker_id=talker_id,
    )
    db.add(talk)
    db.commit()
    return talk


def get_my_talks_from_db(user_id: int, db):
    query = (
        select(Talk)
        .options(
            selectinload(Talk.talker),
            selectinload(Talk.comments),
        )
        .where(Talk.talker_id == user_id)
    )
    talks = db.execute(query).scalars().all()
    return talks


def get_my_talk_from_db(id: int, user_id: int, db):
    query = (
        select(Talk)
        .options(selectinload(Talk.talker), selectinload(Talk.comments))
        .where(Talk.id == id, Talk.talker_id == user_id)
    )
    talk = db.execute(query).scalars().first()
    return talk


def create_comment_to_talk(text: str, user_id: int, talk_id: int, db):
    comment = Comment(
        text=text,
        commenter_id=user_id,
        talk_id=talk_id,
    )
    db.add(comment)
    db.commit()
    return comment

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from .models import Comment, Talk


def create_talk(title: str, text: str, talker_id: int, db):
    talk = Talk(
        title=title,
        text=text,
        talker_id=talker_id,
    )
    db.add(talk)
    db.commit()
    return talk


def update_talk_in_db(id: int, update_fields: dict, db):
    talk = db.query(Talk).filter_by(id=id).first()

    if not talk:
        return False

    for key, value in update_fields.items():
        setattr(talk, key, value)

    return talk


def get_talks_from_db(user_id: int, db):
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


def get_talk_from_db(id: int, db):
    query = (
        select(Talk)
        .options(selectinload(Talk.talker), selectinload(Talk.comments))
        .where(Talk.id == id)
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

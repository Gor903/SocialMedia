from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import Comment, Talk


def get_talks(user_id: int, db):
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


def get_talk(id: int, db):
    query = (
        select(Talk)
        .options(
            selectinload(Talk.talker),
            selectinload(Talk.comments),
        )
        .where(Talk.id == id)
    )
    talk = db.execute(query).scalars().first()
    return talk


def create_talk(talker_id: int, talk: dict):
    talk = Talk(
        talker_id=talker_id,
        **talk,
    )
    return talk


def update_talk(id: int, update_fields: dict, db):
    talk = db.query(Talk).filter_by(id=id).first()

    if not talk:
        return False

    for key, value in update_fields.items():
        setattr(talk, key, value)

    return talk


def create_comment(text: str, user_id: int, talk_id: int, db):
    comment = Comment(
        text=text,
        commenter_id=user_id,
        talk_id=talk_id,
    )
    db.add(comment)
    db.commit()
    return comment

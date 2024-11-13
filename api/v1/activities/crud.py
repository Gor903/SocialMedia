from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import Comment, Talk, Post, PostTag
from .schemas import PostRequest


def get_talks(user_id: int, db):
    query = (
        select(Talk)
        .options(
            selectinload(Talk.owner),
            selectinload(Talk.comments),
        )
        .where(Talk.owner_id == user_id)
    )
    talks = db.execute(query).scalars().all()
    return talks


def get_talk(id: int, db):
    query = (
        select(Talk)
        .options(
            selectinload(Talk.owner),
            selectinload(Talk.comments),
        )
        .where(Talk.id == id)
    )
    talk = db.execute(query).scalars().first()
    return talk


def create_talk(owner_id: int, talk: dict):
    talk = Talk(
        owner_id=owner_id,
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


def create_comment(commenter_id: int, comment: dict):
    comment = Comment(
        commenter_id=commenter_id,
        **comment,
    )

    return comment


def get_comments(user_id: int, db):
    comments = (
        db.query(Comment)
        .filter(
            Comment.commenter_id == user_id,
        )
        .all()
    )

    return comments


def get_comment(comment_id: int, db):
    comments = (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
        )
        .all()
    )

    return comments

def create_post(user_id: int, post: dict) -> Post:
    tagged_people = None
    if post.get("tagged_people"):
        tagged_people = post.pop("tagged_people")
    print(post)
    post = Post(
        owner_id=user_id,
        **post,
    )

    print(post.id)
    return post
    # if tagged_people:
    #     post_tags = [PostTag(
    #
    #     ) for profile in tagged_people]

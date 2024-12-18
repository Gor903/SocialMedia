from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import Comment, Talk, Post, ActivityTag, Reel


def get_talks(user_id: int, db):
    query = (
        select(Talk)
        .options(
            selectinload(Talk.owner),
            # selectinload(Talk.comments),
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
            selectinload(Talk.tagged_people),
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


def get_posts(user_id: int, db):
    posts = db.query(Post).filter(Post.owner_id == user_id).all()

    return posts


def get_post(id: int, db):
    query = (
        select(Post)
        .options(
            selectinload(Post.owner),
            selectinload(Post.comments),
            selectinload(Post.tagged_people),
        )
        .where(Post.id == id)
    )

    post = db.execute(query).scalars().first()

    return post


def create_post(user_id: int, post: dict) -> Post:
    post = Post(
        owner_id=user_id,
        **post,
    )

    return post


def create_tags(activity_id: int, tagged_people) -> List[ActivityTag]:
    post_tags = [
        ActivityTag(
            activity_id=activity_id,
            profile_id=tagged_account,
        )
        for tagged_account in tagged_people
    ]

    return post_tags


def update_post(id: int, update_fields: dict, db):
    post = get_post(id, db)

    if not post:
        return False

    for key, value in update_fields.items():
        setattr(post, key, value)

    return post


def update_tags(activity_id: int, tags, db):
    post_tags = (
        db.query(ActivityTag).filter(ActivityTag.activity_id == activity_id).all()
    )

    [db.delete(post_tag) for post_tag in post_tags]
    db.commit()

    new_post_tags = create_tags(
        activity_id=activity_id,
        tagged_people=tags,
    )

    [db.add(new_post_tag) for new_post_tag in new_post_tags]


def get_reels(user_id: int, db):
    reels = db.query(Reel).filter(Post.owner_id == user_id).all()

    return reels


def get_reel(id: int, db):
    query = (
        select(Reel)
        .options(
            selectinload(Reel.owner),
            selectinload(Reel.comments),
            selectinload(Reel.tagged_people),
        )
        .where(Reel.id == id)
    )

    reel = db.execute(query).scalars().first()

    return reel


def create_reel(user_id: int, reel: dict) -> Post:
    reel = Reel(
        owner_id=user_id,
        **reel,
    )

    return reel


def update_reel(id: int, update_fields: dict, db):
    reel = get_reel(id, db)

    if not reel:
        return False

    for key, value in update_fields.items():
        setattr(reel, key, value)

    return reel

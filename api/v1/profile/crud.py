from fastapi import HTTPException

from sqlalchemy import select
from starlette import status

from .models import Profile, Follows


def get_profiles_from_db(db) -> list:
    query = select(
        Profile.id, Profile.username, Profile.name, Profile.surname
    ).order_by(Profile.id)
    return db.execute(query)


def get_profile_from_db(id: int, db) -> Profile:
    return db.query(Profile).filter(Profile.id == id).first()


def get_followers_from_db(id: int, db) -> list:
    followers = db.query(Follows).filter(Follows.followee_id == id)
    profiles = [get_profile_from_db(follower.follower_id, db) for follower in followers]
    return profiles


def get_followees_from_db(id: int, db) -> list:
    followers = db.query(Follows).filter(Follows.follower_id == id)
    profiles = [get_profile_from_db(follower.followee_id, db) for follower in followers]
    return profiles


def follow_in_db(follower_id: int, followee_id: int, db):
    if follower_id == followee_id or followee_id == 0:
        return
    exists = (
        db.query(Follows)
        .filter_by(follower_id=follower_id, followee_id=followee_id)
        .first()
    )
    if not exists:
        follow_relation = Follows(follower_id=follower_id, followee_id=followee_id)
        db.add(follow_relation)
        db.commit()
        return True


def update_profile_in_db(id: int, update_fields: dict, db) -> Profile | bool:
    profile = get_profile_from_db(id, db)
    if not profile:
        return False

    for key, value in update_fields.items():
        setattr(profile, key, value)

    return profile


def unfollow_in_db(follower_id: int, followee_id: int, db):
    follow = (
        db.query(Follows)
        .filter(
            Follows.follower_id == follower_id,
            Follows.followee_id == followee_id,
        )
        .first()
    )
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Follow pair does not found!!!",
        )
    db.delete(follow)
    db.commit()

from fastapi import APIRouter

from .v1.auth import router as auth_router
from .v1.profile import profile_router, follows_router
from .v1.activities import (
    talks_router,
    comments_router,
    posts_router,
    reel_router,
    story_router,
    highlight_router,
)

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(follows_router)
router.include_router(talks_router)
router.include_router(comments_router)
router.include_router(posts_router)
router.include_router(reel_router)
router.include_router(story_router)
router.include_router(highlight_router)

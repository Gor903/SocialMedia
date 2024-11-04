from .talk_views import router as talks_router
from .comment_views import router as comments_router
from .models import Comment, Talk

__all__ = [
    "talks_router",
    "comments_router",
    "Comment",
    "Talk",
]

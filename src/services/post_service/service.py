from collections.abc import Sequence

from db.models.post import Posts
from schemas.post import PostCreate
from services.post_service.repository import PostRepository


class PostService:
    """
    Сервис для работы с постами.
    """

    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def create_post(self, author_id: int, data: PostCreate) -> Posts:
        async with self.repository.atomic():
            return await self.repository.create_post(
                author_id=author_id,
                text=data.text,
                recommended_amount_nanoton=data.recommended_amount_nanoton,
            )

    async def get_post(self, post_id: int) -> Posts | None:
        return await self.repository.get_by_id(post_id)

    async def list_posts(self, limit: int = 50, offset: int = 0) -> Sequence[Posts]:
        """
        Лента для фронта
        """
        return await self.repository.list_posts(limit, offset)

    async def list_by_author(self, author_id: int, limit: int = 50, offset: int = 0) -> Sequence[Posts]:
        return await self.repository.list_by_author(author_id, limit, offset)

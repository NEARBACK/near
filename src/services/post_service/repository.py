from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.post import Posts
from db.repository.base import BaseRepository


class PostRepository(BaseRepository):
    """
    Репозиторий для постов.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_post(
        self,
        author_id: int,
        text: str,
        recommended_amount_nanoton: int,
    ) -> Posts:
        return await self.save(
            Posts,
            values={
                "author_id": author_id,
                "text": text,
                "recommended_amount_nanoton": recommended_amount_nanoton,
            },
        )

    async def get_by_id(self, post_id: int) -> Posts | None:
        result = await self.session.scalar(select(Posts).where(Posts.id == post_id))
        return result

    async def list_posts(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Posts]:
        """
        Лента всех постов (по дате создания, DESC).
        """
        result = await self.session.scalars(select(Posts).order_by(Posts.created_at.desc()).limit(limit).offset(offset))
        return result.all()

    async def list_by_author(
        self,
        author_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Posts]:
        result = await self.session.scalars(
            select(Posts)
            .where(Posts.author_id == author_id)
            .order_by(Posts.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.all()

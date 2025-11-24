from collections.abc import Sequence

from sqlalchemy import select

from db.models.user import Users
from db.repository.base import BaseRepository  # или from db.repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Репозиторий для работы с пользователями (Users).
    """

    async def get_by_id(self, user_id: int) -> Users | None:
        result = await self.session.scalar(select(Users).where(Users.id == user_id))
        return result

    async def get_by_wallet(self, wallet_address: str) -> Users | None:
        result = await self.session.scalar(select(Users).where(Users.wallet_address == wallet_address))
        return result

    async def create_user(
        self,
        wallet_address: str,
        display_name: str | None = None,
    ) -> Users:
        return await self.save(
            model=Users,
            values={
                "wallet_address": wallet_address,
                "display_name": display_name,
            },
        )

    async def get_or_create(
        self,
        wallet_address: str,
        display_name: str | None = None,
    ) -> Users:
        user = await self.get_by_wallet(wallet_address)
        if user:
            return user
        return await self.create_user(wallet_address=wallet_address, display_name=display_name)

    async def list_users(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Users]:
        result = await self.session.scalars(select(Users).limit(limit).offset(offset))
        return result.all()

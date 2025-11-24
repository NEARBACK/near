from collections.abc import Sequence

from db.models.user import Users
from schemas.user import UserCreate
from services.user_service.repository import UserRepository


class UserService:
    """
    Сервис для работы с пользователями.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_by_wallet(self, wallet: str) -> Users | None:
        return await self.repository.get_by_wallet(wallet)

    async def get_or_create_user(self, data: UserCreate) -> Users:
        """
        Используется при авторизации через TON Connect.
        """
        async with self.repository.atomic():
            return await self.repository.get_or_create(
                wallet_address=data.wallet_address,
                display_name=data.display_name,
            )

    async def list_users(self, limit: int = 100, offset: int = 0) -> Sequence[Users]:
        return await self.repository.list_users(limit, offset)

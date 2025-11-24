from collections.abc import Sequence

from db.models.donations import Donations
from schemas.donation import DonationConfirm, DonationCreate
from services.donation_service.repository import DonationRepository
from services.post_service.repository import PostRepository


class DonationService:
    """
    Сервис для работы с донатами.
    - Создание заявки на донат.
    - Подтверждение (с фронта TonKeeper tx hash).
    """

    def __init__(self, donation_repo: DonationRepository, post_repo: PostRepository):
        self.donation_repo = donation_repo
        self.post_repo = post_repo

    async def create_donation(
        self,
        post_id: int,
        from_wallet: str,
        data: DonationCreate,
    ) -> Donations:
        """
        Логика инициирования доната.

        - Проверяем, что пост существует
        - Берем wallet автора
        - Создаём запись в БД
        - Возвращаем JSON для фронта (amount + comment)
        """

        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")

        # если донор не указал сумму → используем recommended
        amount = data.amount_nanoton or post.recommended_amount_nanoton

        comment = f"donation:{post_id}"  # или donation:<donation_id> (лучше)

        async with self.donation_repo.atomic():
            donation = await self.donation_repo.create_donation(
                post_id=post_id,
                from_wallet=from_wallet,
                to_wallet=post.author.wallet_address,
                amount_nanoton=amount,
                comment=comment,
                status="PENDING",
            )

        return donation

    async def confirm_donation(self, donation_id: int, data: DonationConfirm) -> Donations | None:
        """
        Подтверждение транзакции после TonConnect.
        """

        async with self.donation_repo.atomic():
            return await self.donation_repo.confirm_donation(
                donation_id=donation_id,
                tx_hash=data.tx_hash,
            )

    async def list_donations_for_post(self, post_id: int) -> Sequence[Donations]:
        return await self.donation_repo.list_for_post(post_id)

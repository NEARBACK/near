from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.donations import Donations
from db.repository.base import BaseRepository


class DonationRepository(BaseRepository):
    """
    Репозиторий для донатов.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_donation(
        self,
        post_id: int,
        from_wallet: str,
        to_wallet: str,
        amount_nanoton: int,
        status: str = "PENDING",
        comment: str | None = None,
    ) -> Donations:
        return await self.save(
            Donations,
            values={
                "post_id": post_id,
                "from_wallet": from_wallet,
                "to_wallet": to_wallet,
                "amount_nanoton": amount_nanoton,
                "status": status,
                "comment": comment,
            },
        )

    async def get_by_id(self, donation_id: int) -> Donations | None:
        result = await self.session.scalar(select(Donations).where(Donations.id == donation_id))
        return result

    async def list_for_post(
        self,
        post_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Donations]:
        result = await self.session.scalars(
            select(Donations)
            .where(Donations.post_id == post_id)
            .order_by(Donations.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.all()

    async def confirm_donation(
        self,
        donation_id: int,
        tx_hash: str,
    ) -> Donations | None:
        """
        Обновление статуса доната на CONFIRMED.
        """
        return await self.update_by(
            Donations,
            values={
                "status": "CONFIRMED",
                "tx_hash": tx_hash,
            },
            custom_filter=(Donations.id == donation_id,),
        )

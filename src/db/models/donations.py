from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class DonationStatus(PyEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


class Donations(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    from_wallet: Mapped[str] = mapped_column(String(128), nullable=False)
    to_wallet: Mapped[str] = mapped_column(String(128), nullable=False)

    amount_nanoton: Mapped[int] = mapped_column(BigInteger, nullable=False)

    status: Mapped[DonationStatus] = mapped_column(Enum(DonationStatus), nullable=False, default=DonationStatus.PENDING)

    tx_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    post: Mapped["Posts"] = relationship("Posts", back_populates="donations")  # type: ignore # noqa F821

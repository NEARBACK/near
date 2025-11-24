"""
CREATE TABLE users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_address      VARCHAR(128) UNIQUE NOT NULL,
    display_name        VARCHAR(64),           -- опционально, можно null
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

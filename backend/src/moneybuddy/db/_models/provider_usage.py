"""Provider usage log model.

Retained as a generic per-user provider usage ledger. The product no longer
exposes assistant features, but existing deployments may still carry these
rows, so the schema remains mapped and upgrade-safe.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from moneybuddy.db._models._constants import USER_FK
from moneybuddy.db.base import Base

if TYPE_CHECKING:
    from moneybuddy.db._models.user import User


class ProviderUsageLog(Base):
    """Single provider usage record."""

    __tablename__ = "ai_usage_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(USER_FK, ondelete="CASCADE"), nullable=False, index=True
    )

    # When the provider event completed.
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        index=True,
    )

    provider_name: Mapped[str] = mapped_column("provider", String(20), nullable=False)
    provider_model: Mapped[str] = mapped_column("model", String(100), nullable=False)

    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    request_rounds: Mapped[int] = mapped_column(
        "tool_rounds",
        Integer,
        nullable=False,
        default=1,
    )

    # Pre-computed USD cost so reports stay query-light.
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    user: Mapped[User] = relationship("User", back_populates="provider_usage_logs")

    __table_args__ = (Index("ix_ai_usage_user_timestamp", "user_id", "timestamp"),)

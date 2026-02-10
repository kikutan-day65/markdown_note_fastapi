import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint("actor_id", "target_id", name="uq_actor_id_target_id"),
        CheckConstraint("actor_id != target_id", name="no_self_follow"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Foreign keys
    actor_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # Relationships (ORM)
    actor: Mapped["User"] = relationship(
        "User", foreign_keys=[actor_id], back_populates="followings"
    )
    target: Mapped["User"] = relationship(
        "User", foreign_keys=[target_id], back_populates="followers"
    )

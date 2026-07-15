import uuid

from app.schemas.base import ORMBase


# ===== RESPONSE =====
class TagSummary(ORMBase):
    id: uuid.UUID
    name: str

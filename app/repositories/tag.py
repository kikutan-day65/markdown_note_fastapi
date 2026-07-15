import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tags_by_ids(self, ids: set[uuid.UUID]) -> list[Tag]:
        stmt = select(Tag).where(Tag.id.in_(ids))

        return self.db.scalars(stmt).all()

    def list_tags(self) -> list[Tag]:
        stmt = select(Tag)

        return self.db.scalars(stmt).all()

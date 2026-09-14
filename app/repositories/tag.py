import uuid

from sqlalchemy import select

from app.models.tag import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    def get_tags_by_ids(self, ids: set[uuid.UUID]) -> list[Tag]:
        stmt = select(Tag).where(Tag.id.in_(ids))

        return self.db.scalars(stmt).all()

    def list_tags(self) -> list[Tag]:
        stmt = select(Tag)

        return self.db.scalars(stmt).all()

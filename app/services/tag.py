from app.models.tag import Tag
from app.repositories.tag import TagRepository


class TagService:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def list_tags(self) -> list[Tag]:
        return self.repository.list_tags()

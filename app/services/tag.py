from app.models.tag import Tag
from app.repositories.tag import TagRepository


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    def list_tags(self) -> list[Tag]:
        return self.repository.list_tags()

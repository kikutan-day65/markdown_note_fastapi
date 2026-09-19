from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, obj) -> None:
        self.db.add(obj)

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, obj) -> None:
        self.db.refresh(obj)

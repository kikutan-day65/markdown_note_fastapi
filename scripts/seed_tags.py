from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.tag import Tag
from scripts.tags import TAG_NAMES


def seed_tags() -> None:
    session = SessionLocal()

    try:
        for tag_name in TAG_NAMES:
            tag_name = tag_name.capitalize()
            stmt = select(Tag).where(Tag.name == tag_name)
            existed = session.scalar(stmt)

            if existed:
                print(f"{tag_name} already exists in db")
                continue

            session.add(Tag(name=tag_name))
            print(f"Added: {tag_name}")

        session.commit()

    except Exception as e:
        session.rollback()
        print(e)

    finally:
        session.close()


if __name__ == "__main__":
    seed_tags()

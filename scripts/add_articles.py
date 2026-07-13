from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.article import Article
from app.models.user import User


def generate_text(num: str) -> str:
    return f"""
        Article {num}

        What is Lorem Ipsum?
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since 1966,
        when designers at Letraset and James Mosley,
        the librarian at St Bride Printing Library in London,
        took a 1914 Cicero translation and scrambled it to make dummy text for
        Letraset's Body Type sheets.

        Why do we use it?
        It is a long established fact that a reader will be distracted by the
        readable content of a page when looking at its layout.
        """


def add_articles() -> None:
    session = SessionLocal()

    try:
        stmt = select(User).where(
            User.username.in_([f"testuser{str(i).zfill(2)}" for i in range(1, 10)])
        )
        users = session.scalars(stmt).all()

        users_by_username = {user.username: user for user in users}

        base_time = datetime.now(timezone.utc)

        for i in range(1, 101):
            num = str(i).zfill(3)
            title = f"Title {num}"
            content = generate_text(num=num)

            user_number = ((i - 1) % 9) + 1
            username = f"testuser{user_number:02d}"

            user = users_by_username.get(username)

            if user is None:
                raise ValueError(f"{username} が存在しません")

            created_at = base_time - timedelta(minutes=i - 1)

            article = Article(
                title=title,
                content=content,
                user_id=user.id,
                created_at=created_at,
                updated_at=created_at,
            )

            session.add(article)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    add_articles()

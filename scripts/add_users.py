from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User


def add_users() -> None:
    session = SessionLocal()

    try:
        users = []

        for i in range(1, 10):
            num = str(i).zfill(2)

            username = f"testuser{num}"
            email = f"testuser{num}@example.com"
            password = "testuser123"

            user = User(
                username=username,
                email=email,
                password_hash=get_password_hash(password),
            )

            users.append(user)

        session.add_all(users)
        session.commit()

        print(f"Created {len(users)} users")

    except Exception as e:
        session.rollback()
        print("Failed to create users")
        print(e)

    finally:
        session.close()


if __name__ == "__main__":
    add_users()

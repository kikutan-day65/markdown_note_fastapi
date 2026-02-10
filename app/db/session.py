from sqlalchemy.orm import sessionmaker

from app.db.engine import engine

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

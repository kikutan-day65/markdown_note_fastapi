from sqlalchemy import URL, create_engine

from app.core.settings import settings

db_url = URL.create(
    drivername=settings.DB_DRIVERNAME,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_engine(db_url, pool_pre_ping=True)

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool


def _database_url() -> URL:
    return URL.create(
        "postgresql+psycopg",
        username=os.environ.get("DB_USER", "recipe"),
        password=os.environ.get("DB_PASSWORD", "recipe"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "recipes"),
    )


# NullPool: open a connection per request and close it afterwards. Aurora Serverless v2 only
# auto-pauses when there are zero connections, so a pool of idle connections would keep it
# running (and billing) 24/7.
# Long connect timeout: Aurora can take 10-20s to resume from 0 ACU.
engine = create_engine(
    _database_url(),
    poolclass=NullPool,
    connect_args={"connect_timeout": 25},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    with SessionLocal() as session:
        yield session

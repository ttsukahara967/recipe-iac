import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def _database_url() -> URL:
    return URL.create(
        "postgresql+psycopg",
        username=os.environ.get("DB_USER", "recipe"),
        password=os.environ.get("DB_PASSWORD", "recipe"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "recipes"),
    )


# Long connect timeout: Aurora Serverless v2 can take 10-20s to resume from 0 ACU
engine = create_engine(
    _database_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
    connect_args={"connect_timeout": 25},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    with SessionLocal() as session:
        yield session

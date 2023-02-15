import os
from uuid import UUID
from functools import cache
from typing import AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


DB_URL = os.environ["DATABASE_URL"]
db_url = DB_URL.replace("postgres://", "postgresql://")


class Base(DeclarativeBase):
    pass


@cache
def get_engine() -> Engine:
    return create_engine(db_url)


async def get_db() -> AsyncIterator[Session]:
    engine = get_engine()
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine,
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_session_factory() -> AsyncIterator[sessionmaker[Session]]:
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    yield session_factory


def model_id_exists(
    Model: type[Base],
    id: str | UUID,
    session: Session,
) -> bool:
    """
    Check whether an ID exists for a particular model in the DB.
    """
    first_instance = session.query(Model.id).filter_by(id=id).first()  # type: ignore
    if first_instance is None:
        return False
    else:
        return True

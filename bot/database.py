from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    CursorResult,
    DateTime,
    Float,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Table,
    UniqueConstraint,
    Update,
    func,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine

from pydantic import PostgresDsn

import config


#DATABASE_URL = str(PostgresDsn)
#todo: add config and move all constants there

#todo: choose suitable engine
engine = create_async_engine(config.DB_URI, echo=True)

metadata = MetaData()

questions = Table(
    "questions",
    metadata,
    Column("question_id", Integer, Identity(), primary_key=True),
    Column("user_id", Integer, ForeignKey("users_tg.id", ondelete="CASCADE"), nullable=False),
    Column("question", String, nullable=False),
    Column("addition_time", DateTime, server_default=func.now(), nullable=False)
)


users_tg = Table(
    "users_tg",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("username", String, nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String),
    Column("is_premium", Boolean),
    Column("language_code", String),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

user_settings = Table(
    "user_settings",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("language", String, nullable=False),
    Column("mode", String, nullable=False),
)

async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        res = cursor.first()
        return res._asdict() if res is not None else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Insert | Update) -> CursorResult:
    async with engine.begin() as conn:
        res = await conn.execute(query)
        await conn.commit()
        return res

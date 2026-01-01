from typing import Annotated
from functools import lru_cache
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.core.settings import AppConfig, get_config


@lru_cache(maxsize=1)
def get_db_connection(config: Annotated[AppConfig, Depends(get_config)]) -> AsyncEngine:
    return create_async_engine(
        config.POSTGRES_DSN.unicode_string(),
        pool_size=config.POSTGRES_MAX_CONNECTIONS,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True,
        connect_args={
            "server_settings": {"application_name": f"{config.APP_NAME.lower()}[{config.ENVIRONMENT.lower()}]"}
        },
    )


@lru_cache(maxsize=1)
def get_session_factory(engine: Annotated[AsyncEngine, Depends(get_db_connection)]) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session(
    async_session_factory: Annotated[AsyncEngine, Depends(get_session_factory)],
) -> AsyncGenerator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session

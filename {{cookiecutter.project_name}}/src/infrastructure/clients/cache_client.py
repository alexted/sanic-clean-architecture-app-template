from typing import Annotated
from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.infrastructure.core.settings import get_config, AppConfig


@lru_cache(maxsize=1)
def get_cache_client(config: Annotated[AppConfig, Depends(get_config)]) -> Redis:
    """Provides Redis client"""
    return Redis(
        host=config.CACHE_DSN.host, port=config.CACHE_DSN.port, decode_responses=True, client_name=config.APP_NAME
    )

from fastapi import FastAPI, Request

from psycopg_pool import AsyncConnectionPool
from redis.asyncio import Redis
from typing import cast


async def get_db_connection(request: Request):
    db_pool = cast(AsyncConnectionPool, request.app.state.db_pool)
    async with db_pool.connection() as conn:
        yield conn


async def get_redis_client(request: Request):
    redis_client = cast(Redis, request.app.state.redis_client)
    yield redis_client

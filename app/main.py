from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
import redis.asyncio as redis
from app.core.settings import settings
from app.routers.api import api_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_pool = AsyncConnectionPool(conninfo=settings.db_url)
    app.state.db_pool = db_pool
    await db_pool.open()
    redis_client = redis.ConnectionPool.from_url(settings.redis_url)
    redis_client = redis.Redis(connection_pool=redis_client)
    app.state.redis_client = redis_client
    yield
    await app.state.db_pool.close()
    await app.state.redis_client.close()


app = FastAPI(
    title=settings.app_name,
    version="2.1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    lifespan=lifespan)


@app.get("/")
async def welcome(request: Request):
    docs_url = f"{request.base_url}{app.docs_url[1:]}"
    print(docs_url)
    message = {
        "message": "Welcome to Python Togo official api",
        "version": "2.1.0",
        "author": "Python Software Community Togo",
        "documentations": docs_url
    }
    return message


app.include_router(api_routers)

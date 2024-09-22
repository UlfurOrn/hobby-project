from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from shared.database.database import close_database, init_database

from pokemon_api.config import ServiceConfig
from pokemon_api.routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    config = ServiceConfig()

    init_database(config.database)

    yield

    await close_database()


app = FastAPI(
    title="Pokemon API",
    version="0.0.0",
    host="127.0.0.1",
    port=8000,
    lifespan=lifespan,
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app)

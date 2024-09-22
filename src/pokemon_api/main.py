from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from shared.database.database import close_database, init_database

from pokemon_api.config import ServiceConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    config = ServiceConfig()

    init_database(config.database)

    yield

    await close_database()


app = FastAPI(host="127.0.0.1", port=8000, title="Pokemon API", version="0.0.0", lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app)

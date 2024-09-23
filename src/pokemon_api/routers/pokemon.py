from typing import Annotated, Iterable

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from shared.database.database import get_db_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pokemon_api.models.pokemon import PokemonDB

router = APIRouter()


async def managed_db_session():
    async with get_db_session() as db_session:
        yield db_session


class Pokemon(BaseModel):
    name: str

    health: int
    attack: int
    defence: int
    special_attack: int
    special_defence: int
    speed: int

    total: int


@router.get("", response_model=list[Pokemon])
async def get_pokemon(db_session: Annotated[AsyncSession, Depends(managed_db_session)]) -> Iterable[PokemonDB]:
    query = select(PokemonDB)
    result = await db_session.scalars(query)

    return result.all()

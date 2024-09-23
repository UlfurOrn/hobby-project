from typing import Iterable

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from pokemon_api.dependencies import DBSessionDep
from pokemon_api.models.pokemon import PokemonDB

router = APIRouter()


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
async def get_pokemon(db_session: DBSessionDep) -> Iterable[PokemonDB]:
    query = select(PokemonDB)
    result = await db_session.scalars(query)

    return result.all()

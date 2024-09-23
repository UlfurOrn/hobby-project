from typing import Iterable

from fastapi import APIRouter
from sqlalchemy import select

from pokemon_api.dependencies import DBSessionDep
from pokemon_api.models.pokemon import Pokemon, PokemonDB

router = APIRouter()


@router.get("", response_model=list[Pokemon])
async def get_pokemon(db_session: DBSessionDep) -> Iterable[PokemonDB]:
    query = select(PokemonDB)
    result = await db_session.scalars(query)

    return result.all()

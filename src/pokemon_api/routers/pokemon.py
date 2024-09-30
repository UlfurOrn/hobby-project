from typing import Annotated, Iterable

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from starlette.status import HTTP_400_BAD_REQUEST

from pokemon_api.dependencies import DBSessionDep
from pokemon_api.models.pokemon import Pokemon, PokemonDB

router = APIRouter()


@router.get("", response_model=list[Pokemon])
async def get_pokemon(
    db_session: DBSessionDep,
    name_prefix: Annotated[str, Query(description="The name prefix to filter the Pokémon by.")] = None,
    total_min: Annotated[int, Query(description="The minimum total stats to filter the Pokémon by.", ge=0)] = 0,
    total_max: Annotated[int, Query(description="The minimum total stats to filter the Pokémon by.", ge=0)] = 1000000,
) -> Iterable[PokemonDB]:
    if total_max < total_min:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="total_max must be larger than total_min")

    query = select(PokemonDB)

    if name_prefix is not None:
        name_prefix_filter = f"{name_prefix.lower()}%"
        query = query.where(PokemonDB.name.like(name_prefix_filter))

    query = query.where(PokemonDB.total.between(total_min, total_max))

    result = await db_session.scalars(query)

    return result.all()

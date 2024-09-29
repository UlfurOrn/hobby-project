import asyncio
import json
from typing import Any, Iterable

from dotenv import load_dotenv
from pokemon_api.config import DatabaseConfig as PokemonDatabaseConfig
from pokemon_api.models.pokemon import Pokemon, PokemonDB
from shared.database.database import get_db_session, init_database


def load_pokemon_from_file(filename: str = "webscrapers/output/pokemon.json") -> Iterable[dict[str, Any]]:
    with open(filename, mode="r") as file_object:
        pokemon = json.load(file_object)

    # Currently the setup does not support Pokémon variations, so we remove variations here.
    pokemon = filter(lambda p: not p["is_variation"], pokemon)

    return pokemon


async def main():
    load_dotenv()

    config = PokemonDatabaseConfig()
    init_database(config)

    async with get_db_session() as db_session:
        pokemon = []
        for pokemon_data in load_pokemon_from_file():
            # SQLAlchemy does not allow additional fields, so we first convert to a Pydantic model containing the
            # required fields of the SQLAlchemy model. TODO: Replace with SQLModel?
            pokemon_data = Pokemon(**pokemon_data).model_dump()
            pokemon.append(PokemonDB(**pokemon_data))

        db_session.add_all(pokemon)
        await db_session.commit()


if __name__ == "__main__":
    asyncio.run(main())

import pytest
from dirty_equals import IsDict, IsInt, IsList
from pokemon_api.models.pokemon import PokemonDB


@pytest.fixture(autouse=True)
async def pokemon(db_session):
    db_session.add_all(
        [
            PokemonDB(
                name="bulbasaur",
                types=["Grass", "Poison"],
                total=318,
                health=45,
                attack=49,
                defence=49,
                special_attack=65,
                special_defence=65,
                speed=45,
            ),
            PokemonDB(
                name="ivysaur",
                types=["Grass", "Poison"],
                total=405,
                health=60,
                attack=62,
                defence=63,
                special_attack=80,
                special_defence=80,
                speed=60,
            ),
            PokemonDB(
                name="venusaur",
                types=["Grass", "Poison"],
                total=525,
                health=80,
                attack=82,
                defence=83,
                special_attack=100,
                special_defence=100,
                speed=80,
            ),
        ]
    )

    await db_session.commit()


def IsPokemon(name: str) -> IsDict:
    return IsDict(
        name=name,
        types=IsList,
        total=IsInt,
        health=IsInt,
        attack=IsInt,
        defence=IsInt,
        special_attack=IsInt,
        special_defence=IsInt,
        speed=IsInt,
    )


async def test_get_pokemon(api_client):
    response = await api_client.get("/pokemon")

    assert response.status_code == 200
    assert response.json() == [
        IsPokemon(name="bulbasaur"),
        IsPokemon(name="ivysaur"),
        IsPokemon(name="venusaur"),
    ]

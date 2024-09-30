import pytest
from dirty_equals import IsDict, IsInstance, IsInt
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
        types=IsInstance(list),
        total=IsInt(),
        health=IsInt(),
        attack=IsInt(),
        defence=IsInt(),
        special_attack=IsInt(),
        special_defence=IsInt(),
        speed=IsInt(),
    )


async def test_get_pokemon(api_client):
    response = await api_client.get("/pokemon")

    assert response.status_code == 200
    assert response.json() == [
        IsPokemon(name="bulbasaur"),
        IsPokemon(name="ivysaur"),
        IsPokemon(name="venusaur"),
    ]


async def test_get_pokemon__filtered_by_name_prefix(api_client):
    response = await api_client.get("/pokemon", params={"name_prefix": "bulb"})

    assert response.status_code == 200
    assert response.json() == [
        IsPokemon(name="bulbasaur"),
        # IsPokemon(name="ivysaur"),  name prefix != bulb
        # IsPokemon(name="venusaur"),  name prefix != bulb
    ]


async def test_get_pokemon__filtered_by_stats__total_min(api_client):
    response = await api_client.get("/pokemon", params={"total_min": 400})

    assert response.status_code == 200
    assert response.json() == [
        # IsPokemon(name="bulbasaur"),  total < 400
        IsPokemon(name="ivysaur"),
        IsPokemon(name="venusaur"),
    ]


async def test_get_pokemon__filtered_by_stats__total_max(api_client):
    response = await api_client.get("/pokemon", params={"total_max": 500})

    assert response.status_code == 200
    assert response.json() == [
        IsPokemon(name="bulbasaur"),
        IsPokemon(name="ivysaur"),
        # IsPokemon(name="venusaur"),  total > 500
    ]


async def test_get_pokemon__filtered_by_stats__total_min_and_max(api_client):
    response = await api_client.get("/pokemon", params={"total_min": 400, "total_max": 500})

    assert response.status_code == 200
    assert response.json() == [
        # IsPokemon(name="bulbasaur"),  total < 400
        IsPokemon(name="ivysaur"),
        # IsPokemon(name="venusaur"),  total > 500
    ]


async def test_get_pokemon__filtered_by_stats__max_smaller_than_min(api_client):
    response = await api_client.get("/pokemon", params={"total_min": 500, "total_max": 400})

    assert response.status_code == 400
    assert response.json() == {}


async def test_get_pokemon__filtered_by_name_and_stats(api_client):
    response = await api_client.get("/pokemon", params={"name_prefix": "ivy", "total_min": 400, "total_max": 999})

    assert response.status_code == 200
    assert response.json() == [
        # IsPokemon(name="bulbasaur"),  total < 400
        IsPokemon(name="ivysaur"),
        # IsPokemon(name="venusaur"),  name prefix != ivy
    ]

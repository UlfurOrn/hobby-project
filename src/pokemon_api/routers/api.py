from fastapi import APIRouter

from pokemon_api.routers import pokemon

api_router = APIRouter()
api_router.include_router(pokemon.router, prefix="/pokemon", tags=["pokemon"])

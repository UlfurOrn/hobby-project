from pydantic import BaseModel
from sqlalchemy import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDB(DeclarativeBase):
    pass


class PokemonDB(BaseDB):
    __tablename__ = "pokemon"

    name: Mapped[str] = mapped_column(primary_key=True)

    health: Mapped[int]
    attack: Mapped[int]
    defence: Mapped[int]
    special_attack: Mapped[int]
    special_defence: Mapped[int]
    speed: Mapped[int]

    # TODO: Try out replacing this field with a "hybrid property" calculated from the above values
    total: Mapped[int]

    types: Mapped[list[str]] = mapped_column(ARRAY(String))


class Pokemon(BaseModel):
    name: str

    health: int
    attack: int
    defence: int
    special_attack: int
    special_defence: int
    speed: int

    total: int

"""Create Pokémon table

Revision ID: a74367808480
Revises:
Create Date: 2024-09-23 15:42:39.529852
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pokemon_api.models.pokemon import PokemonDB
from sqlalchemy import select

# revision identifiers, used by Alembic.
revision: str = "a74367808480"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemon",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("health", sa.Integer(), nullable=False),
        sa.Column("attack", sa.Integer(), nullable=False),
        sa.Column("defence", sa.Integer(), nullable=False),
        sa.Column("special_attack", sa.Integer(), nullable=False),
        sa.Column("special_defence", sa.Integer(), nullable=False),
        sa.Column("speed", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("pokemon")

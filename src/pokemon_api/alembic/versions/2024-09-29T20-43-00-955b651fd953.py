"""Add types field to Pokémon table

Revision ID: 955b651fd953
Revises: a74367808480
Create Date: 2024-09-29 20:43:00.696790
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "955b651fd953"
down_revision: Union[str, None] = "a74367808480"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("pokemon", sa.Column("types", sa.ARRAY(sa.String()), nullable=False))


def downgrade() -> None:
    op.drop_column("pokemon", "types")

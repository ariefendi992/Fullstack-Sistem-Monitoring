"""empty message

Revision ID: 4ae81292c335
Revises: 15d2ce89fae0
Create Date: 2023-12-18 23:18:48.781596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ae81292c335'
down_revision: Union[str, None] = '15d2ce89fae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

"""add table kelas

Revision ID: 7987d08596c6
Revises: 4ae81292c335
Create Date: 2023-12-18 23:18:55.517525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7987d08596c6'
down_revision: Union[str, None] = '4ae81292c335'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_datum_kelas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kelas', sa.String(16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_datum_kelas')
    # ### end Alembic commands ###

"""Create table ContasPagarReceber

Revision ID: d5a722ce3caa
Revises: 
Create Date: 2024-08-03 18:28:34.912508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a722ce3caa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contas_pagar_receber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=30), nullable=True),
    sa.Column('value', sa.Numeric(), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contas_pagar_receber')
    # ### end Alembic commands ###
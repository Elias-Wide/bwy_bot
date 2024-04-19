"""fix: change_schedule_fields_and_others.py

Revision ID: 80fd02331d15
Revises: 2396728d9816
Create Date: 2024-04-19 10:18:18.600070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80fd02331d15'
down_revision: Union[str, None] = '2396728d9816'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descriptin', sa.Text(), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.TEXT(), nullable=True))
        batch_op.drop_column('descriptin')

    # ### end Alembic commands ###

"""Add-table-shedule-course

Revision ID: 26dc74399ef2
Revises: 15c3f2abf6a7
Create Date: 2024-04-09 23:21:51.010584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types.choice import ChoiceType

from app.core.constants import ACTIVITY_PURPOSE, AM_NOON_PM, GENDER


# revision identifiers, used by Alembic.
revision: str = '26dc74399ef2'
down_revision: Union[str, None] = '15c3f2abf6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('gender', ChoiceType(GENDER), nullable=True),
    sa.Column('activity', ChoiceType(ACTIVITY_PURPOSE), nullable=True),
    sa.Column('corse_day', sa.Integer(), nullable=True),
    sa.Column('am_noon_pm', ChoiceType(AM_NOON_PM), nullable=True),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shedule',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('start_course', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shedule')
    op.drop_table('course')
    # ### end Alembic commands ###

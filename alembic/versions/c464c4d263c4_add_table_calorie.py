"""Add table calorie.

Revision ID: c464c4d263c4
Revises: 5771c00fce6d
Create Date: 2024-04-15 16:56:05.984999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy_utils.types.choice import ChoiceType
from app.core.constants import PHYSICAL_ACTIVITY, GENDER
from app.core.config import STATIC_DIR


# revision identifiers, used by Alembic.
revision: str = 'c464c4d263c4'
down_revision: Union[str, None] = '5771c00fce6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calorie',
    sa.Column('gender', ChoiceType(GENDER), nullable=True),
    sa.Column('activity', ChoiceType(PHYSICAL_ACTIVITY), nullable=True),
    sa.Column('picture', FileType(storage = FileSystemStorage(path=STATIC_DIR)), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calorie')
    # ### end Alembic commands ###
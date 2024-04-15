"""First

Revision ID: d12726d58fe6
Revises: 
Create Date: 2024-04-14 02:31:13.621381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy_utils.types.choice import ChoiceType
from app.core.constants import ACTIVITY_PURPOSE, WORKOUT_TYPE, GENDER, AM_NOON_PM
from app.core.config import UPLOAD_DIR


# revision identifiers, used by Alembic.
revision: str = 'd12726d58fe6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('descriptin', sa.Text(), nullable=False),
    sa.Column('video', FileType(storage = FileSystemStorage(path=UPLOAD_DIR)), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('possibleanswer',
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('telegram_id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('gender', ChoiceType(GENDER), nullable=True),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('activity', ChoiceType(ACTIVITY_PURPOSE), nullable=True),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('telegram_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    op.create_table('workout',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('descriptin', sa.Text(), nullable=False),
    sa.Column('workout_type', ChoiceType(WORKOUT_TYPE), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('course',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('descriptin', sa.Text(), nullable=False),
    sa.Column('gender', ChoiceType(GENDER), nullable=True),
    sa.Column('activity', ChoiceType(ACTIVITY_PURPOSE), nullable=True),
    sa.Column('corse_day', sa.Integer(), nullable=True),
    sa.Column('am_noon_pm', ChoiceType(AM_NOON_PM), nullable=True),
    sa.Column('workout_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], name='workout_id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('exercise_workout',
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('workout_id', sa.Integer(), nullable=True),
    sa.Column('extra_data', sa.String(length=100), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], name='exercise_id'),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('possibleanswer_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['possibleanswer_id'], ['possibleanswer.id'], name='possibleanswer_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shedule',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('start_course', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sleep',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('go_to_bed_time', sa.DateTime(), nullable=True),
    sa.Column('wake_up_time', sa.DateTime(), nullable=True),
    sa.Column('sleep_duration', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sleep')
    op.drop_table('shedule')
    op.drop_table('question')
    op.drop_table('exercise_workout')
    op.drop_table('course')
    op.drop_table('workout')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('possibleanswer')
    op.drop_table('exercise')
    # ### end Alembic commands ###

"""empty message

Revision ID: e4d6aee3a5f7
Revises: ab5732f4832a
Create Date: 2025-07-24 21:07:09.688042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4d6aee3a5f7'
down_revision: Union[str, Sequence[str], None] = 'ab5732f4832a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listening_third_task_options', sa.Column('question_id', sa.Integer(), nullable=False))
    op.drop_constraint(op.f('listening_third_task_options_task_id_fkey'), 'listening_third_task_options', type_='foreignkey')
    op.create_foreign_key(None, 'listening_third_task_options', 'listening_third_task_questions', ['question_id'], ['id'])
    op.drop_column('listening_third_task_options', 'task_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listening_third_task_options', sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'listening_third_task_options', type_='foreignkey')
    op.create_foreign_key(op.f('listening_third_task_options_task_id_fkey'), 'listening_third_task_options', 'listening_third_tasks', ['task_id'], ['id'])
    op.drop_column('listening_third_task_options', 'question_id')
    # ### end Alembic commands ###

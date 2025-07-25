"""empty message

Revision ID: 10cd37ec3401
Revises: 0d3edecda42a
Create Date: 2025-07-25 17:37:12.905182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10cd37ec3401'
down_revision: Union[str, Sequence[str], None] = '0d3edecda42a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('reading_first_task_options_task_id_fkey'), 'reading_first_task_options', type_='foreignkey')
    op.create_foreign_key(None, 'reading_first_task_options', 'reading_first_tasks', ['task_id'], ['id'])
    op.drop_constraint(op.f('reading_first_task_questions_task_id_fkey'), 'reading_first_task_questions', type_='foreignkey')
    op.create_foreign_key(None, 'reading_first_task_questions', 'reading_first_tasks', ['task_id'], ['id'])
    op.drop_constraint(op.f('reading_second_task_options_task_id_fkey'), 'reading_second_task_options', type_='foreignkey')
    op.create_foreign_key(None, 'reading_second_task_options', 'reading_second_tasks', ['task_id'], ['id'])
    op.drop_constraint(op.f('reading_second_task_questions_task_id_fkey'), 'reading_second_task_questions', type_='foreignkey')
    op.create_foreign_key(None, 'reading_second_task_questions', 'reading_second_tasks', ['task_id'], ['id'])
    op.drop_constraint(op.f('reading_third_task_options_task_id_fkey'), 'reading_third_task_options', type_='foreignkey')
    op.create_foreign_key(None, 'reading_third_task_options', 'reading_third_tasks', ['task_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading_third_task_options', type_='foreignkey')
    op.create_foreign_key(op.f('reading_third_task_options_task_id_fkey'), 'reading_third_task_options', 'listening_third_tasks', ['task_id'], ['id'])
    op.drop_constraint(None, 'reading_second_task_questions', type_='foreignkey')
    op.create_foreign_key(op.f('reading_second_task_questions_task_id_fkey'), 'reading_second_task_questions', 'listening_second_tasks', ['task_id'], ['id'])
    op.drop_constraint(None, 'reading_second_task_options', type_='foreignkey')
    op.create_foreign_key(op.f('reading_second_task_options_task_id_fkey'), 'reading_second_task_options', 'listening_second_tasks', ['task_id'], ['id'])
    op.drop_constraint(None, 'reading_first_task_questions', type_='foreignkey')
    op.create_foreign_key(op.f('reading_first_task_questions_task_id_fkey'), 'reading_first_task_questions', 'listening_first_tasks', ['task_id'], ['id'])
    op.drop_constraint(None, 'reading_first_task_options', type_='foreignkey')
    op.create_foreign_key(op.f('reading_first_task_options_task_id_fkey'), 'reading_first_task_options', 'listening_first_tasks', ['task_id'], ['id'])
    # ### end Alembic commands ###

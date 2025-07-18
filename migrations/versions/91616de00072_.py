"""empty message

Revision ID: 91616de00072
Revises: ba89044b8948
Create Date: 2025-07-11 20:01:12.130921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91616de00072'
down_revision: Union[str, Sequence[str], None] = 'ba89044b8948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reading_tasks_type_three',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reading_tasks_type_two',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('reading_questions', sa.Column('task_type', sa.String(length=50), nullable=False))
    op.drop_constraint(op.f('reading_questions_task_id_fkey'), 'reading_questions', type_='foreignkey')
    op.add_column('sentence_options', sa.Column('task_type', sa.String(length=50), nullable=False))
    op.drop_constraint(op.f('sentence_options_task_id_fkey'), 'sentence_options', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(op.f('sentence_options_task_id_fkey'), 'sentence_options', 'reading_tasks_type_one', ['task_id'], ['id'], ondelete='CASCADE')
    op.drop_column('sentence_options', 'task_type')
    op.create_foreign_key(op.f('reading_questions_task_id_fkey'), 'reading_questions', 'reading_tasks_type_one', ['task_id'], ['id'], ondelete='CASCADE')
    op.drop_column('reading_questions', 'task_type')
    op.drop_table('reading_tasks_type_two')
    op.drop_table('reading_tasks_type_three')
    # ### end Alembic commands ###

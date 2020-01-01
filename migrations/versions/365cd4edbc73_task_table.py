"""task table

Revision ID: 365cd4edbc73
Revises: fecf3292adb8
Create Date: 2019-12-02 23:07:50.243478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '365cd4edbc73'
down_revision = 'fecf3292adb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=128), nullable=True),
    sa.Column('task_due', sa.DateTime(), nullable=True),
    sa.Column('task_remind', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_index(op.f('ix_task_task_due'), 'task', ['task_due'], unique=False)
    op.create_index(op.f('ix_task_task_name'), 'task', ['task_name'], unique=False)
    op.create_index(op.f('ix_task_task_remind'), 'task', ['task_remind'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_remind'), table_name='task')
    op.drop_index(op.f('ix_task_task_name'), table_name='task')
    op.drop_index(op.f('ix_task_task_due'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###

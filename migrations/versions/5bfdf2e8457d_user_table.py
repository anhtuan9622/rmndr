"""user table

Revision ID: 5bfdf2e8457d
Revises: 9a4e904f7c0d
Create Date: 2019-12-04 19:52:55.062556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bfdf2e8457d'
down_revision = '9a4e904f7c0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=320), nullable=False),
    sa.Column('user_password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_user_email'), 'user', ['user_email'], unique=True)
    op.create_table('task',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=128), nullable=False),
    sa.Column('task_due', sa.Text(), nullable=True),
    sa.Column('task_remind', sa.Text(), nullable=True),
    sa.Column('task_sent', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_index(op.f('ix_task_task_due'), 'task', ['task_due'], unique=False)
    op.create_index(op.f('ix_task_task_name'), 'task', ['task_name'], unique=False)
    op.create_index(op.f('ix_task_task_remind'), 'task', ['task_remind'], unique=False)
    op.create_index(op.f('ix_task_task_sent'), 'task', ['task_sent'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_sent'), table_name='task')
    op.drop_index(op.f('ix_task_task_remind'), table_name='task')
    op.drop_index(op.f('ix_task_task_name'), table_name='task')
    op.drop_index(op.f('ix_task_task_due'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###

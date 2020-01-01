"""empty message

Revision ID: 4510763a066f
Revises: 9e6af549955b
Create Date: 2019-12-07 00:11:09.902190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4510763a066f'
down_revision = '9e6af549955b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'task_due',
               existing_type=sa.TEXT(),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('task', 'task_remind',
               existing_type=sa.TEXT(),
               type_=sa.DateTime(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'task_remind',
               existing_type=sa.DateTime(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('task', 'task_due',
               existing_type=sa.DateTime(),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###

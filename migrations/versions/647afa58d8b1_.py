"""empty message

Revision ID: 647afa58d8b1
Revises: 868937545b87
Create Date: 2019-12-17 19:30:34.576104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647afa58d8b1'
down_revision = '868937545b87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'task_due',
               existing_type=sa.DATETIME(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('task', 'task_remind',
               existing_type=sa.DATETIME(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'task_remind',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATETIME(),
               existing_nullable=True)
    op.alter_column('task', 'task_due',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATETIME(),
               existing_nullable=True)
    # ### end Alembic commands ###

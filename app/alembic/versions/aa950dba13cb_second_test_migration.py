"""second test migration

Revision ID: aa950dba13cb
Revises: bd376251ad2f
Create Date: 2022-04-28 00:55:53.185722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa950dba13cb'
down_revision = 'bd376251ad2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eldorado_test', sa.Column('newtestfield', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('eldorado_test', 'newtestfield')
    # ### end Alembic commands ###
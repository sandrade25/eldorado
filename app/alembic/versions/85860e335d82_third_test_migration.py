"""third test migration

Revision ID: 85860e335d82
Revises: aa950dba13cb
Create Date: 2022-04-28 21:18:37.922417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85860e335d82'
down_revision = 'aa950dba13cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eldorado_test', sa.Column('third_testfield', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('eldorado_test', 'third_testfield')
    # ### end Alembic commands ###
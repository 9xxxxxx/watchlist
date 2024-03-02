"""Initial migration.

Revision ID: 886d0ec648d5
Revises: a30f03c065a8
Create Date: 2024-03-02 22:47:45.755908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '886d0ec648d5'
down_revision = 'a30f03c065a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('theme')
    # ### end Alembic commands ###

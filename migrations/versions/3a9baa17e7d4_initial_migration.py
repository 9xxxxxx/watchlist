"""Initial migration.

Revision ID: 3a9baa17e7d4
Revises: 
Create Date: 2024-03-01 14:21:32.551818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a9baa17e7d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('impression')
    op.drop_table('music')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('music',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=60), nullable=True),
    sa.Column('data', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('impression',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('movie_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('rating', sa.FLOAT(), nullable=True),
    sa.Column('review', sa.VARCHAR(length=1500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
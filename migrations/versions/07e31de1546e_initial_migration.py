"""Initial migration.

Revision ID: 07e31de1546e
Revises: 3a9baa17e7d4
Create Date: 2024-03-01 14:38:53.068670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07e31de1546e'
down_revision = '3a9baa17e7d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=40), nullable=True))
        batch_op.add_column(sa.Column('name', sa.String(length=40), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=40),
               existing_nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=40),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('username')

    # ### end Alembic commands ###

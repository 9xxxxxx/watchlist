"""Initial migration.

Revision ID: 28640fd63e94
Revises: 886d0ec648d5
Create Date: 2024-03-02 22:48:35.427861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28640fd63e94'
down_revision = '886d0ec648d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theme', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alt', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theme', schema=None) as batch_op:
        batch_op.drop_column('alt')

    # ### end Alembic commands ###

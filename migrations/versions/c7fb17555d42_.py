"""empty message

Revision ID: c7fb17555d42
Revises: 2209ea9dd941
Create Date: 2019-08-19 21:03:49.906284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7fb17555d42'
down_revision = '2209ea9dd941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record_daytime', sa.Column('time_date', sa.Date(), nullable=True))
    op.drop_column('record_daytime', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record_daytime', sa.Column('date', sa.DATE(), nullable=True))
    op.drop_column('record_daytime', 'time_date')
    # ### end Alembic commands ###

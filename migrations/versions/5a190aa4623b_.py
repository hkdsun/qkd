"""empty message

Revision ID: 5a190aa4623b
Revises: 1da08775b81
Create Date: 2015-11-08 18:18:03.534375

"""

# revision identifiers, used by Alembic.
revision = '5a190aa4623b'
down_revision = '1da08775b81'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('date', sa.DateTime(), nullable=True))
    op.drop_column('entries', 'url')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('entries', 'date')
    ### end Alembic commands ###

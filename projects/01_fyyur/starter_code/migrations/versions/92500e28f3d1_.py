"""empty message

Revision ID: 92500e28f3d1
Revises: 96d6198e49f1
Create Date: 2021-06-23 08:50:44.790152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92500e28f3d1'
down_revision = '96d6198e49f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('Venue', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.execute('UPDATE "Venue" SET created_date = \'2021-06-23\' WHERE created_date IS NULL')
    op.execute('UPDATE "Artist" SET created_date = \'2021-06-23\' WHERE created_date IS NULL')
    op.alter_column('Venue', 'created_date', nullable= False)
    op.alter_column('Artist', 'created_date', nullable= False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'created_date')
    op.drop_column('Artist', 'created_date')
    # ### end Alembic commands ###
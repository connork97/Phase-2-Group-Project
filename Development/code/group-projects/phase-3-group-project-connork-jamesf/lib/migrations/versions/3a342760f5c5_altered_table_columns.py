"""altered table columns

Revision ID: 3a342760f5c5
Revises: ddc30608f593
Create Date: 2023-04-20 12:20:06.569250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a342760f5c5'
down_revision = 'ddc30608f593'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('times')
    op.add_column('activities', sa.Column('productivity', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'activities', type_='foreignkey')
    op.drop_constraint(None, 'activities', type_='foreignkey')
    # op.drop_column('activities', 'friend_id')
    # op.drop_column('activities', 'time_id')
    op.add_column('days', sa.Column('productivity', sa.Integer(), nullable=True))
    op.drop_column('days', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('days', sa.Column('name', sa.VARCHAR(), nullable=True))
    op.drop_column('days', 'productivity')
    op.add_column('activities', sa.Column('time_id', sa.INTEGER(), nullable=True))
    op.add_column('activities', sa.Column('friend_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'activities', 'times', ['time_id'], ['id'])
    op.create_foreign_key(None, 'activities', 'friends', ['friend_id'], ['id'])
    op.drop_column('activities', 'productivity')
    op.create_table('times',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('time', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

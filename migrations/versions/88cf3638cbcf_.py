"""empty message

Revision ID: 88cf3638cbcf
Revises: 5df260372421
Create Date: 2024-10-22 05:20:33.116913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88cf3638cbcf'
down_revision = '5df260372421'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=162), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
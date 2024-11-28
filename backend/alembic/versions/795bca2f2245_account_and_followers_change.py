"""account_and_followers_change

Revision ID: 795bca2f2245
Revises: 6b8055e88ddb
Create Date: 2024-11-23 13:27:35.073757

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '795bca2f2245'
down_revision = '6b8055e88ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('num_followers', sa.Integer(), nullable=True))
    op.add_column('account', sa.Column('num_following', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'num_following')
    op.drop_column('account', 'num_followers')
    # ### end Alembic commands ###
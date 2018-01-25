"""add plist columns

Revision ID: cc7d6ba72692
Revises: 8306a6c493d2
Create Date: 2018-01-23 16:29:42.664760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc7d6ba72692'
down_revision = '8306a6c493d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('plist_name', sa.String(length=64), nullable=True))
    op.add_column('project', sa.Column('plist_url', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'plist_url')
    op.drop_column('project', 'plist_name')
    # ### end Alembic commands ###

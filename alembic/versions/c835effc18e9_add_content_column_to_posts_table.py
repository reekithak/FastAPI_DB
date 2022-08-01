"""add content column to posts table

Revision ID: c835effc18e9
Revises: 0d79980473ac
Create Date: 2022-08-02 01:40:31.421406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c835effc18e9'
down_revision = '0d79980473ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass

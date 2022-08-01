"""create posts table

Revision ID: 0d79980473ac
Revises: 
Create Date: 2022-08-02 01:20:46.513157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d79980473ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", type_=sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", type_=sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

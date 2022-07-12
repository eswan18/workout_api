"""Alter table sets add column start_time

Revision ID: 9cc569439b81
Revises: 5adb9c80352c
Create Date: 2022-07-12 18:31:46.327459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9cc569439b81"
down_revision = "5adb9c80352c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sets", sa.Column("start_time", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sets", "start_time")
    # ### end Alembic commands ###

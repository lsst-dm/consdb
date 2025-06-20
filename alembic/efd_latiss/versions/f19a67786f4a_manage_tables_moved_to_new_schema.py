"""Manage tables moved to new schema

Revision ID: f19a67786f4a
Revises: 092de58eaa4e
Create Date: 2025-05-01 22:14:46.613788+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f19a67786f4a"
down_revision: Union[str, None] = "092de58eaa4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transformed_efd_scheduler", schema="efd_latiss")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transformed_efd_scheduler",
        sa.Column(
            "id", sa.INTEGER(), autoincrement=True, nullable=False, comment="Unique ID, auto-incremented"
        ),
        sa.Column(
            "start_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
            comment="Start time of transformation interval, must be provided",
        ),
        sa.Column(
            "end_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
            comment="End time of transformation interval, must be provided",
        ),
        sa.Column(
            "timewindow",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
            comment="Time window to expand start/end times by (minutes)",
        ),
        sa.Column(
            "status",
            sa.CHAR(length=20),
            server_default=sa.text("'pending'::bpchar"),
            autoincrement=False,
            nullable=True,
            comment="Process status, default 'pending'",
        ),
        sa.Column(
            "process_start_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
            comment="Timestamp when process started",
        ),
        sa.Column(
            "process_end_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
            comment="Timestamp when process ended",
        ),
        sa.Column(
            "process_exec_time",
            sa.INTEGER(),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=True,
            comment="Execution time in seconds, default 0",
        ),
        sa.Column(
            "exposures",
            sa.INTEGER(),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=True,
            comment="Number of exposures processed, default 0",
        ),
        sa.Column(
            "visits1",
            sa.INTEGER(),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=True,
            comment="Number of visits recorded, default 0",
        ),
        sa.Column(
            "retries",
            sa.INTEGER(),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=True,
            comment="Number of retries attempted, default 0",
        ),
        sa.Column("error", sa.TEXT(), autoincrement=False, nullable=True, comment="Error message, if any"),
        sa.Column("butler_repo", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=True,
            comment="Timestamp when record was created, default current timestamp",
        ),
        sa.PrimaryKeyConstraint("id", name="transformed_efd_scheduler_pkey"),
        schema="efd_latiss",
        comment="Transformed EFD scheduler.",
    )
    # ### end Alembic commands ###

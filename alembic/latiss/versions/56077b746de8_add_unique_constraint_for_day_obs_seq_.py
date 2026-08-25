"""add unique constraint for day obs seq num key

Revision ID: 56077b746de8
Revises: 53707815663e
Create Date: 2024-09-16 17:31:22.643951+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56077b746de8"
down_revision: str | None = "53707815663e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "un_exposure_flexdata_day_obs_seq_num_key",
        "exposure_flexdata",
        ["day_obs", "seq_num", "key"],
        schema="cdb_latiss",
    )


def downgrade() -> None:
    op.drop_constraint(
        "un_exposure_flexdata_day_obs_seq_num_key", "exposure_flexdata", schema="cdb_latiss", type_="unique"
    )

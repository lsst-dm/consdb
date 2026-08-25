"""add unique constraint for day obs seq num key

Revision ID: 02f64409522c
Revises: 5f50b32c44fc
Create Date: 2024-09-16 17:31:25.545455+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02f64409522c"
down_revision: str | None = "5f50b32c44fc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "un_exposure_flexdata_day_obs_seq_num_key",
        "exposure_flexdata",
        ["day_obs", "seq_num", "key"],
        schema="cdb_lsstcomcamsim",
    )


def downgrade() -> None:
    op.drop_constraint(
        "un_exposure_flexdata_day_obs_seq_num_key",
        "exposure_flexdata",
        schema="cdb_lsstcomcamsim",
        type_="unique",
    )

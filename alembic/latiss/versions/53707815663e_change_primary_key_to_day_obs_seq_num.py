"""change primary key to day_obs + seq_num

Revision ID: 53707815663e
Revises: 59776480aa4d
Create Date: 2024-09-11 00:15:14.413772+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "53707815663e"
down_revision: Union[str, None] = "59776480aa4d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_exposure_id", "ccdexposure", schema="cdb_latiss", type_="foreignkey")
    op.drop_constraint("fk_obs_id", "exposure_flexdata", schema="cdb_latiss", type_="foreignkey")
    op.drop_constraint("un_exposure_id_detector", "ccdexposure", schema="cdb_latiss", type_="unique")
    op.drop_constraint("un_day_obs_seq_num", "exposure", schema="cdb_latiss", type_="unique")
    op.add_column(
        "ccdexposure",
        sa.Column(
            "day_obs",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Day of observation.",
        ),
        schema="cdb_latiss",
    )
    op.add_column(
        "ccdexposure",
        sa.Column(
            "seq_num",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Sequence number.",
        ),
        schema="cdb_latiss",
    )
    op.create_unique_constraint(
        "un_ccdexposure_ccdexposure_id", "ccdexposure", ["ccdexposure_id"], schema="cdb_latiss"
    )
    op.create_unique_constraint(
        "un_ccdexposure_day_obs_seq_num_detector",
        "ccdexposure",
        ["day_obs", "seq_num", "detector"],
        schema="cdb_latiss",
    )
    op.create_unique_constraint(
        "un_exposure_day_obs_seq_num", "exposure", ["day_obs", "seq_num"], schema="cdb_latiss"
    )
    op.create_unique_constraint("un_exposure_exposure_id", "exposure", ["exposure_id"], schema="cdb_latiss")
    op.add_column(
        "exposure_flexdata",
        sa.Column(
            "day_obs",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Day of observation.",
        ),
        schema="cdb_latiss",
    )
    op.add_column(
        "exposure_flexdata",
        sa.Column(
            "seq_num",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Sequence number.",
        ),
        schema="cdb_latiss",
    )
    op.create_foreign_key(
        "fk_exposure_flexdata_day_obs_seq_num",
        "exposure_flexdata",
        "exposure",
        ["day_obs", "seq_num"],
        ["day_obs", "seq_num"],
        source_schema="cdb_latiss",
        referent_schema="cdb_latiss",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "day_obs",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Day of observation.",
        ),
        schema="cdb_latiss",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "seq_num",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Sequence number.",
        ),
        schema="cdb_latiss",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "postisr_pixel_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Median postISR pixel value.",
        ),
        schema="cdb_latiss",
    )
    op.create_foreign_key(
        "fk_visit1_quicklook_day_obs_seq_num",
        "visit1_quicklook",
        "exposure",
        ["day_obs", "seq_num"],
        ["day_obs", "seq_num"],
        source_schema="cdb_latiss",
        referent_schema="cdb_latiss",
    )
    op.create_foreign_key(
        "fk_ccdexposure_day_obs_seq_num",
        "ccdexposure",
        "exposure",
        ["day_obs", "seq_num"],
        ["day_obs", "seq_num"],
        source_schema="cdb_latiss",
        referent_schema="cdb_latiss",
    )
    # ### end Alembic commands ###

    # Added by hand: copy day_obs and seq_num into the ccdexposure,
    # exposure_flexdata, and visit1_quicklook tables
    # Extra commands to copy columns from the exposure table
    # and mark the columns as non-null
    pkey = {
        "ccdexposure": "exposure_id",
        "exposure_flexdata": "obs_id",
        "visit1_quicklook": "visit_id",
    }
    the_schema = "cdb_latiss"
    for destination_table in ("ccdexposure", "exposure_flexdata", "visit1_quicklook"):
        op.execute(
            f"""
                UPDATE {the_schema}.{destination_table}
                    SET day_obs = {the_schema}.exposure.day_obs,
                        seq_num = {the_schema}.exposure.seq_num
                    FROM {the_schema}.exposure
                    WHERE {the_schema}.exposure.exposure_id =
                        {the_schema}.{destination_table}.{pkey[destination_table]}
            """
        )
        op.alter_column(destination_table, "day_obs", nullable=False, schema=the_schema)
        op.alter_column(destination_table, "seq_num", nullable=False, schema=the_schema)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_visit1_quicklook_day_obs_seq_num", "visit1_quicklook", schema="cdb_latiss", type_="foreignkey"
    )
    op.drop_column("visit1_quicklook", "postisr_pixel_median", schema="cdb_latiss")
    op.drop_column("visit1_quicklook", "seq_num", schema="cdb_latiss")
    op.drop_column("visit1_quicklook", "day_obs", schema="cdb_latiss")
    op.drop_constraint(
        "fk_exposure_flexdata_day_obs_seq_num", "exposure_flexdata", schema="cdb_latiss", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_obs_id",
        "exposure_flexdata",
        "exposure",
        ["obs_id"],
        ["exposure_id"],
        source_schema="cdb_latiss",
        referent_schema="cdb_latiss",
    )
    op.drop_column("exposure_flexdata", "seq_num", schema="cdb_latiss")
    op.drop_column("exposure_flexdata", "day_obs", schema="cdb_latiss")
    op.drop_constraint("un_exposure_exposure_id", "exposure", schema="cdb_latiss", type_="unique")
    op.drop_constraint("un_exposure_day_obs_seq_num", "exposure", schema="cdb_latiss", type_="unique")
    op.create_unique_constraint("un_day_obs_seq_num", "exposure", ["day_obs", "seq_num"], schema="cdb_latiss")
    op.drop_constraint(
        "fk_ccdexposure_day_obs_seq_num", "ccdexposure", schema="cdb_latiss", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_exposure_id",
        "ccdexposure",
        "exposure",
        ["exposure_id"],
        ["exposure_id"],
        source_schema="cdb_latiss",
        referent_schema="cdb_latiss",
    )
    op.drop_constraint(
        "un_ccdexposure_day_obs_seq_num_detector", "ccdexposure", schema="cdb_latiss", type_="unique"
    )
    op.drop_constraint("un_ccdexposure_ccdexposure_id", "ccdexposure", schema="cdb_latiss", type_="unique")
    op.create_unique_constraint(
        "un_exposure_id_detector", "ccdexposure", ["exposure_id", "detector"], schema="cdb_latiss"
    )
    op.drop_column("ccdexposure", "seq_num", schema="cdb_latiss")
    op.drop_column("ccdexposure", "day_obs", schema="cdb_latiss")
    # ### end Alembic commands ###

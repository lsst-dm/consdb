"""Update the views

Revision ID: 8024a0becf41
Revises: ab45b3673c90
Create Date: 2025-04-17 16:33:23.022417+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8024a0becf41"
down_revision: Union[str, None] = "ab45b3673c90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        "ccdexposure",
        "Information from observatory systems about each detector (CCD) within each raw image taken",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "ccdexposure_camera",
        "Information from the Camera Control System about each detector (CCD) within each raw image taken",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "ccdexposure_flexdata",
        "Flexible key/value metadata about each detector (CCD) within each raw image taken; used for development and engineering purposes",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "ccdexposure_flexdata_schema",
        "Key names and value types used in the ccdexposure_flexdata table",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "ccdvisit1_quicklook",
        "Information from Summit Rapid Analysis about each detector (CCD) within each visit in visit system 1 (visit per exposure); describes detectors in processed visit images (or calibrated exposures)",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "exposure",
        "Information from observatory systems about each raw image taken",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "exposure_flexdata",
        "Flexible key/value metadata about each raw image taken; used for development and engineering purposes",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "exposure_flexdata_schema",
        "Key names and value types used in the exposure_flexdata table",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )
    op.create_table_comment(
        "visit1_quicklook",
        "Information from Summit Rapid Analysis about each visit in visit system 1 (visit per exposure); describes processed visit images (or calibrated exposures)",
        existing_comment=None,
        schema="cdb_lsstcomcamsim",
    )

    op.execute("DROP VIEW cdb_lsstcomcamsim.ccdvisit1")
    op.execute("DROP VIEW cdb_lsstcomcamsim.visit1")
    op.execute("CREATE VIEW cdb_lsstcomcamsim.ccdvisit1 AS SELECT * FROM cdb_lsstcomcamsim.ccdexposure")
    op.execute("CREATE VIEW cdb_lsstcomcamsim.visit1 AS SELECT * FROM cdb_lsstcomcamsim.exposure")
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN ccdexposure_id TO ccdvisit_id")
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")
    op.execute("ALTER TABLE cdb_lsstcomcamsim.visit1 RENAME COLUMN exposure_id TO visit_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        "visit1_quicklook",
        existing_comment="Information from Summit Rapid Analysis about each visit in visit system 1 (visit per exposure); describes processed visit images (or calibrated exposures)",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "exposure_flexdata_schema",
        existing_comment="Key names and value types used in the exposure_flexdata table",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "exposure_flexdata",
        existing_comment="Flexible key/value metadata about each raw image taken; used for development and engineering purposes",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "exposure",
        existing_comment="Information from observatory systems about each raw image taken",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "ccdvisit1_quicklook",
        existing_comment="Information from Summit Rapid Analysis about each detector (CCD) within each visit in visit system 1 (visit per exposure); describes detectors in processed visit images (or calibrated exposures)",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "ccdexposure_flexdata_schema",
        existing_comment="Key names and value types used in the ccdexposure_flexdata table",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "ccdexposure_flexdata",
        existing_comment="Flexible key/value metadata about each detector (CCD) within each raw image taken; used for development and engineering purposes",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "ccdexposure_camera",
        existing_comment="Information from the Camera Control System about each detector (CCD) within each raw image taken",
        schema="cdb_lsstcomcamsim",
    )
    op.drop_table_comment(
        "ccdexposure",
        existing_comment="Information from observatory systems about each detector (CCD) within each raw image taken",
        schema="cdb_lsstcomcamsim",
    )
    # ### end Alembic commands ###

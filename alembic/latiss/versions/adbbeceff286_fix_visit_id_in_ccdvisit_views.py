"""Fix visit_id in ccdvisit views.

Revision ID: adbbeceff286
Revises: 47c0b5ce839e
Create Date: 2024-12-05 00:56:52.135839+00:00

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "adbbeceff286"
down_revision: Union[str, None] = "47c0b5ce839e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

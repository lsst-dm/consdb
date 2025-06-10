"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

<% drop_sqls = config.attributes.get("drop_sqls", []) %>
<% upgrade_sqls = config.attributes.get("upgrade_sqls", []) %>
<% downgrade_sqls = config.attributes.get("downgrade_sqls", []) %>

def upgrade() -> None:
% for sql in drop_sqls:
    op.execute(${repr(sql)})
% endfor
    ${upgrades if upgrades else "pass"}
% for sql in upgrade_sqls:
    op.execute(${repr(sql)})
% endfor


def downgrade() -> None:
% for sql in drop_sqls:
    op.execute(${repr(sql)})
% endfor
    ${downgrades if downgrades else "pass"}
% for sql in downgrade_sqls:
    op.execute(${repr(sql)})
% endfor

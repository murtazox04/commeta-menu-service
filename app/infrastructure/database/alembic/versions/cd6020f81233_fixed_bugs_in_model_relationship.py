"""Fixed bugs in model relationship

Revision ID: cd6020f81233
Revises: bf53a91baaa7
Create Date: 2024-06-27 09:49:01.555893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd6020f81233'
down_revision: Union[str, None] = 'bf53a91baaa7'
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
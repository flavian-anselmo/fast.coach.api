"""empty message

Revision ID: ef1ffe7b6319
Revises: 685497c22089
Create Date: 2022-12-29 00:34:40.545237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef1ffe7b6319'
down_revision = '685497c22089'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments_tbl', sa.Column('paid_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments_tbl', 'paid_at')
    # ### end Alembic commands ###

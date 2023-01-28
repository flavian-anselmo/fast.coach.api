"""empty message

Revision ID: 89f891f4ed7e
Revises: 5bbfec2fff9d
Create Date: 2022-12-28 22:12:09.269860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f891f4ed7e'
down_revision = '5bbfec2fff9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments_tbl',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('is_payment_succesfull', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['book_ticket_tbl.ticket_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users_tbl.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments_tbl')
    # ### end Alembic commands ###

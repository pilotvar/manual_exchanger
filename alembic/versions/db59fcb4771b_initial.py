"""initial

Revision ID: db59fcb4771b
Revises: 
Create Date: 2024-07-06 15:54:45.930988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db59fcb4771b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(length=250), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('block', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_chat_id'), 'chats', ['chat_id'], unique=True)
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start', sa.Text(), nullable=True),
    sa.Column('tech', sa.Text(), nullable=True),
    sa.Column('exchange', sa.Text(), nullable=True),
    sa.Column('start_photo', sa.String(), nullable=True),
    sa.Column('tech_photo', sa.String(), nullable=True),
    sa.Column('exchange_photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    op.drop_index(op.f('ix_chats_chat_id'), table_name='chats')
    op.drop_table('chats')
    # ### end Alembic commands ###

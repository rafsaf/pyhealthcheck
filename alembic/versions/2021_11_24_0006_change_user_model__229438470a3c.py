"""change_user_model

Revision ID: 229438470a3c
Revises: cefce371682e
Create Date: 2021-11-24 00:06:21.148916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229438470a3c'
down_revision = 'cefce371682e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=254), nullable=False))
    op.add_column('user', sa.Column('is_maintainer', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('user', sa.Column('is_root', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.drop_index('ix_user_email', table_name='user')
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(length=254), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.drop_column('user', 'is_root')
    op.drop_column('user', 'is_maintainer')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###

"""healthcheck_table_rename_column_emails_to_alert

Revision ID: 1d0b2ba74305
Revises: f33c05f3c96f
Create Date: 2021-12-11 20:18:09.939531

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d0b2ba74305'
down_revision = 'f33c05f3c96f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('healthstack', sa.Column('emails_to_alert', sa.ARRAY(sa.String(length=128)), nullable=False))
    op.drop_column('healthstack', 'emails_list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('healthstack', sa.Column('emails_list', postgresql.ARRAY(sa.VARCHAR(length=128)), autoincrement=False, nullable=False))
    op.drop_column('healthstack', 'emails_to_alert')
    # ### end Alembic commands ###

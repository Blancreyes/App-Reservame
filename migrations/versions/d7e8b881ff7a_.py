"""empty message

Revision ID: d7e8b881ff7a
Revises: 77c2bbe97d8c
Create Date: 2023-03-22 12:44:12.936686

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd7e8b881ff7a'
down_revision = '77c2bbe97d8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.alter_column('startTime',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_constraint('reservas_startTime_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.create_unique_constraint('reservas_startTime_key', ['startTime'])
        batch_op.alter_column('startTime',
               existing_type=sa.String(length=120),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###
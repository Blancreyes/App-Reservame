"""empty message

Revision ID: 2931d550ecce
Revises: 573c0c0080ab
Create Date: 2023-03-12 09:28:26.600963

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2931d550ecce'
down_revision = '573c0c0080ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pistas', schema=None) as batch_op:
        batch_op.drop_constraint('pistas_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('startTime', sa.DateTime(), nullable=False))
        batch_op.drop_constraint('reservas_endDate_key', type_='unique')
        batch_op.drop_constraint('reservas_startDate_key', type_='unique')
        batch_op.create_unique_constraint(None, ['startTime'])
        batch_op.drop_column('endDate')
        batch_op.drop_column('startDate')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))

    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('startDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('endDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('reservas_startDate_key', ['startDate'])
        batch_op.create_unique_constraint('reservas_endDate_key', ['endDate'])
        batch_op.drop_column('startTime')

    with op.batch_alter_table('pistas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('pistas_user_id_fkey', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###

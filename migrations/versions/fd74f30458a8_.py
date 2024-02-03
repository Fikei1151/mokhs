"""empty message

Revision ID: fd74f30458a8
Revises: ace0f9296cb5
Create Date: 2024-02-03 19:11:41.533560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd74f30458a8'
down_revision = 'ace0f9296cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grade', schema=None) as batch_op:
        batch_op.add_column(sa.Column('classroom_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'classroom', ['classroom_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grade', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('classroom_id')

    # ### end Alembic commands ###

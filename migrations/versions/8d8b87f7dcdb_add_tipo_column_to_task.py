"""Add tipo column to Task

Revision ID: 8d8b87f7dcdb
Revises: 
Create Date: 2024-08-15 15:28:24.458384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d8b87f7dcdb'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('uf', sa.String(length=2), nullable=False))
        batch_op.add_column(sa.Column('gra', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('loc', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('estacao', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('ard', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('dc', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('status', sa.String(length=100), nullable=False))

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('tipo')
        batch_op.drop_column('uf')
        batch_op.drop_column('gra')
        batch_op.drop_column('loc')
        batch_op.drop_column('estacao')
        batch_op.drop_column('ard')
        batch_op.drop_column('dc')
        batch_op.drop_column('status')

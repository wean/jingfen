"""empty message

Revision ID: f3aa2b4f0460
Revises: 8c46cc16d9fd
Create Date: 2018-03-14 22:57:49.177128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3aa2b4f0460'
down_revision = '8c46cc16d9fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jd_uid', sa.String(length=128), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('sku', sa.String(length=128), nullable=True),
    sa.Column('spu', sa.String(length=128), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.Column('bonus_rate', sa.DECIMAL(), nullable=True),
    sa.Column('prize_amout', sa.DECIMAL(), nullable=True),
    sa.Column('image_url', sa.String(length=128), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('link', sa.String(length=128), nullable=True),
    sa.Column('ticket_id', sa.String(length=128), nullable=True),
    sa.Column('ticket_total_number', sa.Integer(), nullable=True),
    sa.Column('ticket_used_number', sa.Integer(), nullable=True),
    sa.Column('ticket_amount', sa.DECIMAL(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('ticket_valid', sa.Boolean(), nullable=True),
    sa.Column('jingfen_class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['jingfen_class_id'], ['jingfen_class.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('spu')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_jd_uid'), 'products', ['jd_uid'], unique=True)
    op.create_index(op.f('ix_products_sku'), 'products', ['sku'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_sku'), table_name='products')
    op.drop_index(op.f('ix_products_jd_uid'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###

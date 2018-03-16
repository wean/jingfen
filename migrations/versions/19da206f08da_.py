"""empty message

Revision ID: 19da206f08da
Revises: f3aa2b4f0460
Create Date: 2018-03-14 22:59:42.254539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '19da206f08da'
down_revision = 'f3aa2b4f0460'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jingfen_products',
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
    op.create_index(op.f('ix_jingfen_products_id'), 'jingfen_products', ['id'], unique=False)
    op.create_index(op.f('ix_jingfen_products_jd_uid'), 'jingfen_products', ['jd_uid'], unique=True)
    op.create_index(op.f('ix_jingfen_products_sku'), 'jingfen_products', ['sku'], unique=True)
    op.drop_index('ix_products_id', table_name='products')
    op.drop_index('ix_products_jd_uid', table_name='products')
    op.drop_index('ix_products_sku', table_name='products')
    op.drop_index('spu', table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('update_time', mysql.DATETIME(), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('jd_uid', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('title', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('sku', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('spu', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('price', mysql.DECIMAL(precision=10, scale=0), nullable=True),
    sa.Column('bonus_rate', mysql.DECIMAL(precision=10, scale=0), nullable=True),
    sa.Column('prize_amout', mysql.DECIMAL(precision=10, scale=0), nullable=True),
    sa.Column('image_url', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('url', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('link', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('ticket_id', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('ticket_total_number', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('ticket_used_number', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('ticket_amount', mysql.DECIMAL(precision=10, scale=0), nullable=True),
    sa.Column('start_time', mysql.DATETIME(), nullable=True),
    sa.Column('end_time', mysql.DATETIME(), nullable=True),
    sa.Column('ticket_valid', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('jingfen_class_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['jingfen_class_id'], [u'jingfen_class.id'], name=u'products_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_index('spu', 'products', ['spu'], unique=True)
    op.create_index('ix_products_sku', 'products', ['sku'], unique=True)
    op.create_index('ix_products_jd_uid', 'products', ['jd_uid'], unique=True)
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.drop_index(op.f('ix_jingfen_products_sku'), table_name='jingfen_products')
    op.drop_index(op.f('ix_jingfen_products_jd_uid'), table_name='jingfen_products')
    op.drop_index(op.f('ix_jingfen_products_id'), table_name='jingfen_products')
    op.drop_table('jingfen_products')
    # ### end Alembic commands ###
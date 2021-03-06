"""empty message

Revision ID: 01bd456fc3ef
Revises: 5d4f83fbfee1
Create Date: 2021-08-12 15:01:23.515956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '01bd456fc3ef'
down_revision = '5d4f83fbfee1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nick'),
    sa.UniqueConstraint('nick')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=250), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('email', table_name='user')
    op.drop_index('email_2', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.CheckConstraint('(`is_active` in (0,1))', name='user_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('email_2', 'user', ['email'], unique=False)
    op.create_index('email', 'user', ['email'], unique=False)
    op.drop_table('task')
    op.drop_table('account')
    # ### end Alembic commands ###

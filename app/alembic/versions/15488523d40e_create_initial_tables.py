"""create initial tables

Revision ID: 15488523d40e
Revises: 
Create Date: 2024-09-21 12:24:19.675197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15488523d40e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "user_types",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String(40), nullable=False)
    )

    op.create_table(
        "users",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(40), nullable=False),
        sa.Column('last_name', sa.String(40), nullable=False),
        sa.Column('password', sa.String(500), nullable=False),
        sa.Column('email', sa.String(40), nullable=False),
        sa.Column('phone', sa.String(40), nullable=True),
        sa.Column('user_type_id', sa.Integer, sa.ForeignKey("user_types.id"), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True)
    )

    op.create_table(
        "stations",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('city', sa.String(200), nullable=False)
    )

    op.create_table(
        "user_stations",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column('station_id', sa.Integer, sa.ForeignKey("stations.id"), nullable=False),
    )

    op.create_table(
        "device_types",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String(40), nullable=False)
    )

    op.create_table(
        "devices",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ip_address', sa.String(40), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('device_type_id', sa.Integer, sa.ForeignKey("device_types.id"), nullable=False),
        sa.Column('station_id', sa.Integer, sa.ForeignKey("stations.id"), nullable=False)

    )

    op.create_table(
        "device_data",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('device_id', sa.Integer, sa.ForeignKey("devices.id"), nullable=False),
        sa.Column('station_id', sa.Integer),
        sa.Column('ttl', sa.Integer),
        sa.Column('record_version', sa.Integer, nullable=False),
        sa.Column('data_length', sa.Integer, nullable=False)
    )

    op.create_table(
        "data_readings",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('device_data_id', sa.Integer, sa.ForeignKey("device_data.id"), nullable=False),
        sa.Column('value', sa.Integer, nullable=False)
    )

    # op.create_foreign_key('fk_device_type_id_device', 'devices', 'device_types', ['device_type_id'], ['id'])
    
    # op.create_foreign_key('fk_device_id_device', 'device_data', 'devices', ['device_id'], ['id'])

    # op.create_foreign_key('fk_device_data_id_device_data', 'data_readings', 'device_data', ['device_data_id'], ['id'])


def downgrade() -> None:
    pass

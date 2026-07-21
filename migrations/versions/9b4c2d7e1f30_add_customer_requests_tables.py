"""add customer requests tables

Revision ID: 9b4c2d7e1f30
Revises: 6287fae76eed
Create Date: 2026-07-22

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "9b4c2d7e1f30"
down_revision: str | None = "6287fae76eed"

branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customer_requests",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "request_type",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "customer_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "contact",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "telegram_chat_id",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "desired_datetime",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "person_count",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "comment",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            (
                "person_count IS NULL "
                "OR person_count BETWEEN 1 AND 500"
            ),
            name="ck_customer_requests_person_count",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_customer_requests_status",
        "customer_requests",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_customer_requests_status_request_type",
        "customer_requests",
        ["status", "request_type"],
        unique=False,
    )

    op.create_index(
        "ix_customer_requests_desired_datetime",
        "customer_requests",
        ["desired_datetime"],
        unique=False,
    )

    op.create_table(
        "customer_request_items",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "customer_request_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "menu_item_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "title_snapshot",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "price_amount_snapshot",
            sa.Numeric(
                precision=10,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "price_currency_snapshot",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "comment",
            sa.Text(),
            nullable=True,
        ),
        sa.CheckConstraint(
            "quantity BETWEEN 1 AND 100",
            name=(
                "ck_customer_request_items_quantity"
            ),
        ),
        sa.CheckConstraint(
            "price_amount_snapshot > 0",
            name=(
                "ck_customer_request_items_price_positive"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["customer_request_id"],
            ["customer_requests.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["menu_item_id"],
            ["menu_items.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        (
            "ix_customer_request_items_"
            "customer_request_id"
        ),
        "customer_request_items",
        ["customer_request_id"],
        unique=False,
    )

    op.create_index(
        "ix_customer_request_items_menu_item_id",
        "customer_request_items",
        ["menu_item_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_customer_request_items_menu_item_id",
        table_name="customer_request_items",
    )

    op.drop_index(
        (
            "ix_customer_request_items_"
            "customer_request_id"
        ),
        table_name="customer_request_items",
    )

    op.drop_table(
        "customer_request_items"
    )

    op.drop_index(
        "ix_customer_requests_desired_datetime",
        table_name="customer_requests",
    )

    op.drop_index(
        "ix_customer_requests_status_request_type",
        table_name="customer_requests",
    )

    op.drop_index(
        "ix_customer_requests_status",
        table_name="customer_requests",
    )

    op.drop_table(
        "customer_requests"
    )
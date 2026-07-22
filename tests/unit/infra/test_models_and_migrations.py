from pathlib import Path
import re

import pytest

from src.modules.catalog.infra.models import MenuCategoryModel, MenuItemModel
from src.modules.customer_requests.infra.models import (
    CustomerRequestItemModel,
    CustomerRequestModel,
)
from src.modules.notifications.infra.models import (
    NotificationDeliveryModel,
    ProcessedKafkaMessageModel,
)
from src.modules.users.infra.models import UserModel
from src.shared.outbox.infra.models import OutboxMessageModel


@pytest.mark.unit
def test_expected_tables_are_registered() -> None:
    assert UserModel.__tablename__ == "users"
    assert MenuCategoryModel.__tablename__ == "menu_categories"
    assert MenuItemModel.__tablename__ == "menu_items"
    assert CustomerRequestModel.__tablename__ == "customer_requests"
    assert CustomerRequestItemModel.__tablename__ == "customer_request_items"
    assert OutboxMessageModel.__tablename__ == "outbox_messages"
    assert NotificationDeliveryModel.__tablename__ == "notification_deliveries"
    assert ProcessedKafkaMessageModel.__tablename__ == "processed_kafka_messages"


@pytest.mark.unit
def test_customer_request_database_constraints_exist() -> None:
    request_constraints = {
        constraint.name for constraint in CustomerRequestModel.__table__.constraints
    }
    item_constraints = {
        constraint.name for constraint in CustomerRequestItemModel.__table__.constraints
    }

    assert "ck_customer_requests_person_count" in request_constraints
    assert "ck_customer_request_items_quantity" in item_constraints
    assert "ck_customer_request_items_price_positive" in item_constraints


@pytest.mark.unit
def test_migration_graph_has_single_linear_head() -> None:
    versions = Path("migrations/versions")
    revisions: dict[str, str | None] = {}

    for path in versions.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        revision_match = re.search(r"^revision[^=]*=\s*['\"]([^'\"]+)", text, re.M)
        down_match = re.search(
            r"^down_revision[^=]*=\s*(?:['\"]([^'\"]+)['\"]|None)",
            text,
            re.M,
        )
        assert revision_match, f"Revision not found in {path.name}"
        revisions[revision_match.group(1)] = (
            down_match.group(1) if down_match and down_match.group(1) else None
        )

    parents = {parent for parent in revisions.values() if parent is not None}
    heads = set(revisions) - parents

    assert heads == {"9b4c2d7e1f30"}
    assert revisions["9b4c2d7e1f30"] == "6287fae76eed"
    assert revisions["6287fae76eed"] == "e906f5c2f554"

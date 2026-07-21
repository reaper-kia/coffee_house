# src/modules/customer_requests/infra/repositories.py

from uuid import UUID
from decimal import Decimal

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.customer_requests.domain.exceptions import CustomerRequestNotFound
from src.modules.customer_requests.application.ports.customer_request_read_repository import CustomerRequestReadRepository
from src.modules.customer_requests.application.ports.customer_request_repository import CustomerRequestRepository
from src.modules.customer_requests.application.ports.menu_item_snapshot_repository import MenuItemSnapshotRepository, ProductSnapshot
from src.modules.customer_requests.domain.entities import CustomerRequest, CustomerRequestItem
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType
from src.modules.customer_requests.application.read_models import (
    CustomerRequestReadModel,
    CustomerRequestItemReadModel,
    CustomerRequestPageReadModel,
)

from src.modules.customer_requests.infra.models import (
    CustomerRequestModel,
    CustomerRequestItemModel,
)

from src.modules.catalog.infra.models import MenuItemModel, MenuCategoryModel


# ============================================================
# 1. WRITE-РЕПОЗИТОРИЙ (для доменных сущностей)
# ============================================================
class SQLAlchemyCustomerRequestRepository(CustomerRequestRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, request: CustomerRequest) -> None:
        """Сохранить новую заявку (INSERT)."""
        model = self._to_model(request)
        self.session.add(model)

    async def get_by_id(self, request_id: UUID) -> CustomerRequest | None:
        """Найти заявку по ID и вернуть доменную сущность."""
        stmt = (
            select(CustomerRequestModel)
            .where(CustomerRequestModel.id == request_id)
            .options(selectinload(CustomerRequestModel.items))  # Подгружаем items
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def save(self, request: CustomerRequest) -> None:
        """Обновить существующую заявку (UPDATE)."""
        # 1. Загружаем модель с её items
        stmt = (
            select(CustomerRequestModel)
            .where(CustomerRequestModel.id == request.id)
            .options(selectinload(CustomerRequestModel.items))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise CustomerRequestNotFound(
                f"Customer request {request.id} not found"
            )

        # 2. Обновляем простые поля
        model.request_type = request.request_type.value
        model.customer_name = request.customer_name
        model.contact = request.contact
        model.telegram_chat_id = request.telegram_chat_id
        model.desired_datetime = request.desired_datetime
        model.person_count = request.person_count
        model.comment = request.comment
        model.status = request.status.value
        model.updated_at = request.updated_at

        # 3. Обновляем items (удаляем старые, добавляем новые)
        model.items.clear()
        for item in request.items:
            item_model = CustomerRequestItemModel(
                menu_item_id=item.menu_item_id,
                title_snapshot=item.title_snapshot,
                price_amount_snapshot=item.price_amount_snapshot,
                price_currency_snapshot=item.price_currency_snapshot,
                quantity=item.quantity,
                comment=item.comment,
            )
            model.items.append(item_model)

    # ---------- Вспомогательные мапперы ----------
    @staticmethod
    def _to_model(request: CustomerRequest) -> CustomerRequestModel:
        """Превращает доменную сущность в SQLAlchemy-модель (для вставки)."""
        return CustomerRequestModel(
            id=request.id,
            request_type=request.request_type.value,
            customer_name=request.customer_name,
            contact=request.contact,
            telegram_chat_id=request.telegram_chat_id,
            desired_datetime=request.desired_datetime,
            person_count=request.person_count,
            comment=request.comment,
            status=request.status.value,
            created_at=request.created_at,
            updated_at=request.updated_at,
            items=[
                CustomerRequestItemModel(
                    menu_item_id=item.menu_item_id,
                    title_snapshot=item.title_snapshot,
                    price_amount_snapshot=item.price_amount_snapshot,
                    price_currency_snapshot=item.price_currency_snapshot,
                    quantity=item.quantity,
                    comment=item.comment,
                )
                for item in request.items
            ],
        )

    @staticmethod
    def _to_domain(model: CustomerRequestModel) -> CustomerRequest:
        """Превращает SQLAlchemy-модель в доменную сущность."""
        items = [
            CustomerRequestItem(
                menu_item_id=item.menu_item_id,
                title_snapshot=item.title_snapshot,
                price_amount_snapshot=item.price_amount_snapshot,
                price_currency_snapshot=item.price_currency_snapshot,
                quantity=item.quantity,
                comment=item.comment,
            )
            for item in model.items
        ]
        return CustomerRequest(
            id=model.id,
            request_type=CustomerRequestType(model.request_type),
            customer_name=model.customer_name,
            contact=model.contact,
            desired_datetime=model.desired_datetime,
            person_count=model.person_count,
            comment=model.comment,
            telegram_chat_id=model.telegram_chat_id,
            status=CustomerRequestStatus(model.status),
            _items=items,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


# ============================================================
# 2. READ-РЕПОЗИТОРИЙ (для read-моделей / DTO)
# ============================================================
class SQLAlchemyCustomerRequestReadRepository(CustomerRequestReadRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, request_id: UUID) -> CustomerRequestReadModel | None:
        """Вернуть read-модель заявки по ID (оптимизировано для отображения)."""
        # Загружаем заявку с items одним запросом
        stmt = (
            select(CustomerRequestModel)
            .where(CustomerRequestModel.id == request_id)
            .options(selectinload(CustomerRequestModel.items))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_read_model(model)

    async def list(
        self,
        status: CustomerRequestStatus | None,
        request_type: CustomerRequestType | None,
        limit: int,
        offset: int,
    ) -> CustomerRequestPageReadModel:
        """Вернуть страницу read-моделей с пагинацией и фильтрами."""
        # 1. Базовый запрос
        query = select(CustomerRequestModel)

        # 2. Применяем фильтры
        if status is not None:
            query = query.where(CustomerRequestModel.status == status.value)
        if request_type is not None:
            query = query.where(CustomerRequestModel.request_type == request_type.value)

        # 3. Считаем общее количество (для пагинации)
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        # 4. Загружаем данные с пагинацией и сортировкой
        query = (
            query
            .order_by(CustomerRequestModel.created_at.desc())
            .limit(limit)
            .offset(offset)
            .options(selectinload(CustomerRequestModel.items))  # ← Загружаем items для каждой заявки
        )
        result = await self.session.execute(query)
        models = result.scalars().all()

        # 5. Преобразуем в read-модели
        items = [self._to_read_model(model) for model in models]
        return CustomerRequestPageReadModel(items=items, total=total)

    # ---------- Вспомогательный маппер (ORM → ReadModel) ----------
    @staticmethod
    def _to_read_model(model: CustomerRequestModel) -> CustomerRequestReadModel:
        """Превращает SQLAlchemy-модель в read-модель (DTO)."""
        return CustomerRequestReadModel(
            id=model.id,
            request_type=CustomerRequestType(model.request_type),
            customer_name=model.customer_name,
            contact=model.contact,
            telegram_chat_id=model.telegram_chat_id,
            desired_datetime=model.desired_datetime,
            person_count=model.person_count,
            comment=model.comment,
            status=CustomerRequestStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            items=[
                CustomerRequestItemReadModel(
                    menu_item_id=item.menu_item_id,
                    title=item.title_snapshot,
                    quantity=item.quantity,
                    price_amount=item.price_amount_snapshot,
                    price_currency=item.price_currency_snapshot,
                    comment=item.comment,
                )
                for item in model.items
            ],
        )


# ============================================================
# 3. РЕПОЗИТОРИЙ ДЛЯ СНАПШОТОВ (чтение из каталога)
# ============================================================
class SQLAlchemyMenuItemSnapshotRepository(MenuItemSnapshotRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_available_by_ids(self, menu_item_ids: set[UUID]) -> dict[UUID, ProductSnapshot]:
        """
        Получить снапшоты для списка ID товаров.
        Возвращает словарь {menu_item_id: ProductSnapshot}.
        Фильтрует только доступные товары (is_available=True) из активных категорий.
        """
        if not menu_item_ids:
            return {}

        # 1. Запрос к таблицам каталога
        stmt = (
            select(
                MenuItemModel.id,
                MenuItemModel.title,
                MenuItemModel.price_amount,
                MenuItemModel.price_currency,
            )
            .outerjoin(
                MenuCategoryModel,
                MenuItemModel.category_id == MenuCategoryModel.id,
            )
            .where(
                MenuItemModel.id.in_(menu_item_ids),
                MenuItemModel.is_available.is_(True),
                or_(
                    MenuItemModel.category_id.is_(None),
                    MenuCategoryModel.is_active.is_(True),
                ),
            )
        )

        # 2. Выполняем запрос
        result = await self.session.execute(stmt)
        rows = result.all()

        # 3. Превращаем строки в словарь {id: ProductSnapshot}
        return {
            row.id: ProductSnapshot(
                menu_item_id=row.id,
                title=row.title,
                price_amount=row.price_amount,
                price_currency=row.price_currency,
            )
            for row in rows
        }
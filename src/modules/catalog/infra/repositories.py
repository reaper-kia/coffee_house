from uuid import UUID
from typing import Optional, List

from sqlalchemy import select, exists, or_
from sqlalchemy.ext.asyncio import AsyncSession


from src.modules.catalog.domain.entities import MenuItem, MenuCategory
from src.shared.domain.value_objects import Money
from src.modules.catalog.domain.value_objects import (
    ProductTitle,
    CategoryTitle,
    Description,
    Position,
)



from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.modules.catalog.application.ports.menu_item_repository import MenuItemRepository


from src.modules.catalog.infra.models import MenuItemModel, MenuCategoryModel
from src.modules.catalog.application.read_models import CategoryReadModel, MenuItemReadModel



class SQLAlchemyMenuCategoryRepository(MenuCategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, category: MenuCategory) -> None:
        stmt = select(MenuCategoryModel).where(MenuCategoryModel.id == category.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = MenuCategoryModel(
                id=category.id,
                title=category.title.value,
                position=category.position.value,
                is_active=category.is_active,
            )
            self.session.add(model)
        else:
            model.title = category.title.value
            model.position = category.position.value
            model.is_active = category.is_active

    async def get_by_id(self, category_id: UUID) -> Optional[MenuCategory]:
        stmt = select(MenuCategoryModel).where(MenuCategoryModel.id == category_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def delete(self, category_id: UUID) -> None:
        stmt = select(MenuCategoryModel).where(MenuCategoryModel.id == category_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)

    async def exists_by_id(self, category_id: UUID) -> bool:
        stmt = select(exists().where(MenuCategoryModel.id == category_id))
        result = await self.session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    def _to_domain(model: MenuCategoryModel) -> MenuCategory:
        return MenuCategory(
            id=model.id,
            title=CategoryTitle(model.title),
            position=Position(model.position),
            is_active=model.is_active,
        )


class SQLAlchemyMenuItemRepository(MenuItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, item: MenuItem) -> None:
        stmt = select(MenuItemModel).where(MenuItemModel.id == item.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = MenuItemModel(
                id=item.id,
                category_id=item.category_id,
                title=item.title.value,
                price_amount=item.price.amount,
                price_currency=item.price.currency,
                description=item.description.value,
                is_available=item.is_available,
                image_url=item.image_url,
                position=item.position.value,
            )
            self.session.add(model)
        else:
            model.category_id = item.category_id
            model.title = item.title.value
            model.price_amount = item.price.amount
            model.price_currency = item.price.currency
            model.description = item.description.value
            model.is_available = item.is_available
            model.image_url = item.image_url
            model.position = item.position.value

    async def get_by_id(self, item_id: UUID) -> Optional[MenuItem]:
        stmt = select(MenuItemModel).where(MenuItemModel.id == item_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def delete(self, item_id: UUID) -> None:
        stmt = select(MenuItemModel).where(MenuItemModel.id == item_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)

    async def exists_by_id(self, item_id: UUID) -> bool:
        stmt = select(exists().where(MenuItemModel.id == item_id))
        result = await self.session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    def _to_domain(model: MenuItemModel) -> MenuItem:
        return MenuItem(
            id=model.id,
            category_id=model.category_id,
            title=ProductTitle(model.title),
            price=Money(amount=model.price_amount, currency=model.price_currency),
            description=Description(model.description),
            is_available=model.is_available,
            image_url=model.image_url,
            position=Position(model.position),
        )


class SQLAlchemyMenuCategoryReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_categories(
        self,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CategoryReadModel]:
        stmt = select(
            MenuCategoryModel.id,
            MenuCategoryModel.title,
            MenuCategoryModel.position,
            MenuCategoryModel.is_active,
        )
        if active_only:
            stmt = stmt.where(MenuCategoryModel.is_active.is_(True))
        stmt = stmt.order_by(
            MenuCategoryModel.position,
            MenuCategoryModel.title,
        ).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            CategoryReadModel(
                id=row.id,
                title=row.title,
                position=row.position,
                is_active=row.is_active,
            )
            for row in rows
        ]


class SQLAlchemyMenuItemReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_menu_items(
        self,
        category_id: UUID | None = None,
        available_only: bool = True,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[MenuItemReadModel]:
        stmt = select(
            MenuItemModel.id,
            MenuItemModel.category_id,
            MenuCategoryModel.title.label("category_title"),
            MenuItemModel.title,
            MenuItemModel.description,
            MenuItemModel.price_amount,
            MenuItemModel.price_currency,
            MenuItemModel.image_url,
            MenuItemModel.is_available,
            MenuItemModel.position,
        ).outerjoin(
            MenuCategoryModel,
            MenuItemModel.category_id == MenuCategoryModel.id
        )
        if category_id is not None:
            stmt = stmt.where(MenuItemModel.category_id == category_id)
        if available_only:
            stmt = stmt.where(MenuItemModel.is_available.is_(True))
        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    MenuItemModel.title.ilike(search_pattern),
                    MenuItemModel.description.ilike(search_pattern),
                )
            )
        stmt = stmt.order_by(
            MenuCategoryModel.position,
            MenuItemModel.position,
            MenuItemModel.title,
        ).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            MenuItemReadModel(
                id=row.id,
                category_id=row.category_id,
                category_title=row.category_title,
                title=row.title,
                description=row.description,
                price_amount=row.price_amount,
                price_currency=row.price_currency,
                image_url=row.image_url,
                is_available=row.is_available,
                position=row.position,
            )
            for row in rows
        ]

    async def get_by_id(self, menu_item_id: UUID) -> Optional[MenuItemReadModel]:
        stmt = select(
            MenuItemModel.id,
            MenuItemModel.category_id,
            MenuCategoryModel.title.label("category_title"),
            MenuItemModel.title,
            MenuItemModel.description,
            MenuItemModel.price_amount,
            MenuItemModel.price_currency,
            MenuItemModel.image_url,
            MenuItemModel.is_available,
            MenuItemModel.position,
        ).outerjoin(
            MenuCategoryModel,
            MenuItemModel.category_id == MenuCategoryModel.id
        ).where(MenuItemModel.id == menu_item_id)
        result = await self.session.execute(stmt)
        row = result.one_or_none()
        if row is None:
            return None
        return MenuItemReadModel(
            id=row.id,
            category_id=row.category_id,
            category_title=row.category_title,
            title=row.title,
            description=row.description,
            price_amount=row.price_amount,
            price_currency=row.price_currency,
            image_url=row.image_url,
            is_available=row.is_available,
            position=row.position,
        )
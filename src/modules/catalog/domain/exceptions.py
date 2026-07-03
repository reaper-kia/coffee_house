class CatalogDomainError(Exception):
    pass


class InvalidCategoryNameError(CatalogDomainError):
    """Некорректное название категории."""
    pass

class InvalidProductTitleError(CatalogDomainError):
    """Некорректное название товара."""
    pass

class InvalidProductDescriptionError(CatalogDomainError):
    """Некорректное описание товара."""
    pass

class InvalidCurrencyError(CatalogDomainError):
    """Неподдерживаемая валюта (только USD, EUR)."""
    pass

class NegativeAmountError(CatalogDomainError):
    """Отрицательная сумма денег."""
    pass

class InvalidPositionError(CatalogDomainError):
    """Некорректная позиция (отрицательное значение)."""
    pass

class MenuItemNotFoundError(CatalogDomainError):
    pass

class CategoryNotFoundError(CatalogDomainError):
    pass

class CategoryAlreadyExistsError(CatalogDomainError):
    pass
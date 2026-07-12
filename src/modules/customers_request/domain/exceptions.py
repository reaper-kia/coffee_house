class DomainOrderError(Exception):
    ...


class EmptyOrderError(DomainOrderError):
    ...


class DifferentCurrencyInOrderError(DomainOrderError):
    ...


class InvalidQuantityError(DomainOrderError):
    ...


class OrderNotFoundError(DomainOrderError):
    ...


class ProductForOrderNotFoundError(DomainOrderError):
    ...

class InvalidOrderStatusTransitionError(DomainOrderError):
    ...
    
class OrderAccessDeniedError(DomainOrderError):
    ...
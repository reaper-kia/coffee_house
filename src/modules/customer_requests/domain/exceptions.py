class CustomerRequestException(Exception):
    """Base exception for customer request business rules."""


class CustomerRequestNotFound(CustomerRequestException):
    pass


class CustomerRequestStatusInvalidTransition(CustomerRequestException):
    pass


class CustomerRequestEmptyError(CustomerRequestException):
    pass


class CustomerRequestInvalidPersonCountError(CustomerRequestException):
    pass


class CustomerRequestInvalidTypeError(CustomerRequestException):
    pass


class CustomerRequestItemInvalidQuantityError(CustomerRequestException):
    pass


class CustomerRequestItemInvalidTitleError(CustomerRequestException):
    pass


class CustomerRequestItemInvalidPriceError(CustomerRequestException):
    pass


class CustomerRequestItemInvalidCurrencyError(CustomerRequestException):
    pass


class CustomerRequestItemInvalidCommentError(CustomerRequestException):
    pass


class MenuItemUnavailable(CustomerRequestException):
    pass
class CustomerRequestException(Exception):
    pass


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

class CustomerRequestItemInvalidCommentError(CustomerRequestException):
    pass

class InvalidCustomerRequest(CustomerRequestException):
    pass

class MenuItemUnavailable(CustomerRequestException):
    pass
class CustomerRequestStatusInvalidTransition(CustomerRequestException):
    pass
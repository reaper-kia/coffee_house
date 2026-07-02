class CustomerRequestException(Exception):
    pass


class CustomerRequestNotFound(CustomerRequestException):
    pass


class InvalidCustomerRequestStatusTransition(CustomerRequestException):
    pass
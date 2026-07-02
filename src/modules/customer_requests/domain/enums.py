from enum import StrEnum


class CustomerRequestStatus(StrEnum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    DONE = "DONE"


class CustomerRequestType(StrEnum):
    TABLE_BOOKING = "TABLE_BOOKING"
    PREORDER = "PREORDER"
    EVENT_REQUEST = "EVENT_REQUEST"
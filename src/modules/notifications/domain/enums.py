from enum import StrEnum


class NotificationChannel(StrEnum):
    TELEGRAM = "TELEGRAM"


class NotificationDeliveryStatus(StrEnum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
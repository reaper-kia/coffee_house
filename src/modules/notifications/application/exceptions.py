class NotificationProcessingError(Exception):
    pass


class InvalidIntegrationEvent(NotificationProcessingError):
    pass


class UnsupportedIntegrationEvent(NotificationProcessingError):
    pass
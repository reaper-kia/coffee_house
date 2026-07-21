class NotificationError(Exception):
    pass


class NotificationNotFoundError(NotificationError):
    pass


class NotificationAccessDeniedError(NotificationError):
    pass
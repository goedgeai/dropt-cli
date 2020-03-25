import copy


class DrOptException(Exception):
    pass


class ConnectionException(DrOptException):
    def __init__(self, message):
        super(ConnectionException, self).__init__(message)
        self.message = message

    def __str__(self):
        message = self.message if self.message is not None else ''
        return f'ConnectionException: {message}'


class ApiException(DrOptException):
    def __init__(self, body, status_code):
        self.message = body.get('message', None) if body is not None else None
        self._body = body
        if self.message is not None:
            super(ApiException, self).__init__(self.message)
        else:
            super(ApiException, self).__init__()
        self.status_code = status_code

    def __str__(self):
        message = self.message if self.message is not None else ''
        return f'ApiException ({self.status_code}): {message}'

    def to_json(self):
        return copy.deepcopy(self._body)

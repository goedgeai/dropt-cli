import copy
from .vendored import six as six


class DrOptException(Exception):
  pass


@six.python_2_unicode_compatible
class ConnectionException(DrOptException):
  def __init__(self, message):
    super(ConnectionException, self).__init__(message)
    self.message = message

  def __str__(self):
    return six.u('{0}: {1}').format(
      'ConnectionException',
      self.message if self.message is not None else '',
    )

@six.python_2_unicode_compatible
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
    return six.u('{0} ({1}): {2}').format(
      'ApiException',
      self.status_code,
      self.message if self.message is not None else '',
    )

  def to_json(self):
    return copy.deepcopy(self._body)

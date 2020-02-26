import copy
import warnings

from .compat import json
from .vendored import six as six


class ListOf(object):
  def __init__(self, type):
    self.type = type

  def __call__(self, value):
    return [self.type(v) for v in value]


Any = lambda x: x


class Field(object):
  def __init__(self, type):
    self.type = type

  def __call__(self, value):
    if value is None:
      return None
    return self.type(value)


class DeprecatedField(Field):
  def __init__(self, type, recommendation=None):
    super(DeprecatedField, self).__init__(type)
    self.recommendation = (' ' + recommendation) if recommendation else ''

  def __call__(self, value):
    warnings.warn(
      'This field has been deprecated and may be removed in a future version.{0}'.format(self.recommendation),
      DeprecationWarning,
    )
    return super(DeprecatedField, self).__call__(value)


class BaseApiObject(object):
  def __getattribute__(self, name):
    value = object.__getattribute__(self, name)
    if isinstance(value, Field):
      return value(self._body.get(name))
    return value

  def __setattr__(self, name, value):
    field = self._get_field(name)
    if field:
      value = ApiObject.as_json(value)
      self._body[name] = value
    else:
      object.__setattr__(self, name, value)

  def __delattr__(self, name):
    field = self._get_field(name)
    if field:
      del self._body[name]
    else:
      object.__delattr__(self, name)

  def _get_field(self, name):
    try:
      subvalue = object.__getattribute__(self, name)
    except AttributeError:
      return None
    else:
      return subvalue if isinstance(subvalue, Field) else None

  def __repr__(self):
    return six.u('{0}({1})').format(
      self.__class__.__name__,
      json.dumps(
        ApiObject.as_json(self._body),
        indent=2,
        sort_keys=True,
        separators=(',', ': '),
      ),
    )

  def to_json(self):
    return copy.deepcopy(self._body)


class ApiObject(BaseApiObject):
  def __init__(self, body, bound_endpoint=None, retrieve_params=None):
    super(ApiObject, self).__init__()
    object.__setattr__(self, '_body', body)
    object.__setattr__(self, '_bound_endpoint', bound_endpoint)
    object.__setattr__(self, '_retrieve_params', retrieve_params)

  def __eq__(self, other):
    return (
      isinstance(other, self.__class__) and
      self._body == other._body
    )

  @staticmethod
  def as_json(obj):
    if isinstance(obj, BaseApiObject):
      return obj.to_json()
    elif isinstance(obj, dict):
      c = {}
      for key in obj:
        c[key] = ApiObject.as_json(obj[key])
      return c
    elif isinstance(obj, list):
      return [ApiObject.as_json(c) for c in obj]
    return obj


class _DictWrapper(BaseApiObject, dict):
  def __init__(self, body, bound_endpoint=None, retrieve_params=None):
    super(_DictWrapper, self).__init__()
    dict.__init__(self, body)
    self._bound_endpoint = bound_endpoint
    self._retrieve_params = retrieve_params

  @property
  def _body(self):
    return self

  def to_json(self):
    return dict(copy.deepcopy(self))

  def copy(self):
    return self.__class__(dict.copy(self))

  def __eq__(self, other):
    return (
      isinstance(other, self.__class__) and
      dict.__eq__(self, other)
    )

class Validation(ApiObject):
  valid_id = Field(six.text_type)
  suggest_id = Field(six.text_type)
  value = Field(float)

class Assignment(ApiObject):
  assign_id = Field(six.text_type)
  name = Field(six.text_type)
  value = Field(six.text_type)

class Assignments(_DictWrapper):
  pass

class Parameter(ApiObject):
  param_id = Field(six.text_type)
  prj_id = Field(six.text_type)
  name = Field(six.text_type)
  type = Field(six.text_type)
  max = Field(float)
  min = Field(float)
  value = Field(six.text_type)

class Suggestion(ApiObject):
  suggest_id = Field(six.text_type)
  project_id = Field(six.text_type)
  index = Field(six.text_type)
  state = Field(six.text_type)
  create_dt = Field(six.text_type)
  assignments = Field(Assignments)

class Project(ApiObject):
  project_id = Field(six.text_type)
  name = Field(six.text_type)
  trial = Field(int)
  parameters = Field(ListOf(Parameter))
  progress = Field(int)

class Token(ApiObject):
  all_experiments = Field(bool)
  client = Field(six.text_type)
  development = Field(bool)
  experiment = Field(six.text_type)
  permissions = DeprecatedField(six.text_type)
  token = Field(six.text_type)
  token_type = Field(six.text_type)
  user = Field(six.text_type)


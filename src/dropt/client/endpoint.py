import json
from .objects import ResponseSuggestion

class BoundApiEndpoint(object):
  def __init__(self, bound_resource, endpoint):
    self._bound_resource = bound_resource
    self._endpoint = endpoint

  def call_with_json(self, json):
    return self.call_with_params(json.loads(json))

  def call_with_params(self, params):
    name = self._endpoint._name
    url = self._bound_resource._base_url + ('/' + name if name else '')
    conn = self._bound_resource._resource._conn
    raw_response = None

    raw_response = conn._request(self._endpoint._method, url, params)

    if self._endpoint._response_cls is not None:
      return self._endpoint._response_cls(raw_response, self, params)
    return None

  def __call__(self, **kwargs):
    rep = self.call_with_params(kwargs)

    # type casting (str -> int or float)
    if hasattr(rep, 'assignments'):
      resp_sugt = ResponseSuggestion(rep.suggest_id)
      for a in rep.assignments:
        if self.is_number(rep.assignments[a]):
          if float(rep.assignments[a]).is_integer():
            resp_sugt.assignments[a] = int(float(rep.assignments[a]))
          else:
            resp_sugt.assignments[a] = float(rep.assignments[a])
        else:
          resp_sugt.assignments[a] = rep.assignments[a]
      return resp_sugt

    if 'msg' in rep._body:
      raise ValueError(rep._body['msg'])
    return rep

  def is_number(self, s):
    try:
      float(s)
      return True
    except ValueError:
      return False


class ApiEndpoint(object):
  def __init__(self, name, response_cls, method, attribute_name=None):
    self._name = name
    self._response_cls = response_cls
    self._method = method
    self._attribute_name = attribute_name or name

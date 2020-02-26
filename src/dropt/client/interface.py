import os

from .compat import json as simplejson
from .endpoint import ApiEndpoint
from .objects import (
  ApiObject,
  Project,
  Suggestion,
  Validation,
  Token,
)
from .requestor import Requestor, DEFAULT_API_URL
from .resource import ApiResource
from .version import __version__

class ConnectionImpl(object):
  def __init__(self, requestor, api_url=None):
    self.requestor = requestor
    self.api_url = api_url or DEFAULT_API_URL

    suggestions = ApiResource(
      self,
      "suggestions",
      endpoints=[
        ApiEndpoint(None, Suggestion, "POST", "create"),
        ApiEndpoint(None, object_or_paginated_objects(Suggestion), "GET", "fetch"),
        ApiEndpoint(None, Suggestion, "PUT", "update"),
        ApiEndpoint(None, None, "DELETE", "delete"),
      ],
    )

    validations = ApiResource(
      self,
      "validations",
      endpoints=[
        ApiEndpoint(None, Validation, "POST", "create"),
        ApiEndpoint(None, object_or_paginated_objects(Validation), "GET", "fetch"),
        ApiEndpoint(None, Validation, "PUT", "update"),
        ApiEndpoint(None, None, "DELETE", "delete"),
      ],
    )

    tokens = ApiResource(
      self,
      "tokens",
      endpoints=[
        ApiEndpoint(None, Token, "POST", "create"),
      ],
    )

    self.projects = ApiResource(
      self,
      "projects",
      endpoints=[
        ApiEndpoint(None, Project, "POST", "create"),
        ApiEndpoint(None, object_or_paginated_objects(Project), "GET", "fetch"),
        ApiEndpoint(None, Project, "PUT", "update"),
        ApiEndpoint(None, None, "DELETE", "delete"),
      ],
      resources=[
        suggestions,
        validations,
        tokens,
      ],
    )

    client_projects = ApiResource(
      self,
      "projects",
      endpoints=[
        ApiEndpoint(None, Project, "POST", "create"),
        ApiEndpoint(None, lambda *args, **kwargs: Pagination(Project, *args, **kwargs), "GET", "fetch"),
      ],
    )

  def _request(self, method, url, params):
    if method.upper() in ("GET", "DELETE"):
      json, params = None, self._request_params(params)
    else:
      json, params = ApiObject.as_json(params), None
    return self.requestor.request(
      method,
      url,
      json=json,
      params=params,
    )

  def _get(self, url, params=None):
    return self._request("GET", url, params)

  def _post(self, url, params=None):
    return self._request("POST", url, params)

  def _put(self, url, params=None):
    return self._request("PUT", url, params)

  def _delete(self, url, params=None):
    return self._request("DELETE", url, params)

  def _request_params(self, params):
    req_params = params or {}

    def serialize(value):
      if isinstance(value, (dict, list)):
        return simplejson.dumps(value)
      return str(value)

    return dict((
      (key, serialize(ApiObject.as_json(value)))
      for key, value
      in req_params.items()
      if value is not None
    ))

  def set_api_url(self, api_url):
    self.api_url = api_url

  def set_verify_ssl_certs(self, verify_ssl_certs):
    self.requestor.verify_ssl_certs = verify_ssl_certs

  def set_proxies(self, proxies):
    self.requestor.proxies = proxies

  def set_timeout(self, timeout):
    self.requestor.timeout = timeout


class Connection(object):
  def __init__(self, client_token=None, user_agent=None, server_ip="140.113.24.232"):
    client_token = client_token
    # api_url = os.environ.get("SIGOPT_API_URL") or DEFAULT_API_URL
    api_url = os.environ.get("SIGOPT_API_URL") or "http://"+ server_ip + ":8080"
    if not client_token:
      raise ValueError("Must provide client_token.")

    default_headers = {
      "Content-Type": "application/json",
      "User-Agent": user_agent if user_agent is not None else "dropt-python/{0}".format(__version__),
      "X-DrOpt-Python-Version": __version__,
    }
    requestor = Requestor(
      client_token,
      "",
      default_headers,
    )
    self.impl = ConnectionImpl(requestor, api_url=api_url)

  def set_api_url(self, api_url):
    self.impl.set_api_url(api_url)

  def set_verify_ssl_certs(self, verify_ssl_certs):
    self.impl.set_verify_ssl_certs(verify_ssl_certs)

  def set_proxies(self, proxies):
    self.impl.set_proxies(proxies)

  def set_timeout(self, timeout):
    self.impl.set_timeout(timeout)

  @property
  def projects(self):
    return self.impl.projects

def object_or_paginated_objects(api_object):
  def decorator(body, *args, **kwargs):
    if body.get("object") == "pagination":
      return Pagination(api_object, body, *args, **kwargs)
    return api_object(body, *args, **kwargs)
  return decorator

def load_config_file(file_name):
    with open(file_name) as json_file:
        config = json.load(json_file)
    return json.dumps(config) 

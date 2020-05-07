import json
from .__init__ import __version__
from .endpoint import ApiEndpoint
from .objects import ApiObject, Project, Suggestion, Validation, Token
from .requestor import Requestor
from .resource import ApiResource


class ConnectionImpl:
    def __init__(self, requestor, api_url=None):
        self.requestor = requestor
        self.api_url = api_url

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
                ApiEndpoint(None, Project, "POST", "resume")
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
                ApiEndpoint(None, Project, "POST", "resume")
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
                return json.dumps(value)
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


class Connection:
    def __init__(self, client_token=None, server_ip=None, server_port=""):
        client_token = client_token
        if server_port != "":
            api_url = f"http://{server_ip}:{server_port}"
        else:
            api_url = f"https://{server_ip}"
        if not client_token:
            raise ValueError("Must provide client_token.")

        default_headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "dropt-cli/{__version__}"
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

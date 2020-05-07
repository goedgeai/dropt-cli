import json

from .objects import ResponseSuggestion
from .util import is_float


class BoundApiEndpoint:
    def __init__(self, bound_resource, endpoint):
        self._bound_resource = bound_resource
        self._endpoint = endpoint

    def call_with_json(self, string):
        return self.call_with_params(json.loads(string))

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
        if self._endpoint.get_attribute_name() == 'resume':
            assert kwargs.get('project_id') != None, "Please provide the project_id of the resumed project!"
            self._bound_resource._base_url += "/resume/"+str(kwargs['project_id'])
        
        rep = self.call_with_params(kwargs)

        # type casting (str -> int or float)
        if hasattr(rep, 'assignments'):
            resp_sugt = ResponseSuggestion(rep.suggest_id)
            for key in rep.assignments:
                if is_float(rep.assignments[key]):
                    if float(rep.assignments[key]).is_integer():
                        resp_sugt.assignments[key] = int(float(rep.assignments[key]))
                    else:
                        resp_sugt.assignments[key] = float(rep.assignments[key])
                else:
                    resp_sugt.assignments[key] = rep.assignments[key]
            return resp_sugt

        if 'msg' in rep._body:
            raise ValueError(rep._body['msg'])
        return rep


class ApiEndpoint:
    def __init__(self, name, response_cls, method, attribute_name=None):
        self._name = name
        self._response_cls = response_cls
        self._method = method
        self._attribute_name = attribute_name or name
    
    def get_attribute_name(self):
        return self._attribute_name

import copy
import json
import warnings


class ListOf:
    def __init__(self, type):
        self.type = type

    def __call__(self, value):
        return [self.type(v) for v in value]


class Field:
    def __init__(self, type):
        self.type = type

    def __call__(self, value):
        if value is None:
            return None
        return self.type(value)


class DeprecatedField(Field):
    def __init__(self, type, recommendation=None):
        super(DeprecatedField, self).__init__(type)
        self.recommendation = f" {recommendation}" if recommendation else ""

    def __call__(self, value):
        warnings.warn(
            (
                f"This field has been deprecated "
                f"and may be removed in a future version. "
                f"{self.recommendation}"
            ),
            DeprecationWarning,
        )
        return super(DeprecatedField, self).__call__(value)


class BaseApiObject:
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
        j = json.dumps(
            ApiObject.as_json(self._body),
            indent=2,
            sort_keys=True,
            separators=(",", ": "))
        return f"{self.__class__.__name__}({j})"

    def to_json(self):
        return copy.deepcopy(self._body)


class ApiObject(BaseApiObject):
    def __init__(self, body, bound_endpoint=None, retrieve_params=None):
        super(ApiObject, self).__init__()
        object.__setattr__(self, "_body", body)
        object.__setattr__(self, "_bound_endpoint", bound_endpoint)
        object.__setattr__(self, "_retrieve_params", retrieve_params)

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
        else:
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
    valid_id = Field(str)
    suggest_id = Field(str)
    value = Field(float)
    value_detail = Field(str)


class Assignment(ApiObject):
    assign_id = Field(str)
    name = Field(str)
    value = Field(str)


class Assignments(_DictWrapper):
    pass


class Parameter(ApiObject):
    param_id = Field(str)
    prj_id = Field(str)
    name = Field(str)
    type = Field(str)
    max = Field(float)
    min = Field(float)
    value = Field(str)


class Suggestion(ApiObject):
    suggest_id = Field(str)
    project_id = Field(str)
    index = Field(str)
    state = Field(str)
    create_dt = Field(str)
    assignments = Field(Assignments)


class Project(ApiObject):
    project_id = Field(str)
    name = Field(str)
    trial = Field(int)
    parameters = Field(ListOf(Parameter))
    progress = Field(int)


class Token(ApiObject):
    all_experiments = Field(bool)
    client = Field(str)
    development = Field(bool)
    experiment = Field(str)
    permissions = DeprecatedField(str)
    token = Field(str)
    token_type = Field(str)
    user = Field(str)


class ResponseSuggestion():
    def __init__(self, sugt_id):
        self.suggest_id = sugt_id
        self.assignments = {}

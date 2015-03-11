"""
This module contains base for implementing resource classes

"""
import json
from ..exceptions import APIError, AttrError


class Attribute(object):
    """
    This class represents an attribute (default value, etc)

    """

    def __init__(self, name, required=True, default=None):
        self.name = name
        self.required= required
        self.default = default


class JsonObject(object):
    """
    This is a base class to implement jsonifiable objects

    """
    ATTRS = []
    NESTED_RESOURCES = {}
    NESTED_RESOURCE_DICT_KEY_FMT = '{}s_attributes'


    def __init__(self, **kwargs):
        """
        Inititialize the object with kwargs and checks if attributes are allowed

        """
        self.from_dict(**kwargs)


    def from_dict(self, **kwargs):
        """
        Build an object from a dictionary

        """
        self._parse_nested_resources_args(kwargs)
        self._parse_args(kwargs)


    def _parse_nested_resources_args(self, kwargs):
        """
        Parse arguments nested resources arguments from kwargs

        """
        for name, klass in self._get_nested_resources().items():
            setattr(self, name.capitalize(), klass.nest_in(self._pluralize(name), self))
            setattr(self, self._pluralize(name), [])
            if self._pluralize(name) in kwargs:
                getattr(self, self._pluralize(name)).extend([
                    getattr(self, name.capitalize())(**data) for data in kwargs.pop(self._pluralize(name))
                ])


    def _parse_args(self, kwargs):
        """
        Parse arguements and set attributes accordingly

        """
        self.id = kwargs.pop('id', None)
        for attr in self._get_attrs():
            value = kwargs.pop(attr.name, attr.default)
            if value is not None:
                setattr(self, attr.name, value)


    def _pluralize(self, str):
        """
        Pluralize a string

        """
        return str if str[-1] == 's' else str + 's'


    def _unpluralize(self, str):
        """
        Utility to unpluralize a string

        """
        return str[:-1] if str[-1] == 's' else str


    def _get_nested_resources(self):
        """
        Returns the nested resources dict

        """
        return self.NESTED_RESOURCES


    def _get_attrs(self):
        """
        Returns the attributes needed to interact with the object

        """
        return self.ATTRS


    def as_dict(self):
        """
        Return the current object as a dict using self._get_attrs()

        """
        d = {}
        for attr in self._get_attrs():
            value = getattr(self, attr.name, attr.default)
            if value is not None:
                d.update({attr.name: value})
            elif attr.required:
                raise AttrError('Attribute {} is required'.format(attr.name))
        if self.id is not None:
            d['id'] = self.id
        d.update({
            self.NESTED_RESOURCE_DICT_KEY_FMT.format(nested):
                list(map(lambda x: x.as_dict(), getattr(self, self._pluralize(nested), [])))
            for nested in self._get_nested_resources()
        })
        return d



class APIObject(JsonObject):
    """
    A class representing an API resource

    """
    BASE_ROUTE = ''
    ROUTE_SUFFIX = ''
    DICT_KEY = None

    @classmethod
    def get_route(klass, id=None):
        """
        Returns the route to the object for id if specified

        """
        if id is not None:
            return "{}{}/{}{}".format(klass.quanta.site_route, klass.BASE_ROUTE, id, klass.ROUTE_SUFFIX)
        else:
            return "{}{}{}".format(klass.quanta.site_route, klass.BASE_ROUTE, klass.ROUTE_SUFFIX)



class BaseObject(APIObject):
    """
    This is a base class to implement quanta objects

    """

    @classmethod
    def get(klass, id):
        """
        Retrieves a object from quanta API and returns an instance

        """
        r = klass.quanta._get(klass.get_route(id))
        return klass(**r[klass.DICT_KEY])


    @classmethod
    def create(klass, **kwargs):
        """
        Create an object instance and save it to the API

        """
        obj = klass(**kwargs)
        r = klass.quanta._post(klass.get_route(), data={klass.DICT_KEY: obj.as_dict()})
        return klass(**r[klass.DICT_KEY])


    @classmethod
    def list(klass):
        """
        Retrieves and returns a list of hosts

        """
        r = klass.quanta._get(klass.get_route())
        return list(map(lambda data: klass(**data), r[klass.DICT_KEY + 's']))


    @classmethod
    def all(klass, *args, **kwargs):
        """
        Alias for `list`

        """
        return klass.list(*args, **kwargs)


    def update(self, **kwargs):
        r = self.quanta._put(self.get_route(self.id), data={self.DICT_KEY: self.as_dict()})
        self.from_dict(**r[self.DICT_KEY])


    def delete(self):
        r = self.quanta._delete(self.get_route(self.id))
        if hasattr(self, 'id'):
            self.id = None



class NestedObject(JsonObject):
    """
    This class represents a 'nestable' object to include in a top-level resource

    """
    @classmethod
    def nest_in(klass, name, _resource):
        class _NestedObject(klass):
            resource = _resource
            nested_name = name
        return _NestedObject

    @classmethod
    def create(klass, **kwargs):
        getattr(klass.resource, klass.nested_name).append(klass(**kwargs))
        klass.resource.update()


    def delete(self):
        self._destroy = True
        self.resource.update()


    def update(self, **kwargs):
        self.resource.update()



class SingleObject(APIObject):
    """
    This class overload APIObject to provide a way to deal with single objects

    """

    @classmethod
    def get(klass):
        r = klass.quanta._get(klass.get_route())
        return klass(**r[klass.DICT_KEY])

    def update(self, **kwargs):
        try:
            r = self.quanta._put(self.get_route(), data={self.DICT_KEY: self.as_dict()})
            self.from_dict(**r[self.DICT_KEY])
        except APIError as e:
            self.from_dict(self.get(self.id).as_dict())
            raise e
        return self

"""
Module containing objects to interact with Quanta API

"""
import json


def get_obj_class(klass, _quanta, _logger):
    """
    A closure to retrieve a class from a base klass using quanta as an internal
    Quanta object for the newly created class

    """
    class QuantaObj(klass):
        quanta = _quanta
        logger = _logger

    return QuantaObj



class BaseObject:
    """
    This is a base class to implement quanta objects

    """
    ATTRS = []
    BASE_ROUTE = ''
    DICT_KEY = None

    def __init__(self, **kwargs):
        """
        Inititialize the object with kwargs and checks if attributes are allowed

        """
        self.id = kwargs.pop('id', None)
        for k, v in kwargs.items():
            if k in self._get_attrs():
                setattr(self, k, v)

    @classmethod
    def get_route(klass, id=None):
        """
        Returns the route to the object for id if specified

        """
        if id is not None:
            return "{}{}/{}".format(klass.quanta.site_route, klass.BASE_ROUTE, id)
        else:
            return "{}{}".format(klass.quanta.site_route, klass.BASE_ROUTE)


    def _get_attrs(self):
        """
        Returns the attributes needed to interact with the object

        """
        return self.ATTRS


    def as_dict(self):
        """
        Return the current object as a dict using self._get_attrs()

        """
        d = {a: getattr(self, a, None) for a in self._get_attrs()}
        d['id'] = self.id
        return d


    def update(self):
        r = self.quanta._put(self.get_route(self.id), data={self.DICT_KEY: self.as_dict()})


    def delete(self):
        r = self.quanta._delete(self.get_route(self.id))


    @classmethod
    def get(klass, id):
        """
        Retrieves a server from quanta API and returns an instance

        """
        raise NotImplementedError("The get method has not beed implemented yet")
        r = klass.quanta._get(klass.get_route(id))
        data = r[klass.DICT_KEY]
        return klass(**data)


    @classmethod
    def create(klass, **kwargs):
        """
        Create an object instance and save it to the API

        """
        obj = klass(**kwargs)
        r = klass.quanta._post(klass.get_route(), data={klass.DICT_KEY: obj.as_dict()})
        obj.id = r[klass.DICT_KEY].get('id', None)
        return obj


    @classmethod
    def list(klass):
        """
        Retrieves and returns a list of hosts

        """
        raise NotImplementedError("The list method has not beed implemented yet")


class SingleObject(BaseObject):
    """
    This class overload BaseObject to provide a way to deal with single objects

    """
    @classmethod
    def create(klass, **kwargs):
        """
        There is no need to POST the data since there is only one Analytics account

        """
        obj = klass(**kwargs)
        obj.update()
        return obj


class Server(BaseObject):
    """
    This class represents a server object

    """
    BASE_ROUTE = '/servers'
    ATTRS = [
        'name',
        'role',
        'ip',
        'dns',
        'port',
        'enabled',
    ]
    DICT_KEY = 'server'


class Scenario(BaseObject):
    """
    This class represents a scenario object

    """
    BASE_ROUTE = '/scenarios'
    ATTRS = [
        'name',
        'user_agent',
        'main',
        'magento_string',
        'status',
        'cookies',
        'enabled',
    ]

    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(args, kwargs)

    def as_dict(self):
        pass

    def add_step(self, save=True, **kwargs):
        pass

    def delete_step(self, id, save=True):
        pass


class Step:
    def __init__(self, no, name, url, id=None,
                 is_post=False, post_data="",
                 expected_string="",
                 magento_enabled=False,
                 request_timeout=20.0,
                 expected_code=200):
        self.no = no
        self.name = name
        self.url = url
        self.id = id
        self.is_post = is_post
        self.post_data = post_data
        self.expected_string = expected_string
        self.magento_enabled = magento_enabled
        self.request_timeout = request_timeout
        self.expected_code = 200



class Analytics(SingleObject):
    """
    This class maps a Google Analytics account to Quanta API

    """
    BASE_ROUTE = '/analytics'
    DICT_KEY = 'analytics'
    ATTRS = [
    ]



class Monitor(SingleObject):
    """
    This class maps deal with the Monitor settings on the Quanta API

    """
    BASE_ROUTE = '/magento'
    DICT_KEY = 'magento'
    ATTRS = [
        'url',
        'enabled',
    ]

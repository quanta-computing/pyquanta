"""
This module contains classes about Sites in quanta

"""

from .base import Attribute, BaseObject

class Site(BaseObject):
    """
    This class represents a site in Quanta

    """
    BASE_ROUTE = '/sites'
    ATTRS = [
        Attribute('id'),
        Attribute('name'),
        Attribute('role', required=False),
    ]
    DICT_KEY = 'site'

    @classmethod
    def get_route(klass, id=None):
        """
        Returns the route to the object for id if specified

        """
        if id is not None:
            return "{}/{}{}".format(klass.BASE_ROUTE, id, klass.ROUTE_SUFFIX)
        else:
            return "{}{}".format(klass.BASE_ROUTE, klass.ROUTE_SUFFIX)

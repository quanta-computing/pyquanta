"""
This module contains organization and site resources

"""

from .base import Attribute, BaseObject, NestedObject

class OrgSite(NestedObject):
    """
    This class represents a Site in Quanta

    """
    ATTRS = [
        Attribute('id', required=False),
        Attribute('name'),
        Attribute('role', required=False),
    ]


class Organization(BaseObject):
    """
    This class represents an organization

    """
    BASE_ROUTE = '/organizations'
    ATTRS = [
        Attribute('id', required=False),
        Attribute('name'),
        Attribute('role', required=False),
    ]
    NESTED_RESOURCES = {
        'site': OrgSite,
    }
    DICT_KEY = 'organization'


    @classmethod
    def get_route(klass, id=None):
        """
        Returns the route to the object for id if specified

        """
        if id is not None:
            return "{}/{}{}".format(klass.BASE_ROUTE, id, klass.ROUTE_SUFFIX)
        else:
            return "{}{}".format(klass.BASE_ROUTE, klass.ROUTE_SUFFIX)

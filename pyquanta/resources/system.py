"""
This module contains resources about System

"""
from .base import Attribute, BaseObject

class Server(BaseObject):
    """
    This class represents a server object

    """
    BASE_ROUTE = '/system/servers'
    ATTRS = [
        Attribute('name'),
        Attribute('role'),
        Attribute('host'),
        Attribute('port', default=10050),
        Attribute('enabled', default=True),
        Attribute('template', default='passive'),
    ]
    DICT_KEY = 'server'

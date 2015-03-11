"""
This packages contains all the Quanta resources

"""
import json

from .scenario import Scenario
from .system import Server
from .magento import Endpoint
from .analytics import Account
from .organization import Organization
from .site import Site

def get_obj_class(klass, _quanta, _logger):
    """
    A closure to retrieve a class from a base klass using quanta as an internal
    Quanta object for the newly created class

    """
    class QuantaObj(klass):
        quanta = _quanta
        logger = _logger

    return QuantaObj

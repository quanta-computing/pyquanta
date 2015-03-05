"""
This module contains resource about Magento data

"""

from .base import Attribute, SingleObject


class Endpoint(SingleObject):
    """
    This class maps deal with the Monitor settings on the Quanta API

    """
    BASE_ROUTE = '/magento/endpoint'
    DICT_KEY = 'endpoint'
    ATTRS = [
        Attribute('url'),
        Attribute('enabled', default=True)
    ]

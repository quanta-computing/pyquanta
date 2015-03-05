"""
This module contains analytics-related resources

"""

from .base import Attribute, SingleObject


class Account(SingleObject):
    """
    This class maps a Google Analytics account to Quanta API

    """
    BASE_ROUTE = '/analytics/account'
    DICT_KEY = 'analytics'
    ATTRS = [
        Attribute('profile_id'),
        Attribute('enabled', default=True)
    ]

    def delete(self):
        r = self.quanta._delete(self.get_route())

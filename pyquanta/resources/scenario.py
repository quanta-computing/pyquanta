"""
This module contains websc related resources

"""
from .base import Attribute, NestedObject, BaseObject


class Step(NestedObject):
    """
    This class represents a scenario step

    """
    ATTRS = [
        Attribute('id', required=False),
        Attribute('name'),
        Attribute('no'),
        Attribute('magento_enabled', default=False),
        Attribute('url'),
        Attribute('is_post', default=False),
        Attribute('expected_code', default=200),
        Attribute('expected_string', required=False),
        Attribute('post_data', required=False),
        Attribute('request_timeout', default=20),
        Attribute('_destroy', default=False),
    ]


class Scenario(BaseObject):
    """
    This class represents a scenario object

    """

    BASE_ROUTE = '/websc/scenarios'
    NESTED_RESOURCES = {
        'step': Step,
    }
    DICT_KEY = 'scenario'
    ATTRS = [
        Attribute('name'),
        Attribute('main', default=False),
        Attribute('enabled', default=True),
        Attribute('magento_string', required=False),
        Attribute('user_agent', required=False),
        Attribute('cookies', required=False),
        Attribute('status', required=False),
        Attribute('failed_step', required=False),
    ]

"""
This module contains exception classes for pyquanta

"""

class AttrError(Exception):
    """
    An exception class to deal with attribute exceptions

    """
    pass


class APIError(Exception):
    """
    A class to handle API errors

    """
    def __init__(self, error):
        if isinstance(error, dict):
            msg = self._format_error_message(error)
        else:
            msg = error
        super(APIError, self).__init__(msg)


    def _format_error_message(self, error):
        msgs = []
        for type_name, error_type in error.items():
            for field_name, field in error_type.items():
                for err in field:
                    if field_name == 'base':
                        field_name = ''
                    msgs.append('{} {} {}'.format(
                                    type_name.capitalize(),
                                    field_name,
                                    err,
                                ))
        return '; '.join(msgs)

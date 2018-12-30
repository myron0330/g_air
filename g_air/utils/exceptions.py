"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Exceptions utils file.
#   Author: Myron
# **********************************************************************************#
"""
error_wrapper = (lambda code, message: {'code': code, 'data': message, 'msg': message})


def deal_with_exception(func):
    """
    Deal with exception.
    """
    def _decorator(obj, *args, **kwargs):
        try:
            response = func(obj, *args, **kwargs)
        except tuple(Exceptions.error_types()) as error_code:
            response = error_code.args[0]
        except:
            response = error_wrapper(500, 'Exception unknown.'.format(func.func_name))
        return response
    return _decorator


class DataException(Exception):
    """
    Exception in module data.
    """
    pass


class BaseExceptions(object):
    """
    Base exception enumerate.
    """
    @classmethod
    def enumerates(cls):
        """
        all exceptions enumerate.
        """
        return [value for attr, value in cls.__dict__.items()]

    @classmethod
    def error_types(cls):
        """
        all error types enumerate.
        """
        return tuple([
            DataException
        ])


class Exceptions(BaseExceptions):
    """
    Enumerate exceptions.
    """
    INVALID_FIELDS = DataException(error_wrapper(500, 'There exits invalid fields.'))


__all__ = [
    'Exceptions',
]

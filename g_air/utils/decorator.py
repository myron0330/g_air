"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: decorator utils.
#   Author: Myron
# **********************************************************************************#
"""
from datetime import datetime
from functools import wraps


def time_consumption(func):
    """
    Time consumption calculator.

    Args:
        func(function): target function

    Returns:
        function: function decorator
    """
    @wraps(func)
    def _decorator(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print('[Time consumption] [{}]: {}'.format(func.__name__, end_time - start_time))
        return result

    return _decorator

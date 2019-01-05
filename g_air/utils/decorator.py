"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: decorator utils.
#   Author: Myron
# **********************************************************************************#
"""
from datetime import datetime


def time_consumption(func):
    """
    Time consumption calculator.

    Args:
        func(func): function definition

    Returns:
        func: decorator function
    """
    def _decorator(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print('time consumption: {}'.format(end_time - start_time))
        return result

    return _decorator

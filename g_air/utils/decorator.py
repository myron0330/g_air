"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: decorator utils.
#   Author: Myron
# **********************************************************************************#
"""
import inspect
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


def output(func):
    """
    Deal with api output.

    Args:
        func(function): target function

    Returns:
        function: function decorator
    """
    @wraps(func)
    def _decorator(*args, **kwargs):
        frame = func(*args, **kwargs)
        arg_spec = inspect.getfullargspec(func)
        arguments_list = arg_spec.args
        arguments_default = arg_spec.defaults
        arguments = dict(zip(arguments_list[-len(arguments_default):], arguments_default))
        arguments.update(kwargs)
        if args:
            args_arguments = dict(zip(arguments_list[:len(args)], args))
            arguments.update(args_arguments)
        dump_excel = arguments.get('dump_excel', False)
        if dump_excel:
            excel_name = arguments.get('excel_name', '{}.xlsx'.format(func.__name__))
            if excel_name == 'symbol':
                excel_name = '{}.xlsx'.format(arguments['symbol'])
            if excel_name == 'target_date':
                excel_name = '{}.xlsx'.format(arguments['target_date'])
            frame.to_excel(excel_name, encoding='gbk')
        return frame

    return _decorator

"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: decorator utils.
#   Author: Myron
# **********************************************************************************#
"""
import re
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
        panel = func(*args, **kwargs)
        arg_spec = inspect.getfullargspec(func)
        arguments_list = arg_spec.args
        arguments_default = arg_spec.defaults
        arguments = dict(zip(arguments_list[-len(arguments_default):], arguments_default))
        arguments.update(kwargs)
        if args:
            args_arguments = dict(zip(arguments_list[:len(args)], args))
            arguments.update(args_arguments)
        if arguments.get('dump_excel', False):
            excel_name = arguments.get('excel_name', '{}.xlsx'.format(func.__name__))
            if excel_name == 'symbol':
                output_panel = panel.swapaxes(0, 2)
                for symbol in output_panel:
                    excel_name = '{}.xlsx'.format(symbol)
                    output_panel[symbol].T.to_excel(excel_name, encoding='gbk')
            elif excel_name == 'target_date':
                output_panel = panel.swapaxes(0, 1)
                for target_date in output_panel:
                    excel_name = '{}.xlsx'.format(target_date)
                    output_panel[target_date].to_excel(excel_name, encoding='gbk')
            else:
                panel.to_excel(excel_name, encoding='gbk')
        if arguments.get('dump_mysql', False):
            symbol_pattern = re.compile(r'([0-9]+)(\.)([A-Za-z]+)')
            date_pattern = re.compile(r'[0-9\-]+')
            pass
        return panel

    return _decorator

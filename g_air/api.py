"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: main function file.
#   Author: Myron
# **********************************************************************************#
"""
import inspect
import multiprocessing
import numpy as np
import pandas as pd
from functools import wraps
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, as_completed
from .data.database_api import *
from .calculator.factors import *
from .calculator.signals import *
from .const import (
    AVAILABLE_DATA_FIELDS,
    MAX_GLOBAL_PERIODS,
    MAX_SYMBOLS_FRAGMENT
)


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
            elif excel_name == 'indicator':
                output_panel = panel
                for indicator in output_panel:
                    excel_name = '{}.xlsx'.format(indicator)
                    output_panel[indicator].to_excel(excel_name, encoding='gbk')
            else:
                panel.to_excel(excel_name, encoding='gbk')
        if arguments.get('dump_mysql', False):
            symbols_name_map = load_symbols_name_map()
            for indicator in panel:
                frame = panel[indicator]
                frame.index += ' 00:00:00'
                all_items = list()
                for symbol in frame.columns:
                    symbol_name = symbols_name_map.get(symbol, symbol)
                    series = frame.iloc[:, frame.columns.get_loc(symbol)]
                    for _ in series.items():
                        item = [_[0], symbol, symbol_name, _[1]]
                        if np.isnan(item[-1]):
                            print(indicator, item)
                            continue
                        all_items.append(item)
                update_table(indicator.strip('(n)').lower(), all_items)
        return panel

    return _decorator


@output
def calculate_indicators_of_date_slot(symbols=None, target_date=None, data=None, **kwargs):
    """
    Calculate indicators of symbols of a specific target date.

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside
        **kwargs(**dict): key-word arguments, available as follows
            * dump_excel(boolean): whether to export data as excel or not
            * excel_name(string): assign an excel name (as result.xlsx) or 'target_date', 'symbol'
            * dump_mysql(boolean): whether to dump data to mysql database or not

    Returns:
        pandas.Panel: symbol indicators panel, {indicator: {date: {symbol}}}
    """
    assert isinstance(kwargs, dict)
    symbols = symbols or load_all_symbols()
    if data is None:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=MAX_GLOBAL_PERIODS)
        data = load_attributes_data(symbols, trading_days, attributes=AVAILABLE_DATA_FIELDS)
    factor_q = calculate_factor_q(target_date=target_date, data=data)
    factor_m = calculate_factor_m(target_date=target_date, data=data)
    factor_m_offset_20 = calculate_factor_m(target_date=target_date, offset=-20, data=data)
    factor_w = calculate_factor_w(target_date=target_date, data=data)
    factor_w_offset_5 = calculate_factor_w(target_date=target_date, offset=-5, data=data)
    factor_d = calculate_factor_d(target_date=target_date, data=data)
    factor_d_offset_1 = calculate_factor_d(target_date=target_date, offset=-1, data=data)
    factor_close = get_close_price_series(target_date=target_date, data=data)
    factor_close_offset_1 = get_close_price_series(target_date=target_date, offset=-1, data=data)
    factor_close_offset_5 = get_close_price_series(target_date=target_date, offset=-5, data=data)
    factor_close_offset_20 = get_close_price_series(target_date=target_date, offset=-20, data=data)

    signal_m = calculate_signal_m(q_series=factor_q, m_series=factor_m)
    signal_m_offset_20 = calculate_signal_m(symbols=symbols, target_date=target_date, offset=-20, data=data)
    signal_w = calculate_signal_w(m_series=factor_m, w_series=factor_w)
    signal_w_offset_5 = calculate_signal_w(symbols=symbols, target_date=target_date, offset=-5, data=data)
    signal_d = calculate_signal_d(w_series=factor_w, d_series=factor_d)
    signal_d_offset_1 = calculate_signal_d(symbols=symbols, target_date=target_date, offset=-1, data=data)

    signal_m1 = calculate_signal_m1(ms_series=signal_m)
    signal_m2 = calculate_signal_m2(ms_series=signal_m, ms_series_offset_20=signal_m_offset_20)
    signal_m3 = calculate_signal_m3(c_series=factor_close, c_series_offset_20=factor_close_offset_20)
    signal_m4 = calculate_signal_m4(m_series=factor_m, m_series_offset_20=factor_m_offset_20)

    signal_w1 = calculate_signal_w1(ws_series=signal_w)
    signal_w2 = calculate_signal_w2(ws_series=signal_w, ws_series_offset_5=signal_w_offset_5)
    signal_w3 = calculate_signal_w3(c_series=factor_close, c_series_offset_5=factor_close_offset_5)
    signal_w4 = calculate_signal_w4(w_series=factor_w, w_series_offset_5=factor_w_offset_5)

    signal_d1 = calculate_signal_d1(ds_series=signal_d)
    signal_d2 = calculate_signal_d2(ds_series=signal_d, ds_series_offset_1=signal_d_offset_1)
    signal_d3 = calculate_signal_d3(c_series=factor_close, c_series_offset_1=factor_close_offset_1)
    signal_d4 = calculate_signal_d4(d_series=factor_d, d_series_offset_1=factor_d_offset_1)

    signal_m2l = calculate_signal_m2l(m2_series=signal_m2, target_date=target_date, data=data)
    signal_w2l = calculate_signal_w2l(w2_series=signal_w2, target_date=target_date, data=data)
    signal_d2l = calculate_signal_d2l(d2_series=signal_d2, target_date=target_date, data=data)
    signal_m4l = calculate_signal_m4l(m4_series=signal_m4, target_date=target_date, data=data)
    signal_w4l = calculate_signal_w4l(w4_series=signal_w4, target_date=target_date, data=data)
    signal_d4l = calculate_signal_d4l(d4_series=signal_d4, target_date=target_date, data=data)

    signal_m2b = calculate_signal_m2b(m2_series=signal_m2, m3_series=signal_m3)
    signal_w2b = calculate_signal_w2b(w2_series=signal_w2, w3_series=signal_w3)
    signal_d2b = calculate_signal_d2b(d2_series=signal_d2, d3_series=signal_d3)
    signal_m4b = calculate_signal_m4b(m4_series=signal_m4, m3_series=signal_m3)
    signal_w4b = calculate_signal_w4b(w4_series=signal_w4, w3_series=signal_w3)
    signal_d4b = calculate_signal_d4b(d4_series=signal_d4, d3_series=signal_d3)
    signal_j = calculate_signal_j(m2b_series=signal_m2b, w2b_series=signal_w2b, d2b_series=signal_d2b)

    signal_z = calculate_signal_z(target_date=target_date, data=data)
    signal_wz = calculate_signal_wz(target_date=target_date, data=data)
    signal_t = calculate_signal_t(target_date=target_date, data=data)
    signal_zq = calculate_signal_zq(j_series=signal_j, target_date=target_date, data=data)
    indicator_dict = OrderedDict([
        ('Q(n)', factor_q),
        ('M(n)', factor_m),
        ('W(n)', factor_w),
        ('D(n)', factor_d),
        ('Ms(n)', signal_m),
        ('Ws(n)', signal_w),
        ('Ds(n)', signal_d),
        ('M1(n)', signal_m1),
        ('M2(n)', signal_m2),
        ('M3(n)', signal_m3),
        ('M4(n)', signal_m4),
        ('W1(n)', signal_w1),
        ('W2(n)', signal_w2),
        ('W3(n)', signal_w3),
        ('W4(n)', signal_w4),
        ('D1(n)', signal_d1),
        ('D2(n)', signal_d2),
        ('D3(n)', signal_d3),
        ('D4(n)', signal_d4),
        ('J(n)', signal_j),
        ('M2L(n)', signal_m2l),
        ('W2L(n)', signal_w2l),
        ('D2L(n)', signal_d2l),
        ('M4L(n)', signal_m4l),
        ('W4L(n)', signal_w4l),
        ('D4L(n)', signal_d4l),
        ('M2B(n)', signal_m2b),
        ('W2B(n)', signal_w2b),
        ('D2B(n)', signal_d2b),
        ('M4B(n)', signal_m4b),
        ('W4B(n)', signal_w4b),
        ('D4B(n)', signal_d4b),
        ('Z(n)', signal_z),
        ('WZ(n)', signal_wz),
        ('T(n)', signal_t),
        ('ZQ(n)', signal_zq)
    ])
    frame = pd.DataFrame(list(indicator_dict.values()), index=list(indicator_dict.keys()))
    frame = frame.reindex(columns=sorted(frame.columns))
    panel = pd.Panel.from_dict({target_date: frame}).swapaxes(0, 1)
    return panel


@output
def calculate_indicators_of_date_range(symbols=None, target_date_range=None, data=None, **kwargs):
    """
    Calculate indicators of a specific symbol in a target date range.

    Args:
        symbols(string or list): symbol name list
        target_date_range(string): target date, %Y-%m-%d
        data(dict): cached data from outside
        **kwargs(**dict): key-word arguments, available as follows
            * dump_excel(boolean): whether to dump excel or not
            * excel_name(string): assign an excel name (as result.xlsx) or 'target_date', 'symbol'
            * dump_mysql(boolean): whether to dump data to mysql database or not

    Returns:
        pandas.Panel: symbol indicators panel, {indicator: {date: {symbol}}}
    """
    assert isinstance(kwargs, dict)
    symbols = symbols or load_all_symbols()
    symbols = symbols.split(',') if isinstance(symbols, str) else symbols
    if data is None:
        target_date_range = sorted(target_date_range)
        start_date = target_date_range[0]
        history_trading_days = load_trading_days_with_history_periods(
            date=start_date, history_periods=MAX_GLOBAL_PERIODS)
        trading_days = history_trading_days + target_date_range[1:]
        data = load_attributes_data(symbols, trading_days, attributes=AVAILABLE_DATA_FIELDS)

    results = list()
    for target_date in target_date_range:
        results.append(calculate_indicators_of_date_slot(
                symbols=symbols,
                target_date=target_date,
                data=data
            ))
    panel = pd.concat(results, axis=1)
    panel = panel.reindex(major_axis=sorted(panel.major_axis))
    return panel


@output
def calculate_indicators_of_date_slot_concurrently(symbols=None, target_date=None, data=None, **kwargs):
    """
    Calculate indicators of symbols in a specific target date with concurrent processing.

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside
        **kwargs(**dict): key-word arguments, available as follows
            * dump_excel(boolean): whether to dump excel or not
            * excel_name(string): assign an excel name (as result.xlsx) or 'target_date', 'symbol'
            * dump_mysql(boolean): whether to dump data to mysql database or not

    Returns:
        pandas.Panel: symbol indicators panel, {indicator: {date: {symbol}}}
    """
    assert isinstance(kwargs, dict)
    all_symbols = symbols or load_all_symbols()
    symbols_length = len(all_symbols)
    symbol_batch = [all_symbols[index:min(index+MAX_SYMBOLS_FRAGMENT, symbols_length)] for index in range(
        0, symbols_length, MAX_SYMBOLS_FRAGMENT)]
    args_batch = map(lambda x: [x, target_date, data], symbol_batch)
    with ProcessPoolExecutor(multiprocessing.cpu_count()) as pool:
        requests = [pool.submit(calculate_indicators_of_date_slot, *args) for args in args_batch]
        responses = [data.result() for data in as_completed(requests)]
    panel = pd.concat(responses, axis=2)
    panel = panel.reindex(minor_axis=sorted(panel.minor_axis))
    return panel


__all__ = [
    'calculate_indicators_of_date_slot',
    'calculate_indicators_of_date_range',
    'calculate_indicators_of_date_slot_concurrently',
]

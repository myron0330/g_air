"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: main function file.
#   Author: Myron
# **********************************************************************************#
"""
import pandas as pd
from collections import OrderedDict
from .data.database_api import *
from .calculator.factors import *
from .calculator.signals import *
from .const import (
    AVAILABLE_DATA_FIELDS,
    MAX_GLOBAL_PERIODS)


def calculate_indicators(symbols=None, target_date=None, dump=True, data=None):
    """
    Calculate indicators of symbols and target date.

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        dump(boolean): whether to dump to excel and csv files
        data(dict): cached data from outside

    Returns:
        dict: symbol indicators frame
    """
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
    signal_d_offset_1 = calculate_signal_m(symbols=symbols, target_date=target_date, offset=-1, data=data)

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

    signal_z = calculate_signal_z(m2l_series=signal_m2l, m3_series=signal_m3)
    signal_wz = calculate_signal_wz(w2l_series=signal_w2l, w3_series=signal_w3)
    signal_t = calculate_signal_t(m2l_series=signal_m2l, m3_series=signal_m3)
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
    if dump:
        frame.to_csv('result.csv', encoding='gbk')
        frame.to_excel('result.xlsx', encoding='gbk')
    return frame


def calculate_indicators_of_date_range(symbol=None, target_date_range=None, dump=True, data=None):
    """
    Calculate indicators of a specific symbol in a target date range.

    Args:
        symbol(string): symbol name
        target_date_range(string): target date, %Y-%m-%d
        dump(boolean): whether to dump to excel and csv files
        data(dict): cached data from outside

    Returns:
        dict: symbol indicators frame
    """
    if data is None:
        target_date_range = sorted(target_date_range)
        start_date = target_date_range[0]
        history_trading_days = load_trading_days_with_history_periods(
            date=start_date, history_periods=MAX_GLOBAL_PERIODS)
        trading_days = history_trading_days + target_date_range[1:]
        data = load_attributes_data([symbol], trading_days, attributes=AVAILABLE_DATA_FIELDS)

    results = OrderedDict()
    for target_date in target_date_range:
        results[target_date] = calculate_indicators(
                symbols=[symbol],
                target_date=target_date,
                dump=False,
                data=data
            )
    trading_days = results.keys()
    frame = pd.concat(results.values(), axis=1)
    frame.columns = trading_days
    if dump:
        frame.to_csv('result.csv', encoding='gbk')
        frame.to_excel('result.xlsx', encoding='gbk')
    return frame

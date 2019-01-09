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


def calculate_indicators(symbols=None, target_date=None):
    """
    Calculate indicators of symbols and target date.

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d

    Returns:
        dict: symbol indicators
    """
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
    ])

    frame = pd.DataFrame(list(indicator_dict.values()), index=list(indicator_dict.keys()))
    frame.to_csv('result.csv', encoding='gbk')
    pass

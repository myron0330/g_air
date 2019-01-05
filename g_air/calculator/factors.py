"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Factors calculating file.
#   Author: Myron
# **********************************************************************************#
"""
from ..data.database_api import (
    load_trading_days_with_history_periods,
    load_attributes_data
)


def calculate_q(symbols, target_date, data=None):
    """
    Calculate factor Q.

    1) Q = SCDQ(n) + TIQ(n) + CADQ(n)/2 + SCDM(n)/2 + SCDM(n-20)/2 + SCDM(n-40)/2

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside

    Returns:
        dict: {symbol: Q_value}
    """
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date)
        data = load_attributes_data(symbols, trading_days, attributes=['scdq', 'tiq', 'cadq', 'scdm'])
    else:
        trading_days = list(data['scdq'].index)
    target_date_index = trading_days.index(target_date)
    target_date_offset_20 = target_date_index - 20
    target_date_offset_40 = target_date_index - 40
    q_series = (
            data['scdq'].iloc[target_date_index, :] + data['tiq'].iloc[target_date_index, :]
            + data['cadq'].iloc[target_date_index, :] + data['scdm'].iloc[target_date_index, :]
            + data['scdm'].iloc[target_date_offset_20, :] / 2 + data['scdm'].iloc[target_date_offset_40, :] / 2)
    return q_series.to_dict()


def calculate_m(symbols, target_date, data=None):
    """
    Calculate factor M.

    2) M = SCDM(n) + TIM(n) + CADM(n)/2 + SCDW(n)/2 + SCDW(n-5)/2 + SCDW(n-10)/2 + SCDW(n-15)/2

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside

    Returns:
        dict: {symbol: M_value}
    """
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=15)
        data = load_attributes_data(symbols, trading_days, attributes=['scdm', 'tim', 'cadm', 'scdw'])
    else:
        trading_days = list(data['scdm'].index)
    target_date_index = trading_days.index(target_date)
    target_date_offset_5 = target_date_index - 5
    target_date_offset_10 = target_date_index - 10
    target_date_offset_15 = target_date_index - 15
    m_series = (
        data['scdm'].iloc[target_date_index, :] + data['tim'].iloc[target_date_index, :]
        + data['cadm'].iloc[target_date_index, :] / 2 + data['scdw'].iloc[target_date_index, :] / 2
        + data['scdw'].iloc[target_date_offset_5, :] / 2 + data['scdw'].iloc[target_date_offset_10, :] / 2
        + data['scdw'].iloc[target_date_offset_15, :] / 2
    )
    return m_series.to_dict()


def calculate_w(symbols, target_date, data=None):
    """
    Calculate factor W.

    3) W = SCDW(n) + TIW(n) + CADW(n)/2 + SCDD(n)/2 + SCDD(n-1)/2 + SCDD(n-2)/2 + SCDD(n-3)/2 + SCDD(n-4)/2

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside

    Returns:
        dict: {symbol: W_value}
    """
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=4)
        data = load_attributes_data(symbols, trading_days, attributes=['scdw', 'tiw', 'cadw', 'scdd'])
    else:
        trading_days = list(data['scdw'].index)
    target_date_index = trading_days.index(target_date)
    target_date_offset_1 = target_date_index - 1
    target_date_offset_2 = target_date_index - 2
    target_date_offset_3 = target_date_index - 3
    target_date_offset_4 = target_date_index - 4
    w_series = (
        data['scdw'].iloc[target_date_index, :] + data['tiw'].iloc[target_date_index, :]
        + data['cadw'].iloc[target_date_index, :] / 2 + data['scdd'].iloc[target_date_index, :] / 2
        + data['scdd'].iloc[target_date_offset_1, :] / 2 + data['scdd'].iloc[target_date_offset_2, :] / 2
        + data['scdd'].iloc[target_date_offset_3, :] / 2 + data['scdd'].iloc[target_date_offset_4, :] / 2
    )
    return w_series.to_dict()


def calculate_d(symbols, target_date, data=None):
    """
    Calculate factor D.

    4) D = SCDD(n) + TID(n) + CADD(n)/2 + SCDH1(n)/2 + SCDH2(n)/2 + SCDH3(n)/2 + SCDH4(n)/2

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        data(dict): cached data from outside

    Returns:
        dict: {symbol: D_value}
    """
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=0)
        data = load_attributes_data(
            symbols, trading_days, attributes=['scdd', 'tid', 'cadd', 'scdh1', 'scdh2', 'scdh3', 'scdh4'])
    else:
        trading_days = list(data['scdd'].index)
    target_date_index = trading_days.index(target_date)
    d_series = (
        data['scdd'].iloc[target_date_index, :] + data['tid'].iloc[target_date_index, :]
        + data['cadd'].iloc[target_date_index, :] / 2 + data['scdh1'].iloc[target_date_index, :] / 2
        + data['scdh2'].iloc[target_date_index, :] / 2 + data['scdh3'].iloc[target_date_index, :] / 2
        + data['scdh4'].iloc[target_date_index, :] / 2
    )
    return d_series.to_dict()


__all__ = [
    'calculate_q',
    'calculate_m',
    'calculate_w',
    'calculate_d'
]

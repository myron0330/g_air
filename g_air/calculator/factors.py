"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Factors calculating file.
#   Author: Myron
# **********************************************************************************#
"""
from ..data.database_api import (
    load_trading_days_with_history_periods,
    load_offset_trading_day,
    load_attributes_data
)


def calculate_factor_q(symbols=None, target_date=None, offset=0, data=None):
    """
    Calculate factor Q(n).

    1.1) Q(n) = SCDQ(n) + TIQ(n) + CADQ(n)/2 + (SCDM(n) + SCDM(n-20) + SCDM(n-40)) / (3 * 2)

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        offset(int): target date offset
        data(dict): cached data from outside

    Returns:
        Series: factor Q(n) series
    """
    if offset:
        target_date = load_offset_trading_day(target_date, offset)
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
            + data['cadq'].iloc[target_date_index, :] / 2 + data['scdm'].iloc[target_date_index, :] / 6
            + data['scdm'].iloc[target_date_offset_20, :] / 6 + data['scdm'].iloc[target_date_offset_40, :] / 6)
    return q_series


def calculate_factor_m(symbols=None, target_date=None, offset=0, data=None):
    """
    Calculate factor M(n).

    1.2) M(n) = SCDM(n) + TIM(n) + CADM(n)/2 + (SCDW(n) + SCDW(n-5) + SCDW(n-10) + SCDW(n-15)) / (4 * 2)

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        offset(int): target date offset
        data(dict): cached data from outside

    Returns:
        Series: factor M(n) series
    """
    if offset:
        target_date = load_offset_trading_day(target_date, offset)
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
        + data['cadm'].iloc[target_date_index, :] / 2 + data['scdw'].iloc[target_date_index, :] / 8
        + data['scdw'].iloc[target_date_offset_5, :] / 8 + data['scdw'].iloc[target_date_offset_10, :] / 8
        + data['scdw'].iloc[target_date_offset_15, :] / 8
    )
    return m_series


def calculate_factor_w(symbols=None, target_date=None, offset=0, data=None):
    """
    Calculate factor W(n).

    1.3) W(n) = SCDW(n) + TIW(n) + CADW(n)/2 + (SCDD(n) + SCDD(n-1) + SCDD(n-2) + SCDD(n-3) + SCDD(n-4)) / (5 * 2)

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        offset(int): target date offset
        data(dict): cached data from outside

    Returns:
        Series: factor W(n) series
    """
    if offset:
        target_date = load_offset_trading_day(target_date, offset)
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
        + data['cadw'].iloc[target_date_index, :] / 2 + data['scdd'].iloc[target_date_index, :] / 10
        + data['scdd'].iloc[target_date_offset_1, :] / 10 + data['scdd'].iloc[target_date_offset_2, :] / 10
        + data['scdd'].iloc[target_date_offset_3, :] / 10 + data['scdd'].iloc[target_date_offset_4, :] / 10
    )
    return w_series


def calculate_factor_d(symbols=None, target_date=None, offset=0, data=None):
    """
    Calculate factor D(n).

    1.4) D(n) = SCDD(n) + TID(n) + CADD(n)/2 + (SCDH1(n) + SCDH2(n) + SCDH3(n) + SCDH4(n)) / (4 * 2)

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        offset(int): target date offset
        data(dict): cached data from outside

    Returns:
        Series: factor D(n) series
    """
    if offset:
        target_date = load_offset_trading_day(target_date, offset)
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=0)
        data = load_attributes_data(
            symbols, trading_days, attributes=['scdd', 'tid', 'cadd', 'scdh1', 'scdh2', 'scdh3', 'scdh4'])
    else:
        trading_days = list(data['scdd'].index)
    target_date_index = trading_days.index(target_date)
    d_series = (
        data['scdd'].iloc[target_date_index, :] + data['tid'].iloc[target_date_index, :]
        + data['cadd'].iloc[target_date_index, :] / 2 + data['scdh1'].iloc[target_date_index, :] / 8
        + data['scdh2'].iloc[target_date_index, :] / 8 + data['scdh3'].iloc[target_date_index, :] / 8
        + data['scdh4'].iloc[target_date_index, :] / 8
    )
    return d_series


def get_close_price_series(symbols=None, target_date=None, offset=0, data=None):
    """
    Get factor Close(n).

    Args:
        symbols(list): list of symbols
        target_date(string): target date, %Y-%m-%d
        offset(int): target date offset
        data(dict): cached data from outside

    Returns:
        Series: close price series
    """
    if offset:
        target_date = load_offset_trading_day(target_date, offset)
    if not data:
        trading_days = load_trading_days_with_history_periods(date=target_date, history_periods=0)
        data = load_attributes_data(symbols, trading_days, attributes=['adj_close_price'])
    else:
        trading_days = list(data['adj_close_price'].index)
    target_date_index = trading_days.index(target_date)
    c_series = data['adj_close_price'].iloc[target_date_index, :]
    return c_series


__all__ = [
    'calculate_factor_q',
    'calculate_factor_m',
    'calculate_factor_w',
    'calculate_factor_d',
    'get_close_price_series'
]

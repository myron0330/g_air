"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: database loading api.
#   Author: Myron
# **********************************************************************************#
"""
import bisect
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .api_base import (
    get_connection
)
from ..const import (
    AVAILABLE_DATA_FIELDS,
    MAX_THREADS
)
from ..utils.exceptions import Exceptions
from ..utils.datetime import normalize_date
from ..utils.decorator import time_consumption
from ..const import MAX_SINGLE_FACTOR_PERIODS


def load_all_symbols():
    """
    Load all symbols from cadd table.
    """
    with get_connection().cursor() as cursor:
        sql = """select distinct 代码 from price"""
        cursor.execute(sql)
        result = list(map(lambda x: x[0], cursor.fetchall()))
    return result


def load_trading_days(start=None, end=None):
    """
    Load trading days from cadd table.

    Args:
        start(string): start time
        end(string): end time

    Returns:
        list of datetime.datetime: trading days list
    """
    with get_connection().cursor() as cursor:
        sql = """select distinct 日期 from cadd"""
        where_clause = """"""
        if start or end:
            if start and not end:
                where_clause += """日期 >= '{}'""".format(normalize_date(start).strftime('%Y-%m-%d %H:%M:%S'))
            if not start and end:
                where_clause += """日期 <= '{}'""".format(normalize_date(end).strftime('%Y-%m-%d %H:%M:%S'))
            if start and end:
                where_clause += """日期 >= '{}' and 日期 <= '{}'""".format(
                    normalize_date(start).strftime('%Y-%m-%d %H:%M:%S'),
                    normalize_date(end).strftime('%Y-%m-%d %H:%M:%S'))
        if where_clause:
            sql = ' where '.join([sql, where_clause])
        cursor.execute(sql)
        result = sorted(map(lambda x: x[0].split(' ')[0], cursor.fetchall()))
    return result


def load_trading_days_with_history_periods(date, history_periods=MAX_SINGLE_FACTOR_PERIODS):
    """
    Load trading days with history periods.

    Args:
        date(string): date, %Y-%m-%d
        history_periods(int): periods length

    Returns:
        list: list of date
    """
    all_trading_days = load_trading_days()
    index = bisect.bisect_right(all_trading_days, date)
    start_index = max(index - history_periods - 1, 0)
    result = all_trading_days[start_index:index]
    return result


def load_offset_trading_day(date, offset=0, all_trading_days=None):
    """
    Load offset trading day.

    Args:
        date(string): date, %Y-%m-%d
        offset(int): all int,  offset < 0, backward; offset > 0, forward
        all_trading_days(list): all trading days list

    Returns:
        string: target date, %Y-%m-%d
    """
    all_trading_days = all_trading_days or load_trading_days()
    index = all_trading_days.index(date)
    return all_trading_days[min(max(index + offset, 0), len(all_trading_days) - 1)]


def load_attribute(symbols=None, trading_days=None, attribute=None):
    """
    Load attribute data from database.

    Args:
        symbols(list): list of symbols
        trading_days(list): list of string: %Y-%m-%d
        attribute(string): attribute name
    """
    attribute = attribute or AVAILABLE_DATA_FIELDS[0]
    assert attribute in AVAILABLE_DATA_FIELDS, Exceptions.INVALID_FIELDS
    with get_connection().cursor() as cursor:
        attribute_map = {
            'adj_open_price': '复权开盘价',
            'adj_close_price': '复权收盘价'
        }
        table_map = {
            'adj_open_price': 'price',
            'adj_close_price': 'price'
        }
        select_clause = '日期,代码,{}'.format(attribute_map.get(attribute, attribute))
        from_clause = '{}'.format(table_map.get(attribute, attribute))
        sql = """select {} from {}""".format(select_clause, from_clause)
        where_clause = """"""
        symbol_condition = """代码 in {}""".format(tuple(symbols)) if symbols else """"""
        trading_days_str_list = trading_days or list()
        trading_days_condition = """substr(日期, 1, 10) in ({})""".format(
            ','.join(map(lambda x: '\"{}\"'.format(x), trading_days_str_list))) if trading_days_str_list else """"""
        joiner = ' and ' if symbol_condition and trading_days_condition else ''
        if symbol_condition or trading_days_condition:
            where_clause = joiner.join([symbol_condition, trading_days_condition])
        if where_clause:
            sql = ' where '.join([sql, where_clause])
        cursor.execute(sql)
        result = list(cursor.fetchall())
    frame = pd.DataFrame(result, columns=['date', 'symbol', attribute])
    frame['date'] = frame['date'].apply(lambda x: x.split(' ')[0])
    return frame


@time_consumption
def load_attributes_data(symbols=None, trading_days=None, attributes=None):
    """
    Load attribute data from database.

    Args:
        symbols(list): list of symbols
        trading_days(list): list of datetime.datetime
        attributes(list): list of attribute name

    Returns:
        dict: {attribute: DataFrame}
    """
    attributes = attributes or AVAILABLE_DATA_FIELDS
    with ThreadPoolExecutor(MAX_THREADS) as pool:
        requests = [pool.submit(load_attribute, symbols, trading_days, attribute) for attribute in attributes]
        responses = [data.result() for data in as_completed(requests)]
    result = dict()
    if responses:
        all_symbols_set = set()
        for frame in responses:
            attribute = frame.columns[-1]
            result[attribute] = frame.pivot(index='date', columns='symbol', values=attribute).reindex(trading_days)
            all_symbols_set |= set(result[attribute].columns)
        for attribute in result.keys():
            result[attribute] = result[attribute].reindex(columns=list(all_symbols_set))
    return result


__all__ = [
    'load_all_symbols',
    'load_trading_days',
    'load_trading_days_with_history_periods',
    'load_offset_trading_day',
    'load_attribute',
    'load_attributes_data'
]

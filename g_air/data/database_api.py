"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: data loading api.
#   Author: Myron
# **********************************************************************************#
"""
import pandas as pd
from .api_base import (
    ConnectionType,
    get_connection
)
from ..const import AVAILABLE_DATA_FIELDS
from ..utils.exceptions import Exceptions
from ..utils.datetime import normalize_date


def load_(symbols, trading_days, fields=None):
    """
    Load data from database.
    """

    fields = fields or AVAILABLE_DATA_FIELDS
    assert set(fields).issubset(AVAILABLE_DATA_FIELDS), Exceptions.INVALID_FIELDS
    with get_connection().cursor() as cursor:
        sql = """select 日期,代码,简称,cadd from cadd limit 0, 100"""
        cursor.execute(sql)
        result = list(cursor.fetchall())
    frame = pd.DataFrame(result)
    return frame


def load_trading_days(start=None, end=None):
    """
    Load trading days based on price table.

    Args:
        start(string): start time
        end(string): end time
    """
    with get_connection().cursor() as cursor:
        sql = """select distinct 日期 from price"""
        if start or end:
            where_clause = """where """
            if start and not end:
                where_clause += """日期 >= {}""".format(normalize_date(start).strftime('%Y-%m-%d'))
            if not start and end:
                where_clause += """日期 <= {}""".format(normalize_date(end).strftime('%Y-%m-%d'))
            if start and end:
                where_clause += """日期 >= {} and 日期 <= {}""".format(
                    normalize_date(start).strftime('%Y-%m-%d'), normalize_date(end).strftime('%Y-%m-%d'))
            sql = ' '.join([sql, where_clause])
        cursor.execute(sql)
        result = sorted(map(lambda x: normalize_date(x[0]), cursor.fetchall()))
    return result

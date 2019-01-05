"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Test data api.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.data.database_api import (
    load_all_symbols,
    load_trading_days,
    load_attribute,
    load_attributes_data
)


class TestDatabaseAPI(TestCase):

    def test_load_all_symbols(self):
        """
        Test load all symbols.
        """
        data = load_all_symbols()
        assert data

    def test_load_trading_days(self):
        """
        Test load trading days.
        """
        trading_days = load_trading_days()
        trading_days_with_start = load_trading_days(start='20180101')
        trading_days_with_end = load_trading_days(end='20181211')
        trading_days_with_start_and_end = load_trading_days(start='20180101', end='20181211')
        assert trading_days and trading_days_with_start and trading_days_with_end and trading_days_with_start_and_end

    def test_load_attribute(self):
        """
        Test load attribute data.
        """
        symbols = ['000001.SZ', '600000.SH']
        trading_days = load_trading_days(start='20181201', end='20190101')
        attribute = 'scdh1'
        data = load_attribute(symbols, trading_days, attribute=attribute)
        assert data

    def test_load_attributes_list(self):
        """
        Test load attributes list.
        """
        symbols = ['000001.SZ', '600000.SH']
        trading_days = load_trading_days(start='20181201', end='20190101')
        data = load_attributes_data(symbols, trading_days)
        assert data

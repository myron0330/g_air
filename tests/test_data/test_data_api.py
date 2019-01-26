"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Test data api.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.data.database_api import *
from g_air.utils.decorator import time_consumption


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
        trading_days = time_consumption(load_trading_days)()
        trading_days_with_start = load_trading_days(start='20180101')
        trading_days_with_end = load_trading_days(end='20181211')
        trading_days_with_start_and_end = load_trading_days(start='20180101', end='20181211')
        assert trading_days and trading_days_with_start and trading_days_with_end and trading_days_with_start_and_end

    def test_load_trading_days_with_history_periods(self):
        """
        Test load trading days with history periods.
        """
        date = '2018-12-03'
        periods = 10
        data = load_trading_days_with_history_periods(date, periods)
        assert data

    def test_load_offset_trading_day(self):
        """
        Test load offset trading day.
        """
        date = '2018-12-03'
        offset = 0
        print(date, offset, load_offset_trading_day(date, offset))
        offset = 1
        print(date, offset, load_offset_trading_day(date, offset))
        offset = -1
        print(date, offset, load_offset_trading_day(date, offset))

    def test_load_attribute(self):
        """
        Test load attribute data.
        """
        trading_days = load_trading_days(start='20181201', end='20190101')
        attribute = 'scdh1'
        data = time_consumption(load_attribute)(trading_days=trading_days, attribute=attribute)
        assert not data.empty

    def test_load_attributes_list(self):
        """
        Test load attributes list.
        """
        symbols = ['000001.SZ', '600000.SH']
        trading_days = load_trading_days(start='20181201', end='20190101')
        data = load_attributes_data(symbols, trading_days)
        print(data)
        # data_all = load_attributes_data(trading_days=trading_days)
        # assert data

    def test_load_symbols_name_map(self):
        """
        Test load symbols name map.
        """
        symbols_name_map = load_symbols_name_map()
        all_symbols = load_all_symbols()
        self.assertEqual(len(symbols_name_map), len(all_symbols))
        pass

"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: test main file.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.data.database_api import (
    load_all_symbols,
    load_trading_days
)
from g_air.main import (
    calculate_indicators,
    calculate_indicators_of_date_range
)


class TestMain(TestCase):

    def setUp(self):
        """
        initialize set up.
        """
        extended_symbols = load_all_symbols()[:20]
        self.symbols = ['000001.SZ', '600000.SH'] + list(set(extended_symbols) - {'000001.SZ', '600000.SH'})
        self.target_date = '2019-01-04'

    def test_calculate_indicators(self):
        """
        Test calculate indicators.
        """
        data = calculate_indicators(symbols=self.symbols, target_date=self.target_date)
        pass

    def test_calculate_indicators_of_date_range(self):
        """
        Test calculate indicators of date range.
        """
        symbol = '600456.SH'
        target_date_range = load_trading_days(start='2019-01-09', end='2019-01-15')
        data = calculate_indicators_of_date_range(
            symbol=symbol, target_date_range=target_date_range)
        pass

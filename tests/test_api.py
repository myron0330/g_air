"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: test main file.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from datetime import datetime
from g_air.data.database_api import (
    load_all_symbols,
    load_trading_days
)
from g_air.api import (
    calculate_indicators_of_date_slot,
    calculate_indicators_of_date_range,
    calculate_indicators_of_date_slot_concurrently
)


class TestMain(TestCase):

    def setUp(self):
        """
        initialize set up.
        """
        self.symbols = ['600456.SH']
        self.target_date = '2019-01-14'

    def test_calculate_indicators(self):
        """
        Test calculate indicators.
        """
        extended_symbols = load_all_symbols()[:5]
        data = calculate_indicators_of_date_slot(
            symbols=extended_symbols,
            target_date=self.target_date,
            dump_excel=True,
            excel_name='target_date'
        )
        print(data)
        pass

    def test_calculate_indicators_of_date_range(self):
        """
        Test calculate indicators of date range.
        """
        # symbol = '600456.SH'
        # symbol = '603043.SH'
        symbol = '002352.SZ'
        target_date_range = load_trading_days(start='2018-12-07', end='2018-12-14')
        data = calculate_indicators_of_date_range(
            symbol=symbol,
            target_date_range=target_date_range,
            dump_excel=True,
            excel_name='symbol'
        )
        pass

    def test_calculate_indicators_of_date_slot(self):
        """
        Test calculate indicators of date slot.
        """
        extended_symbols = load_all_symbols()
        start_time = datetime.now()
        data_concurrent = calculate_indicators_of_date_slot_concurrently(symbols=extended_symbols, target_date=self.target_date)
        end_time = datetime.now()
        print('load concurrently: {}'.format(end_time - start_time))
        start_time = datetime.now()
        data_directly = calculate_indicators_of_date_slot(symbols=extended_symbols, target_date=self.target_date)
        end_time = datetime.now()
        print('load directly: {}'.format(end_time - start_time))

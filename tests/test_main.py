"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: test main file.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.data.database_api import load_all_symbols
from g_air.main import calculate_indicators


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

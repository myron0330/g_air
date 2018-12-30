"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Test data api.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.data.database_api import (
    load_,
    load_trading_days
)


class TestDatabaseAPI(TestCase):

    def test_load_factor_data(self):
        data = load_(None, None)
        pass

    def test_load_trading_days(self):
        """
        Test load trading days.
        """
        trading_days = load_trading_days()
        trading_days_with_start = load_trading_days(start='20180101')
        pass

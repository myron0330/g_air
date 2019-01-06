"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Test factor calculator.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.calculator.factors import *


class TestFactors(TestCase):

    def setUp(self):
        """
        initialize set up.
        """
        self.symbols = ['000001.SZ', '600000.SH']
        self.target_date = '2019-01-04'

    def test_calculate_q(self):
        """
        Test calculate Q.
        """
        data = calculate_factor_q(self.symbols, self.target_date)
        print(data)

    def test_calculate_m(self):
        """
        Test calculate M.
        """
        data = calculate_factor_m(self.symbols, self.target_date)
        print(data)

    def test_calculate_w(self):
        """
        Test calculate W.
        """
        data = calculate_factor_w(self.symbols, self.target_date)
        print(data)

    def test_calculate_d(self):
        """
        Test calculate D.
        """
        data = calculate_factor_d(self.symbols, self.target_date)
        print(data)

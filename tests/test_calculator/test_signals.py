"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Test signal calculator.
#   Author: Myron
# **********************************************************************************#
"""
from unittest import TestCase
from g_air.calculator.factors import *
from g_air.calculator.signals import *


class TestSignals(TestCase):

    def setUp(self):
        """
        initialize set up.
        """
        self.symbols = ['000001.SZ', '600000.SH']
        self.target_date = '2019-01-04'
        self.factor_q = calculate_factor_q(self.symbols, self.target_date)
        self.factor_m = calculate_factor_m(self.symbols, self.target_date)
        self.factor_m_offset_20 = calculate_factor_m(self.symbols, self.target_date, offset=-20)
        self.factor_w = calculate_factor_w(self.symbols, self.target_date)
        self.factor_w_offset_5 = calculate_factor_w(self.symbols, self.target_date, offset=-5)
        self.factor_d = calculate_factor_d(self.symbols, self.target_date)
        self.factor_d_offset_1 = calculate_factor_d(self.symbols, self.target_date, offset=-1)
        self.factor_close = get_close_price_series(self.symbols, self.target_date)
        self.factor_close_offset_1 = get_close_price_series(self.symbols, self.target_date, offset=-1)
        self.factor_close_offset_5 = get_close_price_series(self.symbols, self.target_date, offset=-5)
        self.factor_close_offset_20 = get_close_price_series(self.symbols, self.target_date, offset=-20)
        self.signal_m = calculate_signal_m(self.factor_q, self.factor_m)
        self.signal_w = calculate_signal_w(self.factor_m, self.factor_w)
        self.signal_d = calculate_signal_d(self.factor_w, self.factor_d)
        self.signal_m_offset_20 = calculate_signal_m(symbols=self.symbols,
                                                     target_date=self.target_date,
                                                     offset=-20)
        self.signal_w_offset_5 = calculate_signal_w(symbols=self.symbols,
                                                    target_date=self.target_date,
                                                    offset=-5)
        self.signal_d_offset_1 = calculate_signal_d(symbols=self.symbols,
                                                    target_date=self.target_date,
                                                    offset=-1)

    def test_calculate_m1(self):
        """
        Test calculate m1.
        """
        signal_m1 = calculate_signal_m1(self.signal_m)
        print(self.signal_m)
        print(signal_m1)
        signal_m1_cal = calculate_signal_m1(symbols=self.symbols, target_date=self.target_date)
        print(signal_m1_cal)

    def test_calculate_m2(self):
        """
        Test calculate m2.
        """
        signal_m2 = calculate_signal_m2(ms_series=self.signal_m, ms_series_offset_20=self.signal_m_offset_20)
        print(signal_m2)
        signal_m2_cal = calculate_signal_m2(symbols=self.symbols, target_date=self.target_date)
        print(signal_m2_cal)

    def test_calculate_m3(self):
        """
        Test calculate m3.
        """
        signal_m3 = calculate_signal_m3(c_series=self.factor_close,
                                        c_series_offset_20=self.factor_close_offset_20)
        print(signal_m3)
        signal_m3_cal = calculate_signal_m3(symbols=self.symbols, target_date=self.target_date)
        print(signal_m3_cal)

    def test_calculate_m4(self):
        """
        Test calculate m4.
        """
        signal_m4 = calculate_signal_m4(m_series=self.factor_m,
                                        m_series_offset_20=self.factor_m_offset_20)
        print(signal_m4)
        signal_m4_cal = calculate_signal_m4(symbols=self.symbols, target_date=self.target_date)
        print(signal_m4_cal)

    def test_calculate_w1(self):
        """
        Test calculate w1.
        """
        signal_w1 = calculate_signal_w1(self.signal_w)
        print(self.signal_w)
        print(signal_w1)
        signal_w1_cal = calculate_signal_w1(symbols=self.symbols, target_date=self.target_date)
        print(signal_w1_cal)

    def test_calculate_w2(self):
        """
        Test calculate w2.
        """
        signal_w2 = calculate_signal_w2(ws_series=self.signal_w, ws_series_offset_5=self.signal_w_offset_5)
        print(signal_w2)
        signal_w2_cal = calculate_signal_w2(symbols=self.symbols, target_date=self.target_date)
        print(signal_w2_cal)

    def test_calculate_w3(self):
        """
        Test calculate w3.
        """
        signal_w3 = calculate_signal_w3(c_series=self.factor_close,
                                        c_series_offset_5=self.factor_close_offset_5)
        print(signal_w3)
        signal_w3_cal = calculate_signal_w3(symbols=self.symbols, target_date=self.target_date)
        print(signal_w3_cal)

    def test_calculate_w4(self):
        """
        Test calculate w4.
        """
        signal_w4 = calculate_signal_w4(w_series=self.factor_w,
                                        w_series_offset_5=self.factor_w_offset_5)
        print(signal_w4)
        signal_w4_cal = calculate_signal_w4(symbols=self.symbols, target_date=self.target_date)
        print(signal_w4_cal)

    def test_calculate_d1(self):
        """
        Test calculate d1.
        """
        signal_d1 = calculate_signal_d1(self.signal_d)
        print(self.signal_d)
        print(signal_d1)
        signal_d1_cal = calculate_signal_d1(symbols=self.symbols, target_date=self.target_date)
        print(signal_d1_cal)

    def test_calculate_d2(self):
        """
        Test calculate d2.
        """
        signal_d2 = calculate_signal_d2(ds_series=self.signal_d, ds_series_offset_1=self.signal_d_offset_1)
        print(signal_d2)
        signal_d2_cal = calculate_signal_d2(symbols=self.symbols, target_date=self.target_date)
        print(signal_d2_cal)

    def test_calculate_d3(self):
        """
        Test calculate d3.
        """
        signal_d3 = calculate_signal_d3(c_series=self.factor_close,
                                        c_series_offset_1=self.factor_close_offset_1)
        print(signal_d3)
        signal_d3_cal = calculate_signal_d3(symbols=self.symbols, target_date=self.target_date)
        print(signal_d3_cal)

    def test_calculate_d4(self):
        """
        Test calculate d4.
        """
        signal_d4 = calculate_signal_d4(d_series=self.factor_d,
                                        d_series_offset_1=self.factor_d_offset_1)
        print(signal_d4)
        signal_d4_cal = calculate_signal_d4(symbols=self.symbols, target_date=self.target_date)
        print(signal_d4_cal)

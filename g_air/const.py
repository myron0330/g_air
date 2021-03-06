"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: CONSTANT file.
#   Author: Myron
# **********************************************************************************#
"""


AVAILABLE_DATA_FIELDS = [
    'cadd', 'cadw', 'cadm', 'cadq', 'scdh1', 'scdh2', 'scdh3', 'scdh4', 'scdd', 'scdw', 'scdm', 'scdq',
    'tid', 'tiw', 'tim', 'tiq', 'adj_open_price', 'adj_close_price']
OUTPUT_FIELDS = ['M2B(n)', 'W2B(n)', 'D2B(n)', 'Z(n)', 'WZ(n)', 'T(n)', 'ZQ(n)']
MAX_THREADS = 5
MAX_SINGLE_FACTOR_PERIODS = 40
MAX_GLOBAL_PERIODS = 80
MAX_SYMBOLS_FRAGMENT = 200

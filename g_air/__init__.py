"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: project initialization.
#   Author: Myron
# **********************************************************************************#
"""
import os
# import configparser
#
current_path = os.path.abspath(os.path.dirname(__file__))
# global_configs = configparser.ConfigParser()
# global_configs.read('{}/../etc/g_air.cfg'.format(current_path))
# pass

global_configs = {
    'mysql_source': {
        'host': 'rm-8vbx04w1r5l54f29neo.mysql.zhangbei.rds.aliyuncs.com',
        'port': '3306',
        'user': 'dkhl_zd',
        'password': '!@zd200668',
        'database': 'factor_data_2'},
    'mysql_target': {
        'host': 'rm-8vbx04w1r5l54f29neo.mysql.zhangbei.rds.aliyuncs.com',
        'port': '3306',
        'user': 'guset',
        'password': '4AE6AyNF',
        'database': 'factor_calculation_results'}
}

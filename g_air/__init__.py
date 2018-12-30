"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: project initialization.
#   Author: Myron
# **********************************************************************************#
"""
import os
import configparser

current_path = os.path.abspath(os.path.dirname(__file__))
global_configs = configparser.ConfigParser()
global_configs.read('{}/../etc/g_air.cfg'.format(current_path))

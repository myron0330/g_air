"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: setup.py file.
#   Author: Myron
# **********************************************************************************#
"""
from setuptools import setup, find_packages


setup(name='g_air',
      version='1.0',
      description='Python library for ground_air Co.Ltd,',
      author='Myron',
      author_email='zhainandb@sina.com',
      url='https://www.python.org/sigs/distutils-sig/',
      install_requires=[
            'numpy',
            'pandas',
            'pymysql'
      ],
      packages=find_packages())

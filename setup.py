"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: setup.py file.
#   Author: Myron
# **********************************************************************************#
"""
import os
import site
import platform
from setuptools import setup, find_packages

if platform.system() == "Linux":
    package_path = site.getsitepackages()[0]
else:
    package_path = site.getsitepackages()[1]
data_files = [(os.path.join(package_path, 'g_air/resource'), list())]

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
      data_files=data_files,
      packages=find_packages())

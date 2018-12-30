"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: datetime utils.
#   Author: Myron
# **********************************************************************************#
"""
import pandas as pd
from datetime import datetime


def normalize_date(date):
    """
    Normalize date input to datetime.date.

    Args:
        date(string or datetime.datetime): some specific date.

    Returns:
        datetime.datetime: instance.
    """
    date = pd.Timestamp(date)
    return datetime(date.year, date.month, date.day)

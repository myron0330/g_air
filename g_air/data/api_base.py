"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: API config file.
#   Author: Myron
# **********************************************************************************#
"""
import pymysql
from .. import global_configs


class ConnectionType(object):
    """
    Connection types.
    """
    SOURCE = 'mysql_source'
    TARGET = 'mysql_target'


def get_connection(connection_type=ConnectionType.SOURCE):
    """
    Get connection by connection type.

    Args:
        connection_type(string): connection type.

    Returns:
        Connection: instance.
    """
    configs = dict(global_configs[connection_type])
    configs['port'] = int(configs['port'])
    connection = pymysql.connect(**configs)
    return connection

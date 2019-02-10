"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
#   Author: Myron
# **********************************************************************************#
"""
from datetime import datetime
from PyQt5.QtWidgets import QPlainTextEdit


class GUILogger(object):
    """
    logger.
    """

    def __init__(self, parent):
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def output(self, message, prefix=''):
        """
        Output q logger.

        Args:
            message(string): raw input message.
            prefix(string): message prefix.
        """
        message = self.format(message, prefix=prefix)
        self.widget.appendPlainText(message)

    def clear(self):
        """
        Clear.
        """
        self.widget.clear()

    @staticmethod
    def format(message, prefix=''):
        """
        Format message.

        Args:
            message(string): raw input message.
            prefix(string): message prefix.

        Returns:
            string: formatted message
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return '[{}] {}\n{}\n'.format(current_time, prefix, message)

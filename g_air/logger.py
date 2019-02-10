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

    def output(self, message):
        """
        Output q logger.

        Args:
            message(string): raw input message.
        """
        message = self.format(message)
        self.widget.appendPlainText(message)

    def clear(self):
        """
        Clear.
        """
        self.widget.clear()

    @staticmethod
    def format(message):
        """
        Format message.

        Args:
            message(string): raw input message.

        Returns:
            string: formatted message
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return '[{}]\n{}\n'.format(current_time, message)

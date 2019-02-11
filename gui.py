"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: GUI file.
#   Author: Myron
# **********************************************************************************#
"""
import os
import traceback
from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QDateEdit, QGridLayout, QGroupBox, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QStyleFactory, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget, QDialog, QLineEdit)
from g_air.data.database_api import *
from g_air.api import calculate_indicators_of_date_range
from g_air.logger import GUILogger
from g_air.const import OUTPUT_FIELDS


TIME_FORMAT = 'yyyy-MM-dd'
ALL_SYMBOLS = 'All'
HS300 = 'HS300'
ZZ500 = 'ZZ500'
current_path = os.path.abspath(os.path.dirname(__file__))


class GAirGUI(QWidget):
    """
    G_Air gui.
    """
    def __init__(self, parent=None):
        super(GAirGUI, self).__init__(parent)
        self.start_date_edit = QDateEdit()
        self.end_date_edit = QDateEdit()
        self.symbols_edit = QTextEdit()
        self.full_stock_check_box = QCheckBox(ALL_SYMBOLS)
        self.hs300_check_box = QCheckBox(HS300)
        self.zz500_check_box = QCheckBox(ZZ500)
        self.symbols_widget = QTabWidget()
        self.download_path_edit = QLineEdit()
        self.log_widget = QDialog()
        self.logger = GUILogger(self.log_widget)

        self.input_box = QGroupBox('INPUT')
        self.function_key_box = QGroupBox('FUNCTION KEYS')
        self.log_box = QGroupBox('CONSOLE')
        self.create_input_box()
        self.create_function_key_box()
        self.create_log_box()

        home_layout = QGridLayout()
        home_layout.addWidget(self.input_box, 1, 0, 1, 1)
        home_layout.addWidget(self.function_key_box, 2, 0, 1, 1)
        home_layout.addWidget(self.log_box, 1, 1, 2, 1)
        home_layout.setRowStretch(1, 1)
        home_layout.setRowStretch(2, 1)
        home_layout.setColumnStretch(0, 1)
        home_layout.setColumnStretch(1, 1)
        self.setLayout(home_layout)

        self.setWindowTitle('G_Air Signal Widget')
        self.change_style()
        self.setGeometry(400, 400, 300, 260)
        self.resize(800, 800)

    @property
    def start_date(self):
        """
        Start date.
        """
        return self.start_date_edit.date().toString(TIME_FORMAT)

    @property
    def end_date(self):
        """
        End date.
        """
        return self.end_date_edit.date().toString(TIME_FORMAT)

    @property
    def symbols(self):
        """
        Symbols.
        """
        text = self.symbols_edit.document().toPlainText()
        all_is_checked = self.full_stock_check_box.isChecked()
        hs300_is_checked = self.hs300_check_box.isChecked()
        zz500_is_checked = self.zz500_check_box.isChecked()

        if self.symbols_edit.isEnabled():
            return list(filter(lambda x: x is not '', map(lambda x: x.strip(), text.split(','))))
        else:
            if all_is_checked:
                return None
            symbols = list()
            if hs300_is_checked:
                symbols.extend(load_hs300())
            if zz500_is_checked:
                symbols.extend(load_zz500())
            return symbols

    @property
    def download_path(self):
        """
        Download path.
        """
        return self.download_path_edit.text()

    @staticmethod
    def change_style(style_name='Fusion'):
        """
        Change style of GUI.

        Args:
            style_name(string): style name, could be:
                1). Fusion, Windows, WindowsVista for windows only
                2). Macintosh for mac only
        """
        QApplication.setStyle(QStyleFactory.create(style_name))
        QApplication.setPalette(QApplication.style().standardPalette())

    def create_input_box(self):
        """
        Create input box.
        """
        input_layout = QGridLayout()
        start_date_label = QLabel('Start Date')
        self.start_date_edit = self._initialize_date_edit_widget(self.start_date_edit)
        input_layout.addWidget(start_date_label, 0, 0, 1, 1)
        input_layout.addWidget(self.start_date_edit, 0, 1, 1, 2)
        input_layout.addWidget(QLabel(), 0, 3, 1, 3)

        end_date_label = QLabel('End Date')
        self.end_date_edit = self._initialize_date_edit_widget(self.end_date_edit, date_type='end')
        input_layout.addWidget(end_date_label, 1, 0, 1, 1)
        input_layout.addWidget(self.end_date_edit, 1, 1, 1, 2)
        input_layout.addWidget(QLabel(), 1, 3, 1, 3)

        symbols_label = QLabel('Symbols')
        self._initialize_symbols_edit_widget()
        input_layout.addWidget(symbols_label, 2, 0, 1, 1)
        input_layout.addWidget(self.symbols_widget)

        self.input_box.setLayout(input_layout)

    def create_function_key_box(self):
        """
        Create function key box.
        """
        database_box = QGroupBox('DataBase')
        database_layout = QVBoxLayout()
        database_update_button = QPushButton('Update')
        database_update_button.setDefault(True)
        database_update_button.clicked.connect(self._event_update_database)
        database_delete_button = QPushButton('Delete')
        database_delete_button.setDefault(True)
        database_delete_button.clicked.connect(self._event_delete_database)
        database_layout.addWidget(database_update_button)
        database_layout.addWidget(database_delete_button)
        database_box.setLayout(database_layout)

        console_output_box = QGroupBox('Console')
        console_output_layout = QVBoxLayout()
        console_output_button = QPushButton('Output')
        console_output_button.setDefault(True)
        console_output_button.clicked.connect(self._event_console_output)
        console_output_layout.addWidget(console_output_button)
        console_output_box.setLayout(console_output_layout)

        local_files_box = QGroupBox('Local files')
        local_files_layout = QVBoxLayout()
        local_files_download_button = QPushButton('Download')
        local_files_download_button.setDefault(True)
        local_files_download_button.clicked.connect(self._event_download)
        download_path_label = QLabel('Target path')
        self.download_path_edit.setText(current_path)
        local_files_layout.addWidget(download_path_label)
        local_files_layout.addWidget(self.download_path_edit)
        local_files_layout.addWidget(local_files_download_button)
        local_files_box.setLayout(local_files_layout)

        layout = QVBoxLayout()
        layout.addWidget(database_box)
        layout.addWidget(console_output_box)
        layout.addWidget(local_files_box)
        self.function_key_box.setLayout(layout)

    def create_log_box(self):
        """
        Create log box.
        """
        log_edit_widget = QWidget()
        log_edit_layout = QVBoxLayout()
        log_edit_layout.setContentsMargins(5, 5, 10, 5)
        clear_button = QPushButton('Clear')
        clear_button.setDefault(True)
        clear_button.clicked.connect(self._event_clear_log)
        log_edit_layout.addWidget(clear_button)
        log_edit_layout.addWidget(self.logger.widget)
        log_edit_widget.setLayout(log_edit_layout)
        self.log_box.setLayout(log_edit_layout)

    def _initialize_symbols_edit_widget(self):
        """
        Initialize symbols edit widget.
        """
        self.symbols_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        symbols_edit = QWidget()
        self.symbols_edit.setPlainText('000001.SZ, 600000.SH')
        self.symbols_edit.textChanged.connect(self._event_toggled)

        self.full_stock_check_box.toggled.connect(self._event_toggled)
        self.hs300_check_box.toggled.connect(self._event_toggled)
        self.zz500_check_box.toggled.connect(self._event_toggled)

        symbols_edit_layout = QGridLayout()
        symbols_edit_layout.setContentsMargins(5, 5, 5, 5)
        symbols_edit_layout.addWidget(self.full_stock_check_box, 0, 0, 1, 1)
        symbols_edit_layout.addWidget(self.hs300_check_box, 0, 1, 1, 1)
        symbols_edit_layout.addWidget(self.zz500_check_box, 0, 2, 1, 1)
        symbols_edit_layout.addWidget(self.symbols_edit, 1, 0, 4, 5)
        symbols_edit.setLayout(symbols_edit_layout)
        self.symbols_widget.addTab(symbols_edit, 'Edit Text')

    def _initialize_date_edit_widget(self, date_edit, date_type='start'):
        """
        Create date edit widget.

        Args:
            date_edit(QDateEdit): date edit instance

        Returns:
            QDateEdit: initialized date edit instance
        """
        date_edit.setDisplayFormat(TIME_FORMAT)
        date_edit.setDate(QDate.fromString(datetime.today().strftime('%Y-%m-%d'), TIME_FORMAT))
        if date_type == 'start':
            date_edit.dateChanged.connect(self._event_start_date_changed)
        else:
            date_edit.dateChanged.connect(self._event_end_date_changed)
        return date_edit

    def _event_start_date_changed(self):
        """
        Start Date changed.
        """
        if self.start_date > self.end_date:
            self.end_date_edit.setDate(self.start_date_edit.date())

    def _event_end_date_changed(self):
        """
        End Date changed.
        """
        if self.start_date > self.end_date:
            self.start_date_edit.setDate(self.end_date_edit.date())

    def _event_toggled(self):
        """
        Symbols changed.
        """
        all_is_checked = self.full_stock_check_box.isChecked()
        hs300_is_checked = self.hs300_check_box.isChecked()
        zz500_is_checked = self.zz500_check_box.isChecked()
        if all_is_checked or hs300_is_checked or zz500_is_checked:
            self.symbols_edit.setDisabled(True)
        else:
            self.symbols_edit.setDisabled(False)

    def _event_update_database(self):
        """
        Update database.
        """
        prefix = '[Update]'
        try:
            target_date_range = load_trading_days(start=self.start_date, end=self.end_date)
        except:
            self.logger.output('{}'.format('Loading trading days failed.'), prefix=prefix)
            self.logger.output(traceback.format_exc())
            return

        if target_date_range:
            try:
                calculate_indicators_of_date_range(
                    symbols=self.symbols,
                    target_date_range=target_date_range,
                    dump_mysql=True)
                self.logger.output('Database update successfully.', prefix=prefix)
            except:
                self.logger.output('Database update failed.', prefix=prefix)
                self.logger.output(traceback.format_exc())
        else:
            self.logger.output('No valid target dates.', prefix=prefix)

    def _event_delete_database(self):
        """
        Delete database items.
        """
        prefix = '[Delete]'
        try:
            delete_items_(self.start_date, self.end_date, symbols=self.symbols)
            self.logger.output('Database delete successfully.', prefix=prefix)
        except:
            self.logger.output('Database delete failed.', prefix=prefix)

    def _event_console_output(self):
        """
        Console output result.
        """
        prefix = '[Console output]'

        try:
            target_date_range = load_trading_days(start=self.start_date, end=self.end_date)
        except:
            self.logger.output('{}'.format('Loading trading days failed.', prefix=prefix))
            self.logger.output(traceback.format_exc())
            return

        if target_date_range:
            try:
                result = list()
                panel = calculate_indicators_of_date_range(
                    symbols=self.symbols,
                    target_date_range=target_date_range)
                for indicator in panel:
                    if indicator not in OUTPUT_FIELDS:
                        continue
                    result.append('{}'.format(indicator))
                    result.append(panel[indicator].__str__())
                    result.append('\n')
                self.logger.output('{}'.format('\n'.join(result)), prefix=prefix)
            except:
                self.logger.output('Console output failed.', prefix=prefix)
                self.logger.output(traceback.format_exc())
        else:
            self.logger.output('No valid target dates.', prefix=prefix)

    def _event_download(self):
        """
        Download local files.
        """
        prefix = '[Download]'

        try:
            target_date_range = load_trading_days(start=self.start_date, end=self.end_date)
        except:
            self.logger.output('{}'.format('Loading trading days failed.', prefix=prefix))
            self.logger.output(traceback.format_exc())
            return

        if target_date_range:
            try:
                calculate_indicators_of_date_range(
                    symbols=self.symbols,
                    target_date_range=target_date_range,
                    dump_excel=True,
                    excel_name='symbol',
                    current_path=self.download_path,
                )
                self.logger.output('Download local files successfully.', prefix=prefix)
            except:
                self.logger.output('Download local files failed.', prefix=prefix)
                self.logger.output(traceback.format_exc())
        else:
            self.logger.output('No valid target dates.', prefix=prefix)

    def _event_clear_log(self):
        """
        Clear log output.
        """
        self.logger.clear()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = GAirGUI()
    gallery.show()
    sys.exit(app.exec_())

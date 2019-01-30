"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: GUI file.
#   Author: Myron
# **********************************************************************************#
"""
from datetime import datetime
from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateTimeEdit, QCalendarWidget, QDateEdit,
    QDial, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)


TIME_FORMAT = 'yyyy-MM-dd'


class GAirGUI(QWidget):
    """
    G_Air gui.
    """
    def __init__(self, parent=None):
        super(GAirGUI, self).__init__(parent)
        self.start_date_edit = QDateEdit()
        self.end_date_edit = QDateEdit()
        self.symbols_edit = QTabWidget()
        self.progress_bar = QProgressBar()

        self.input_box = QGroupBox('INPUT')
        self.function_key_box = QGroupBox('FUNCTION KEYS')

        self.create_input_box()
        self.create_function_key_box()
        self.create_progress_bar()

        home_layout = QGridLayout()
        home_layout.addWidget(self.input_box, 1, 0, 1, 1)
        home_layout.addWidget(self.function_key_box, 2, 0, 1, 1)
        home_layout.addWidget(self.progress_bar, 3, 0, 1, 1)
        home_layout.setRowStretch(1, 1)
        home_layout.setRowStretch(2, 1)
        home_layout.setColumnStretch(0, 1)
        home_layout.setColumnStretch(1, 1)
        self.setLayout(home_layout)

        self.setWindowTitle('G_Air Signal Widget')
        self.change_style()
        self.setGeometry(400, 400, 300, 260)
        self.resize(800, 800)

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
        self.end_date_edit = self._initialize_date_edit_widget(self.end_date_edit)
        input_layout.addWidget(end_date_label, 1, 0, 1, 1)
        input_layout.addWidget(self.end_date_edit, 1, 1, 1, 2)
        input_layout.addWidget(QLabel(), 1, 3, 1, 3)

        symbols_label = QLabel('Symbols')
        self._initialize_symbols_edit_widget()
        input_layout.addWidget(symbols_label, 2, 0, 1, 1)
        input_layout.addWidget(self.symbols_edit)

        self.input_box.setLayout(input_layout)

    def create_function_key_box(self):
        """
        Create function key box.
        """
        database_box = QGroupBox('DataBase')
        database_layout = QVBoxLayout()
        database_update_button = QPushButton('Update')
        database_update_button.setDefault(True)
        database_remove_button = QPushButton('Remove')
        database_remove_button.setDefault(True)
        database_layout.addWidget(database_update_button)
        database_layout.addWidget(database_remove_button)
        database_box.setLayout(database_layout)

        local_files_box = QGroupBox('Local files')
        local_files_layout = QVBoxLayout()
        local_files_console_output_button = QPushButton('Console Output')
        local_files_console_output_button.setDefault(True)
        local_files_download_button = QPushButton('Download')
        local_files_download_button.setDefault(True)
        local_files_layout.addWidget(local_files_console_output_button)
        local_files_layout.addWidget(local_files_download_button)
        local_files_box.setLayout(local_files_layout)

        layout = QVBoxLayout()
        layout.addWidget(database_box)
        layout.addWidget(local_files_box)
        layout.addStretch(1)
        self.function_key_box.setLayout(layout)

    def create_bottom_right_group_box(self):
        """
        Create bottom right group box.
        """
        self.bottom_right_group_box.setCheckable(True)
        self.bottom_right_group_box.setChecked(True)

        line_edit = QLineEdit('s3cRe7')
        line_edit.setEchoMode(QLineEdit.Password)

        spin_box = QSpinBox(self.bottom_right_group_box)
        spin_box.setValue(50)

        date_time_edit = QDateTimeEdit(self.bottom_right_group_box)
        date_time_edit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottom_right_group_box)
        slider.setValue(40)

        scroll_bar = QScrollBar(Qt.Horizontal, self.bottom_right_group_box)
        scroll_bar.setValue(60)

        dial = QDial(self.bottom_right_group_box)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(line_edit, 0, 0, 1, 2)
        layout.addWidget(spin_box, 1, 0, 1, 2)
        layout.addWidget(date_time_edit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scroll_bar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottom_right_group_box.setLayout(layout)

    def create_progress_bar(self):
        """
        Create progress bar.
        """
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10000)
        self.progress_bar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advance_progress_bar)
        timer.start(1000)

    def advance_progress_bar(self):
        """
        Advance progress bar.
        """
        current_value = self.progress_bar.value()
        max_value = self.progress_bar.maximum()
        self.progress_bar.setValue(int(current_value + (max_value - current_value) / 100))

    def _initialize_symbols_edit_widget(self):
        """
        Initialize symbols edit widget.
        """
        self.symbols_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        symbols_edit = QWidget()
        text_edit = QTextEdit()
        text_edit.setPlainText('000001.SH, 600000.SZ')
        symbols_edit_layout = QHBoxLayout()
        symbols_edit_layout.setContentsMargins(5, 5, 5, 5)
        symbols_edit_layout.addWidget(text_edit)
        symbols_edit.setLayout(symbols_edit_layout)
        self.symbols_edit.addTab(symbols_edit, 'Edit Text')

    def _initialize_date_edit_widget(self, date_edit):
        """
        Create date edit widget.

        Args:
            date_edit(QDateEdit): date edit instance

        Returns:
            QDateEdit: initialized date edit instance
        """
        date_edit.setDisplayFormat(TIME_FORMAT)
        date_edit.setDate(QDate.fromString(datetime.today().strftime('%Y-%m-%d'), TIME_FORMAT))
        date_edit.dateChanged.connect(self._event_date_changed)
        return date_edit

    def _event_date_changed(self):
        """
        Date changed event process.
        """
        return


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = GAirGUI()
    gallery.show()
    sys.exit(app.exec_())

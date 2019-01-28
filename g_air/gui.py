"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: GUI file.
#   Author: Myron
# **********************************************************************************#
"""
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateTimeEdit,
    QDial, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)


class GAirGUI(QWidget):

    def __init__(self, parent=None):
        super(GAirGUI, self).__init__(parent)
        combo_box = QComboBox()
        combo_box.addItems(QStyleFactory.keys())

        style_label = QLabel("&Style:")
        style_label.setBuddy(combo_box)

        self.top_left_group_box = QGroupBox("Group 1")
        self.top_right_group_box = QGroupBox("Group 2")
        self.bottom_left_tab_widget = QTabWidget()
        self.bottom_right_group_box = QGroupBox("Group 3")
        self.progress_bar = QProgressBar()

        self.create_top_left_group_box()
        self.create_top_right_group_box()
        self.create_bottom_left_tab_widget()
        self.create_bottom_right_group_box()
        self.create_progress_bar()
        combo_box.activated[str].connect(self.change_style)

        top_layout = QHBoxLayout()
        top_layout.addWidget(style_label)
        top_layout.addWidget(combo_box)
        top_layout.addStretch(1)

        home_layout = QGridLayout()
        home_layout.addLayout(top_layout, 0, 0, 1, 2)
        home_layout.addWidget(self.top_left_group_box, 1, 0)
        home_layout.addWidget(self.top_right_group_box, 1, 1)
        home_layout.addWidget(self.bottom_left_tab_widget, 2, 0)
        home_layout.addWidget(self.bottom_right_group_box, 2, 1)
        home_layout.addWidget(self.progress_bar, 3, 0, 1, 2)
        home_layout.setRowStretch(1, 1)
        home_layout.setRowStretch(2, 1)
        home_layout.setColumnStretch(0, 1)
        home_layout.setColumnStretch(1, 1)
        self.setLayout(home_layout)
        self.setWindowTitle("G_Air signal widget")
        self.change_style('Fusion')
        self.setGeometry(400, 400, 300, 260)

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

    def create_top_left_group_box(self):
        """
        Create top left group box.
        """
        radio_button_1 = QRadioButton("Radio button 1")
        radio_button_2 = QRadioButton("Radio button 2")
        radio_button_3 = QRadioButton("Radio button 3")
        radio_button_1.setChecked(True)
        check_box = QCheckBox("Tri-state check box")
        check_box.setTristate(True)
        check_box.setCheckState(Qt.PartiallyChecked)
        layout = QVBoxLayout()
        layout.addWidget(radio_button_1)
        layout.addWidget(radio_button_2)
        layout.addWidget(radio_button_3)
        layout.addWidget(check_box)
        layout.addStretch(1)
        self.top_left_group_box.setLayout(layout)

    def create_top_right_group_box(self):
        """
        Create top right group box.
        """
        default_push_button = QPushButton("Default Push Button")
        default_push_button.setDefault(True)

        toggle_push_button = QPushButton("Toggle Push Button")
        toggle_push_button.setCheckable(True)
        toggle_push_button.setChecked(True)

        flat_push_button = QPushButton("Flat Push Button")
        flat_push_button.setFlat(True)
        layout = QVBoxLayout()
        layout.addWidget(default_push_button)
        layout.addWidget(toggle_push_button)
        layout.addWidget(flat_push_button)
        layout.addStretch(1)
        self.top_right_group_box.setLayout(layout)

    def create_bottom_left_tab_widget(self):
        """
        Create bottom left group box.
        """
        self.bottom_left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                                  QSizePolicy.Ignored)

        tab1 = QWidget()
        table_widget = QTableWidget(10, 10)

        tab1_h_box = QHBoxLayout()
        tab1_h_box.setContentsMargins(5, 5, 5, 5)
        tab1_h_box.addWidget(table_widget)
        tab1.setLayout(tab1_h_box)

        tab2 = QWidget()
        text_edit = QTextEdit()

        text_edit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2_h_box = QHBoxLayout()
        tab2_h_box.setContentsMargins(5, 5, 5, 5)
        tab2_h_box.addWidget(text_edit)
        tab2.setLayout(tab2_h_box)

        self.bottom_left_tab_widget.addTab(tab1, "&Table")
        self.bottom_left_tab_widget.addTab(tab2, "Text &Edit")

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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = GAirGUI()
    gallery.show()
    sys.exit(app.exec_())

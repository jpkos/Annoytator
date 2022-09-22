# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 00:10:31 2021

@author: jankos
"""

from annoytator_gui import Ui_MainWindow

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore 
from PyQt5 import QtGui
import pandas as pd
import cv2
import re

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class EventsWindow(qtw.QDialog):
    newEvent = QtCore.pyqtSignal(str)
    def __init__(self, parent=None, columns=None):
        super(EventsWindow, self).__init__(parent)
        self.columns = columns
        self.resize(125*(len(self.columns) + 1), 120)
        self.layOutWinV = qtw.QVBoxLayout(self)
        self.eventWidget = qtw.QTableWidget(self)
        self.addEventButton = qtw.QPushButton(self)
        self.addEventButton.setText('Add Event')
        self.addHotKeyEdit = qtw.QLineEdit(self)
        self.addHotKeyEdit.setMaxLength(1)
        self.hotKeyLabel = qtw.QLabel('Add hotkey:')
        self.layOutWinV.addWidget(self.eventWidget)
        self.layOutWinV.addWidget(self.hotKeyLabel)
        self.layOutWinV.addWidget(self.addHotKeyEdit)
        self.layOutWinV.addWidget(self.addEventButton)
        self.create_table()
        self.addEventButton.clicked.connect(self.add_new_event)
        
    def create_table(self):
        self.eventWidget.setRowCount(1)
        self.eventWidget.setColumnCount(len(self.columns))
        self.eventWidget.setHorizontalHeaderLabels(self.columns)
        
    def add_new_event(self):
        vals = []
        hotkey = self.addHotKeyEdit.text().upper()
        vals.append(hotkey)
        for col in range(len(self.columns)):
            value = self.eventWidget.item(0,col)
            try:
                vals.append(value.text())
            except AttributeError:
                vals.append('')
        print(vals)
        self.newEvent.emit(','.join(vals))
        
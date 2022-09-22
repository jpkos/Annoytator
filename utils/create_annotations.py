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


class createAnnotationsWindow(qtw.QDialog):
    newAnnotation = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(createAnnotationsWindow, self).__init__(parent)
        self.columnsSpinBox = qtw.QSpinBox()
        self.annotationWindow = qtw.QTableWidget()
        self.annotationWindow.setRowCount(1)
        self.annotationWindow.setColumnCount(1)
        self.resize(125*5, 120)
        self.annotationWindow.setItem(0,0,qtw.QTableWidgetItem('frame'))
        # self.columnsSpinBox.setRange(1, 100)
        self.columnsSpinBox.valueChanged['int'].connect(lambda x: self.annotationWindow.setColumnCount(self.columnsSpinBox.value()))
        self.spinBoxLabel = qtw.QLabel()
        self.spinBoxLabel.setText('Add columns:')
        self.addAnnotationsButton = qtw.QPushButton()
        self.addAnnotationsButton.setText('Add new annotations')
        self.layOutWinV = qtw.QVBoxLayout(self)
        self.layOutWinV.addWidget(self.spinBoxLabel)
        self.layOutWinV.addWidget(self.columnsSpinBox)
        self.layOutWinV.addWidget(self.annotationWindow)
        self.layOutWinV.addWidget(self.addAnnotationsButton)
        self.addAnnotationsButton.clicked.connect(self.add_new_annotation)
        
    def add_new_annotation(self):
        vals = []
        for col in range(self.columnsSpinBox.value()):
            value = self.annotationWindow.item(0,col)
            try:
                vals.append(value.text())
            except AttributeError:
                vals.append('')
        self.newAnnotation.emit(','.join(vals))
        
        

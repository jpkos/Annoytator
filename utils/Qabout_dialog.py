# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 20:25:09 2021

@author: jankos
"""

from annoytator_gui import Ui_MainWindow

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore 
from PyQt5 import QtGui
import pandas as pd
import cv2

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class AboutWindow(qtw.QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.resize(160, 75)
        self.layOutWinV = qtw.QVBoxLayout(self)
        self.contactLabel = qtw.QLabel(self)
        self.contactLabel.setGeometry(5,5,150,50)
        self.setWhatsThis('That\'s my name and email')
        self.setWindowTitle('About')
        self.contactLabel.setText('2021 Jani Koskinen \njani.koskinen@uef.fi')
        

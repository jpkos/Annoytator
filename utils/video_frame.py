# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 19:30:13 2021

@author: jankos
"""
from annoytator_gui import Ui_MainWindow

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore
import pandas as pd
import cv2

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

class VideoViewer(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
            
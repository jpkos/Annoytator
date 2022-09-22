# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 20:12:12 2021

@author: jankos
"""

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5 import QtCore 
from PyQt5.QtWidgets import QAction


class eventListView(QtGui.QListView):
    def __init__(self):
        super(eventListView, self).__init__()
        
    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                return
            else:
                super(eventListView, self).mousePressEvent(event)
        
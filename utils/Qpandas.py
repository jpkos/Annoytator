# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as QtCore
import pandas as pd

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

class PandasModel(QAbstractTableModel):
    #from https://learndataanalysis.org/display-pandas-dataframe-with-pyqt5-qtableview-widget/
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            row = index.row()
            col = index.column()
            self._data.iloc[row][col] = float(value)
            self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
            return True
        return False
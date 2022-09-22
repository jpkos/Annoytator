# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_annotations.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_createNewAnnotationsDialog(object):
    def setupUi(self, createNewAnnotationsDialog):
        createNewAnnotationsDialog.setObjectName("createNewAnnotationsDialog")
        createNewAnnotationsDialog.resize(775, 243)
        self.tableWidget = QtWidgets.QTableWidget(createNewAnnotationsDialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 731, 111))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.columnsSpinBox = QtWidgets.QSpinBox(createNewAnnotationsDialog)
        self.columnsSpinBox.setGeometry(QtCore.QRect(20, 20, 42, 22))
        self.columnsSpinBox.setObjectName("columnsSpinBox")
        self.createNewAnnotationsButton = QtWidgets.QPushButton(createNewAnnotationsDialog)
        self.createNewAnnotationsButton.setGeometry(QtCore.QRect(250, 187, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.createNewAnnotationsButton.setFont(font)
        self.createNewAnnotationsButton.setObjectName("createNewAnnotationsButton")
        self.numberColumnsLabel = QtWidgets.QLabel(createNewAnnotationsDialog)
        self.numberColumnsLabel.setGeometry(QtCore.QRect(70, 20, 131, 16))
        self.numberColumnsLabel.setObjectName("numberColumnsLabel")

        self.retranslateUi(createNewAnnotationsDialog)
        self.columnsSpinBox.valueChanged['int'].connect(self.tableWidget.insertColumn)
        QtCore.QMetaObject.connectSlotsByName(createNewAnnotationsDialog)

    def retranslateUi(self, createNewAnnotationsDialog):
        _translate = QtCore.QCoreApplication.translate
        createNewAnnotationsDialog.setWindowTitle(_translate("createNewAnnotationsDialog", "Create new annotations"))
        self.createNewAnnotationsButton.setText(_translate("createNewAnnotationsDialog", "Create new annotations"))
        self.numberColumnsLabel.setText(_translate("createNewAnnotationsDialog", "Number of columns"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createNewAnnotationsDialog = QtWidgets.QDialog()
    ui = Ui_createNewAnnotationsDialog()
    ui.setupUi(createNewAnnotationsDialog)
    createNewAnnotationsDialog.show()
    sys.exit(app.exec_())


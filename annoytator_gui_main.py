# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from annoytator_gui import Ui_MainWindow
from create_annotations import createAnnotationsWindow

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5 import QtCore 
from utils.Qpandas import PandasModel
from utils.plotting import MplCanvas
from utils.events_window import EventsWindow
from utils.Qabout_dialog import AboutWindow
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

class CurrentFrame(QWidget):
    valueChanged = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(CurrentFrame, self).__init__(parent)
        self._value = 1
    @property    
    def value(self):
        return self._value
    @value.setter
    def value(self, new_frame):
        self._value = new_frame
        self.valueChanged.emit(self._value)
        

class AnnoytatorGUI(qtw.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.canvas = MplCanvas()
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.loadAnnotationButton.clicked.connect(self.load_annotations)
        self.loadVideoButton.clicked.connect(self.load_video)
        self.nextFrameButton.clicked.connect(lambda x: self.change_frame(self.current_frame.value+1))
        self.prevFrameButton.clicked.connect(lambda x: self.change_frame(self.current_frame.value-1))
        self.goToFrameButton.clicked.connect(self.jump_frame)
        self.annotationView.doubleClicked.connect(self.read_cell)
        self.loadDataButton.clicked.connect(self.load_data)
        self.displayDataButton.clicked.connect(self.display_data)
        toolbar = NavigationToolbar(self.canvas, self)
        self.plotLayout.addWidget(toolbar)
        self.plotLayout.addWidget(self.canvas)
        self.setLayout(self.plotLayout)
        self.frameSlider.valueChanged.connect(self.slider_connected)
        self.eventListWidget.itemDoubleClicked.connect(self.add_annotation)
        
        self.frameNumberEdit.returnPressed.connect(self.update_display)
        
        self.addEventsButton.clicked.connect(self.add_events)
        self.saveAnnotationButton.clicked.connect(self.save_annotations)
        self.deleteEventsButton.clicked.connect(self.delete_events)
        
        self.statusBar = qtw.QStatusBar()
        self.setStatusBar(self.statusBar)

        
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.show_about)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        self.data = None
        self.annotations = None
        self.video_capture = None
        self.max_frame = None
        self.current_frame = CurrentFrame()
        self.current_frame.valueChanged.connect(self.frame_updated)
        self.data_loaded = False
        self.annotations_loaded = False
        self.annotation_save_path = ''
        
    def frame_updated(self):
        self.update_video_frame()
        if self.data_loaded:
            self.update_display()
        
    def load_annotations(self):
        file_name,_ = qtw.QFileDialog.getOpenFileName(self, 'Load annotations')
        if file_name == '':
            return None
        df = pd.read_csv(file_name)
        self.annotations = df
        model = PandasModel(self.annotations)
        self.annotationView.setModel(model)
        self.annotations_loaded = True
        
    def save_annotations(self):
        if not self.annotations_loaded:
            print('No annotations loaded yet')
            return None
        if self.annotation_save_path == '':
            file_name,_ = qtw.QFileDialog.getSaveFileName(self, 'Load annotations')
        if file_name == '':
            return None
        self.annotation_save_path = file_name
        self.annotations.to_csv(file_name, index=None)
        
    def add_annotation(self, item):
        vals = item.text().split(',')[1:]
        vals = [val if val != '' else self.current_frame.value for val in vals]
        print(vals)
        new_row = pd.DataFrame([vals], columns=self.annotations.columns.tolist())
        self.annotations = pd.concat([self.annotations[:self.current_frame.value], new_row,
                              self.annotations[self.current_frame.value:]]).reset_index(drop=True).sort_values('frame')
        
        # self.annotationView.setData()
        model = PandasModel(self.annotations)
        self.annotationView.setModel(model)
        self.annotationView.model().layoutChanged.emit()
        self.setFocus()
        self.auto_save_annotations()
            
    def auto_save_annotations(self):
        if self.actionAutosave.isChecked():
            if self.annotation_save_path == '':
                self.annotation_save_path,_ = qtw.QFileDialog.getSaveFileName(self, 'save annotations')
            if self.annotation_save_path == '':
                return None
            self.annotations.to_csv(self.annotation_save_path, index=None)        
        
    def drop_annotation(self, row):
        self.annotations = self.annotations.drop(index=row).reset_index(drop=True)
        model = PandasModel(self.annotations)
        self.annotationView.setModel(model)
        self.annotationView.model().layoutChanged.emit()
        self.setFocus()
        self.auto_save_annotations()
        
    def convert_frame(self, frame):
        display_frame = QtGui.QImage(frame.data,
                             frame.shape[1],
                             frame.shape[0],
                             QtGui.QImage.Format_RGB888).rgbSwapped()
        return display_frame
    

    def load_video(self):
        file_name,_ = qtw.QFileDialog.getOpenFileName(self, 'Load video')
        if file_name == '':
            return None
        self.video_capture = cv2.VideoCapture(file_name)
        self.max_frame = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = self.video_capture.read()
        display_frame = self.convert_frame(frame)
        self.frameViewLabel.setPixmap(QtGui.QPixmap.fromImage(display_frame))
        self.frameNumberEdit.setText(str(self.current_frame.value))
        
    def update_video_frame(self):
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame.value)
        ret, frame = self.video_capture.read()
        display_frame = self.convert_frame(frame)
        self.frameViewLabel.setPixmap(QtGui.QPixmap.fromImage(display_frame))
        self.frameNumberEdit.setText(str(self.current_frame.value))
        
    def change_frame(self, new_frame):
        if new_frame < 0 or new_frame > self.max_frame:
            print('outside of frame range!')
        else:
            self.current_frame.value = new_frame
        
    def jump_frame(self):
        read_frame = self.frameNumberEdit.text()
        new_frame = int(read_frame)
        if new_frame < 0 or new_frame > self.max_frame:
            print('outside of frame range!')
        else:
            self.current_frame.value = new_frame

    def keyPressEvent(self, k):
        print(k.key())
        if k.key() == Qt.Key_Delete:
            selected_row = self.annotationView.selectionModel().currentIndex().row()
            if selected_row>0:
                self.drop_annotation(selected_row)
        if self.video_capture != None:
            if k.key() == Qt.Key_A:
                self.change_frame(self.current_frame.value-10)
            if k.key() == Qt.Key_S:
                self.change_frame(self.current_frame.value-1)
            if k.key() == Qt.Key_D:
                self.change_frame(self.current_frame.value+1)
            if k.key() == Qt.Key_F:
                self.change_frame(self.current_frame.value+10)
        else:
            return None
            
    def read_cell(self):
        index = self.annotationView.selectionModel().currentIndex()
        self.current_frame.value = int(float(index.sibling(index.row(), index.column()).data()))
        # self.update_frame()
        # if self.data_loaded:
        #     self.update_display()
        self.setFocus()
        
    def load_data(self):
        file_name,_ = qtw.QFileDialog.getOpenFileName(self, 'Load data')
        if file_name == '':
            return None
        with open(file_name, 'r') as csvfile:
            line = csvfile.readline()
            d = csv.Sniffer().sniff(line)
            sep = d.delimiter
        df = pd.read_csv(file_name, sep=sep)
        self.xCoorBox.clear()
        self.yCoorBox.clear()
        self.xCoorBox.addItems(df.columns)
        self.yCoorBox.addItems(df.columns)
        self.data = df
        self.frameSlider.setMaximum(len(self.data))
        self.data_loaded = True
        
    def display_data(self):
        self.canvas.axes.clear()
        x = str(self.xCoorBox.currentText())
        y = str(self.yCoorBox.currentText())
        self.canvas.axes.plot(self.data[x], self.data[y])
        if self.displayEventsBox.isChecked():
            for i, row in self.annotations.iterrows():
                self.canvas.axes.axvline(x=row['frame'], color='green')
        if self.connectVideoBox.isChecked():
            self.canvas.axes.axvline(x=self.current_frame.value, color='red')
        self.canvas.axes.tick_params(labelrotation=45)
        self.canvas.draw()
        
    def update_display(self):
        self.display_data()
        
        
    def add_events(self):
        def create_annotation(self,item):
            vals = item.split(',')
            new_header = pd.DataFrame(columns=vals)
            self.annotations = new_header
            # self.annotationView.setData()
            model = PandasModel(self.annotations)
            self.annotationView.setModel(model)
            self.annotationView.model().layoutChanged.emit()
            self.setFocus()
            
        if self.annotations_loaded:
            self.eventWindow = EventsWindow(parent=self, columns=self.annotations.columns)
            self.eventWindow.newEvent.connect(lambda x: self.eventListWidget.addItem(x))
            self.eventWindow.show()
        else:
            self.createAnnotations = createAnnotationsWindow(self)
            self.createAnnotations.show()
            self.createAnnotations.newAnnotation.connect(lambda x: create_annotation(self, x))
            self.annotations_loaded = True
        
    def delete_events(self):
        listItems=self.eventListWidget.selectedItems()   
        for item in listItems:
            self.eventListWidget.takeItem(self.eventListWidget.row(item))
        
    def show_about(self):
        self.aboutDialog = AboutWindow(self)
        self.aboutDialog.show()
        
    def slider_connected(self):
        if self.connectVideoBox.isChecked():
            self.current_frame.value = self.frameSlider.value()
        
        
        
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = AnnoytatorGUI()
    widget.show()
    
    app.exec_()
        
# -*- coding:utf-8 -*-

from PyQt5.QtCore import pyqtSignal,QObject

class MySignal(QObject):
    taskCreatedSignal = pyqtSignal(str,int,int)
    taskSpeedSignal = pyqtSignal(str,int)

signal = MySignal()

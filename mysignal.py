# -*- coding:utf-8 -*-

from PyQt5.QtCore import pyqtSignal,QObject

class MySignal(QObject):
    taskCreatedSignal = pyqtSignal(str,int,int)
    taskSpeedSignal = pyqtSignal(str,int)
    taskPauseSignal = pyqtSignal(int)
    informationSignal = pyqtSignal(str)
    changeUserNameSignal = pyqtSignal(str)
    getListSignal = pyqtSignal(str)
    getUrlSIgnal = pyqtSignal(str)
    exitSignal = pyqtSignal()

signal = MySignal()

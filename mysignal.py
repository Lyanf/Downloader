from PyQt5.QtCore import pyqtSignal,QObject

class MySignal(QObject):
    taskCreatedSignal = pyqtSignal(str,int,int)


signal = MySignal()

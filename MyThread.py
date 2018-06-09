# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
import time
from downloader import DownloadTask
from hurry.filesize import filesize
from mysignal import signal
class BackWorkder(QObject):
    startSpeed = pyqtSignal()
    stopSpeed = pyqtSignal()
    def __init__(self,client):
        super(BackWorkder, self).__init__()
        self.client = client
    @pyqtSlot()
    def setAllSpeedForUI(self):
        while True:
            time.sleep(1)
            i = 0
            for task in self.client.downloadTaskList:
                assert isinstance(task,DownloadTask)
                t = filesize.size(task.getDownloadedSize())
                signal.taskSpeedSignal.emit(str(t),i)
                i = i+1


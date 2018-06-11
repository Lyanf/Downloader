# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
import time
from downloader import DownloadTask
from hurry.filesize import filesize
from mysignal import signal
from User import User
import os

class BackWorkder(QObject):
    startSpeed = pyqtSignal()
    stopSpeed = pyqtSignal()

    def __init__(self, client):
        super(BackWorkder, self).__init__()
        self.client = client
        self.stop = False

    @pyqtSlot()
    def setAllSpeedForUI(self):
        while True:
            if self.stop == False:
                time.sleep(1)
                i = 0
                for task in self.client.downloadTaskList:
                    assert isinstance(task, DownloadTask)
                    t = filesize.size(task.getDownloadedSize())
                    signal.taskSpeedSignal.emit(str(t), i)
                    i = i + 1
            else:
                break
    @pyqtSlot()
    def setSpeedStop(self):
        self.stop == True

class UserWorker(QObject):
    signInSignal = pyqtSignal(str, str)
    logInSignal = pyqtSignal(str, str)
    sendUrlSignal = pyqtSignal(str)
    showListSignal = pyqtSignal()
    getUrlSignal = pyqtSignal(str)

    def __init__(self):
        super(UserWorker, self).__init__()
        self.user = User()
        self.signInSignal.connect(self.signInSlot)
        self.logInSignal.connect(self.logInSlot)
        self.sendUrlSignal.connect(self.sendUrlSlot)
        self.showListSignal.connect(self.showListSlot)
        self.getUrlSignal.connect(self.getUrlSLot)

    @pyqtSlot(str, str)
    def signInSlot(self, username, password):
        get = self.user.signIn(username, password)
        if get == True:
            signal.informationSignal.emit('注册成功！')
        else:
            signal.informationSignal.emit('注册失败！')

    @pyqtSlot(str, str)
    def logInSlot(self, username, password):
        get = self.user.logIn(username, password)
        if get == True:
            signal.changeUserNameSignal.emit(username)
            signal.informationSignal.emit('登陆成功！')
        else:
            signal.informationSignal.emit('登录失败！')

    @pyqtSlot(str)
    def sendUrlSlot(self, url):
        self.user.sendUrl(url)

    @pyqtSlot()
    def showListSlot(self):
        self.user.reLogIn()
        # signal.getListSignal.emit(self.user.fileListStr)
        signal.informationSignal.emit(self.user.fileListStr)
    @pyqtSlot(str)
    def getUrlSLot(self, fileName):
        url = self.user.getUrl(fileName)
        # signal.getUrlSIgnal.emit(url)
        if url == '':
            signal.informationSignal.emit('远程服务器没有这个文件')
            return
        print(url)
        print('%r'%url)
        os.system('echo '+url+'|clip')
        signal.informationSignal.emit(url+'该url已经复制到您的剪切板中！')

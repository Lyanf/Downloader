import time
from User import User
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import threading
from downloader import Downloader, DownloadTask
from mysignal import signal
from hurry.filesize import filesize
import pickle
from MyThread import BackWorkder,UserWorker
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initConnect()
        self.client = self.restoreDonwloader()
        self.center = self.centralWidget()
        self.listPage = self.center
        self.initTaskForUI()
        self.initSpeedShow()
        self.initUserThread()
        assert isinstance(self.center, ListPage)
        assert isinstance(self.client, Downloader)

    def initUserThread(self):
        self.userThread = QThread()
        self.userWorker = UserWorker()
        self.userWorker.moveToThread(self.userThread)
        self.userThread.start()
    def initSpeedShow(self):
        self.back = BackWorkder(self.client)
        self.th = QThread()
        self.back.moveToThread(self.th)
        self.back.startSpeed.connect(self.back.setAllSpeedForUI)
        self.th.start()
        self.back.startSpeed.emit()

    def restoreDonwloader(self):
        getDownloader = ''
        try:
            with open('downloader.data','rb') as f:
                getDownloader = pickle.load(f)
        except (FileNotFoundError, EOFError) as e:
            e.with_traceback(None)
            print('已经创建全新的Downloader！')
            getDownloader = Downloader()
        getDownloader.registerExitDownloader()
        return getDownloader

    def initUI(self):
        temp = ListPage(self)
        self.setCentralWidget(temp)
        self.toolBar = self.addToolBar('tools')
        self.menuBar = self.menuBar()

        addTaskAction = QAction(QIcon(r'Snipaste_2018-04-26_19-07-25.png'), 'New', self)
        startTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-44.png'), 'Start', self)
        pauseTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-19.png'), 'Pause', self)
        deleteTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-26.png'), 'Delete', self)
        self.signInAction = QAction('SingIn')
        self.logInAction = QAction('LogIn')
        self.showListAction = QAction('ShowList')
        self.sendUrlAction = QAction('SendUrl')
        self.getUrlAction = QAction('GetUrl')

        self.addTaskAction = addTaskAction
        self.startTaskAction = startTaskAction
        self.pauseTaskAction = pauseTaskAction
        # self.deleteTaskAction = deleteTaskAction

        assert isinstance(self.menuBar, QMenuBar)
        fileMenu = self.menuBar.addMenu('&File')
        fileMenu.addAction(addTaskAction)
        fileMenu.addAction(startTaskAction)
        fileMenu.addAction(pauseTaskAction)
        fileMenu.addAction(deleteTaskAction)

        userMenu = self.menuBar.addMenu('&User')
        userMenu.addAction(self.signInAction)
        userMenu.addAction(self.logInAction)
        # userMenu.addAction(self.showListAction)
        userMenu.addAction(self.sendUrlAction)
        userMenu.addAction(self.getUrlAction)

        assert isinstance(self.toolBar, QToolBar)
        self.toolBar.addAction(addTaskAction)
        self.toolBar.addAction(startTaskAction)
        self.toolBar.addAction(pauseTaskAction)
        # self.toolBar.addAction(deleteTaskAction)

        self.resize(800, 500)
        self.show()

    def initConnect(self):
        self.addTaskAction.triggered.connect(self.addTaskActionSlot)
        self.startTaskAction.triggered.connect(self.startTaskActionSlot)
        self.pauseTaskAction.triggered.connect(self.pauseTaskActionSlot)
        # self.deleteTaskAction.triggered.connect(self.deleteTaskActionSlot)
        self.signInAction.triggered.connect(self.signInActionSlot)
        self.logInAction.triggered.connect(self.logInActionSlot)
        self.showListAction.triggered.connect(self.showListActionSlot)
        self.sendUrlAction.triggered.connect(self.sendUrlActionSLot)
        self.getUrlAction.triggered.connect(self.getUrlActionSlot)

        signal.taskCreatedSignal.connect(self.taskCreatedSlot)
        signal.taskSpeedSignal.connect(self.speedSlot)
        signal.taskPauseSignal.connect(self.pauseTaskSlot)
        signal.informationSignal.connect(self.informationSlot)
        signal.changeUserNameSignal.connect(self.userChangedSlot)
    def userChangedSlot(self,name):
        assert isinstance(self.listPage,ListPage)
        self.listPage.userLabel.setText(name)
    def informationSlot(self,info):
        t = QMessageBox().information(self,'information',info,QMessageBox.Ok)
    def signInActionSlot(self):
        getTextTuple1 = QInputDialog().getText(self, 'User Name', 'User', )
        if getTextTuple1[-1] == False:
            return None
        else:
            userName = getTextTuple1[0]
            getTextTuple2 = QInputDialog().getText(self,'Password','password')
            if getTextTuple2[-1] ==False:
                return None
            password = getTextTuple2[0]
            # self.userWorker.signInSignal.connect(self.userWorker.signInSlot)
            self.userWorker.signInSignal.emit(userName,password)

    def logInActionSlot(self):
        getTextTuple1 = QInputDialog().getText(self, 'User Name', 'User', )
        if getTextTuple1[-1] == False:
            return None
        else:
            userName = getTextTuple1[0]
            getTextTuple2 = QInputDialog().getText(self,'Password','password')
            if getTextTuple2[-1] ==False:
                return None
            password = getTextTuple2[0]
            # self.userWorker.signInSignal.connect(self.userWorker.signInSlot)
            self.userWorker.logInSignal.emit(userName,password)
    def showListActionSlot(self):
        self.userWorker.showListSignal.emit()
    def sendUrlActionSLot(self):
        turl = QInputDialog().getText(self,'download by server','input the url')
        if turl[-1] == False:
            return None
        url = turl[0]
        self.userWorker.sendUrlSignal.emit(url)
    def getUrlActionSlot(self):
        turl = QInputDialog().getText(self, 'download by server', 'input the fileName')
        if turl[-1] == False:
            return None
        url = turl[0]
        self.userWorker.getUrlSignal.emit(url)

    def initTaskForUI(self):
        i = 0
        for task in self.client.downloadTaskList:
            assert isinstance(task,DownloadTask)
            signal.taskCreatedSignal.emit(task.getName(),task.getSize(),i)
            i = i+1

    def addTaskActionSlot(self):
        getTextTuple = QInputDialog().getText(self, 'URL Input', 'URL', )
        if getTextTuple[-1] == False:
            return None
        else:
            if getTextTuple[0] != '':
                url = getTextTuple[0]
                th = threading.Thread(target=self.client.createTask, kwargs={'url': url})
                th.start()
                # self.client.createTask(url)
            else:
                return None

    def startTaskActionSlot(self):
        center = self.centralWidget()
        assert isinstance(center, ListPage)
        selection = center.singsTable.selectionModel()
        assert isinstance(selection, QItemSelectionModel)
        rowIndex = []
        for i in selection.selectedRows():
            rowIndex.append(i.row())
        for i in rowIndex:
            self.client.start(i)
    def pauseTaskActionSlot(self):
        center = self.centralWidget()
        assert isinstance(center, ListPage)
        selection = center.singsTable.selectionModel()
        assert isinstance(selection, QItemSelectionModel)
        rowIndex = []
        for i in selection.selectedRows():
            rowIndex.append(i.row())
        for i in rowIndex:
            signal.taskPauseSignal.emit(i)
    def deleteTaskActionSlot(self):
        center = self.centralWidget()
        assert isinstance(center, ListPage)
        selection = center.singsTable.selectionModel()
        assert isinstance(selection, QItemSelectionModel)
        rowIndex = []
        for i in selection.selectedRows():
            rowIndex.append(i.row())
        for i in rowIndex:
            self.client.start(i)
            
    def taskCreatedSlot(self, fileName,byteSize,index):
        print(fileName)
        assert isinstance(self.listPage,ListPage)
        self.listPage.singsTable.insertRow(self.listPage.singsTable.rowCount())
        name = QTableWidgetItem(fileName)
        sizeHuman = filesize.size(byteSize)
        sizeHuman = QTableWidgetItem(sizeHuman)
        self.listPage.singsTable.setItem(index,0,name)
        self.listPage.singsTable.setItem(index,1,sizeHuman)
        print('任务创建成功！文件名为: %s'%fileName)

    def speedSlot(self,speed:str,index:int):
        assert isinstance(self.listPage,ListPage)
        speedItem = QTableWidgetItem(speed)
        self.listPage.singsTable.setItem(index,2,speedItem)

    def pauseTaskSlot(self,index):
        self.client.startedIndex.remove(index)


class ListPage(QScrollArea):
    def __init__(self, parent):
        super(ListPage, self).__init__()
        self.parent = parent
        self.setObjectName('nativeMusic')
        # with open('QSS/nativeMusic.qss', 'r', encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())

        self.mainLayout = QVBoxLayout(self)

        self.setTopShow()
        self.musicTable()

    # 布局。
    def setTopShow(self):
        self.showLabel = QLabel("下载器")
        self.userLabel = QLabel('未登录')

        self.spaceLine = QFrame(self)
        self.spaceLine.setObjectName("spaceLine")
        self.spaceLine.setFrameShape(QFrame.HLine)
        self.spaceLine.setFrameShadow(QFrame.Plain)
        self.spaceLine.setLineWidth(2)

        # self.selectButton = QPushButton("选择目录")
        # self.selectButton.setObjectName('selectButton')

        self.topShowLayout = QHBoxLayout()
        self.topShowLayout.addSpacing(20)
        self.topShowLayout.addWidget(self.showLabel)
        # self.topShowLayout.addWidget(self.selectButton)
        self.topShowLayout.addStretch(1)
        self.topShowLayout.addWidget(self.userLabel)

        self.mainLayout.addLayout(self.topShowLayout)
        self.mainLayout.addWidget(self.spaceLine)

    def musicTable(self):
        self.singsTable = QTableWidget()
        self.singsTable.setObjectName('TasksTable')
        self.singsTable.setMinimumWidth(self.width())
        self.singsTable.setColumnCount(4)
        self.singsTable.setHorizontalHeaderLabels(['文件名', '大小', '下载进度', '下载速度'])
        self.singsTable.setColumnWidth(0, self.width() / 4)
        self.singsTable.setColumnWidth(1, self.width() / 4)
        self.singsTable.setColumnWidth(2, self.width() / 4)
        self.singsTable.setColumnWidth(3, self.width() / 4)
        self.singsTable.horizontalHeader().setStretchLastSection(True)
        self.singsTable.verticalHeader().setVisible(False)
        self.singsTable.setShowGrid(False)
        self.singsTable.setAlternatingRowColors(True)

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.mainLayout.addWidget(self.singsTable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = mainWindow()

    t.show()
    app.exec_()

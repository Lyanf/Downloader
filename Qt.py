from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import threading
from downloader import Downloader, DownloadTask
from mysignal import signal
from hurry.filesize import filesize

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initConnect()
        self.client = Downloader()
        self.center = self.centralWidget()
        self.listPage = self.center

        assert isinstance(self.center, ListPage)
        assert isinstance(self.client, Downloader)

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
        self.logOutAction = QAction('LogOut')

        self.addTaskAction = addTaskAction
        self.startTaskAction = startTaskAction
        self.pauseTaskAction = pauseTaskAction
        self.deleteTaskAction = deleteTaskAction

        assert isinstance(self.menuBar, QMenuBar)
        fileMenu = self.menuBar.addMenu('&File')
        fileMenu.addAction(addTaskAction)
        fileMenu.addAction(startTaskAction)
        fileMenu.addAction(pauseTaskAction)
        fileMenu.addAction(deleteTaskAction)

        userMenu = self.menuBar.addMenu('&User')
        userMenu.addAction(self.signInAction)
        userMenu.addAction(self.logInAction)
        userMenu.addAction(self.logOutAction)

        assert isinstance(self.toolBar, QToolBar)
        self.toolBar.addAction(addTaskAction)
        self.toolBar.addAction(startTaskAction)
        self.toolBar.addAction(pauseTaskAction)
        self.toolBar.addAction(deleteTaskAction)

        self.resize(800, 500)
        self.show()

    def initConnect(self):
        self.addTaskAction.triggered.connect(self.addTaskActionSlot)
        self.startTaskAction.triggered.connect(self.startTaskActionSlot)
        self.pauseTaskAction.triggered.connect(self.pauseTaskActionSlot)
        self.deleteTaskAction.triggered.connect(self.deleteTaskActionSlot)

        signal.taskCreatedSignal.connect(self.taskCreatedSlot)

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
        pass
    def deleteTaskActionSlot(self):
        pass
    def taskCreatedSlot(self, fileName,byteSize,index):
        print(fileName)
        assert isinstance(self.listPage,ListPage)
        self.listPage.singsTable.insertRow(self.listPage.singsTable.rowCount())
        name = QTableWidgetItem(fileName)
        sizeHuman = filesize.size(byteSize)
        sizeHuman = QTableWidgetItem(sizeHuman)
        self.listPage.singsTable.setItem(index,0,name)
        self.listPage.singsTable.setItem(index,1,sizeHuman)
        print(sizeHuman.text())
        print('ok le?')

    def initDownloader(self):
        self.donwloader = Downloader()


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

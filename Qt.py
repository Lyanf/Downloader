from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.toolBar = self.addToolBar('tools')
        self.menuBar = self.menuBar()

        addTaskAction = QAction(QIcon(r'Snipaste_2018-04-26_19-07-25.png'),'New',self)
        startTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-44.png'),'Start',self)
        pauseTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-19.png'),'Pause',self)
        deleteTaskAction = QAction(QIcon(r'Snipaste_2018-04-27_17-30-26.png'),'Delete',self)


        assert isinstance(self.menuBar,QMenuBar)
        fileMenu = self.menuBar.addMenu('&File')
        fileMenu.addAction(addTaskAction)
        fileMenu.addAction(startTaskAction)
        fileMenu.addAction(pauseTaskAction)
        fileMenu.addAction(deleteTaskAction)

        assert isinstance(self.toolBar,QToolBar)
        self.toolBar.addAction(addTaskAction)
        self.toolBar.addAction(startTaskAction)
        self.toolBar.addAction(pauseTaskAction)
        self.toolBar.addAction(deleteTaskAction)

        self.resize(800,500)
        self.show()
class downloadTaskList(QScrollArea):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.table = QTableWidget(self)


class NativeMusic(QScrollArea):
    def __init__(self, parent):
        super(NativeMusic, self).__init__()
        self.parent = parent
        self.setObjectName('nativeMusic')
        with open('QSS/nativeMusic.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

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
        self.singsTable.setHorizontalHeaderLabels(['文件名', '大小', '下载进度','下载速度'])
        self.singsTable.setColumnWidth(0, self.width() / 4 )
        self.singsTable.setColumnWidth(1, self.width() / 4 )
        self.singsTable.setColumnWidth(2, self.width() / 4 )
        self.singsTable.setColumnWidth(3,self.width()/4)
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
    temp = NativeMusic(t)
    t.setCentralWidget(temp)
    print(type(t.layout()))
    temp.show()
    app.exec_()

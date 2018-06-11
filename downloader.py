# -*- coding:utf-8 -*-

import time
import requests
import os
import threading
import atexit
import pickle
from mysignal import signal


class DownloadTask():
    def __init__(self, url, fileFolder, threadNum):
        self.time = time.time()
        self.url = url
        self.name = url.split(r'/')[-1]
        self.filePath = os.path.join(fileFolder, self.name)
        self.response = requests.get(url, stream=True)
        # self.header = self.response.headers
        self.fileSize = (int)(self.response.headers['Content-Length'])
        self.startList = []
        self.endList = []
        self.threadNum = threadNum
        self.downloadedSize = 0
        self.__dividFile()
        self.completed = False

    def __dividFile(self):
        length = self.fileSize
        num = self.threadNum
        if (length % num == 0):
            soloSize = (int)(length / num)
            for i in range(0, length, soloSize):
                self.startList.append(i)
            for i in self.startList:
                self.endList.append(i + soloSize - 1)
        else:
            # 这里的soloSize因为除不尽，所以只是整数部分，这里把小数部分都整合到最后一个块里面
            soloSize = (int)(length / num)
            for i in range(0, length, soloSize):
                self.startList.append(i)
            for i in self.startList[0:-1]:
                self.endList.append(i + soloSize - 1)
            self.endList.append(length - 1)
        self.oriStartList = self.startList
        self.oriEndList = self.endList
        print(self.startList)
        print(self.endList)
        # self.hasDownloaded = self.startList

    def getName(self):
        return self.name

    def getSize(self):
        return self.fileSize

    def setHasCompleted(self, completed: bool):
        self.completed = completed

    def isCompleted(self):
        return self.completed

    def getContinueStartEndList(self):
        return self.startList, self.endList

    def getOriStartEndList(self):
        return self.oriStartList, self.oriEndList

    def getUrl(self):
        return self.url

    def logDownloaded(self, index, size):
        self.startList[index] = self.startList[index] + size

    def addDownloadedSize(self, size):
        self.downloadedSize += size

    def getDownloadedSize(self):
        return self.downloadedSize

    def __str__(self):
        return 'DownloadTask:' + '%s   url:%s' % (self.getName(), self.getUrl())


class Downloader:
    def __init__(self):
        self.downloadTaskList = []
        self.downloadingThread = []
        self.threadNum = 5
        self.soloSize = 10240
        self.tempFolder = os.path.abspath('./tempSave')
        self.saveFolder = os.path.abspath('./downloadFiles')
        self.dataFolder = os.path.abspath('./')
        self.dataPath = os.path.join(self.dataFolder, 'downloader.data')
        self.startedIndex = []
    def setThreadNum(self, num):
        # num = (int)(num)
        if num > 64 or num <= 0:
            raise Exception('线程数错误', num)
        self.threadNum = num

    def setSaveFolder(self, folder):
        self.saveFolder = folder

    # 新建一个下载任务
    def createTask(self, url, fileFolder=None):
        if not fileFolder:
            fileFolder = self.saveFolder
        task = DownloadTask(url, fileFolder, self.threadNum)
        self.downloadTaskList.append(task)
        signal.taskCreatedSignal.emit(task.getName(), task.getSize(), len(self.downloadTaskList) - 1)
        return

    #     开始一个下载任务，接收该下载任务的index
    def start(self, index):
        t = threading.Thread(target=self.__startDownload, kwargs={'index': index})
        t.start()
        self.startedIndex.append(index)

    '''开始一个下载任务，接收该下载任务的index，属于内部函数'''
    def __startDownload(self, index):
        thisTask = self.downloadTaskList[index]
        assert isinstance(thisTask, DownloadTask)
        if thisTask.isCompleted() == True:
            print('该任务的下载已经完成了！')
            return
        que = []
        for i in range(0, self.threadNum):
            t = threading.Thread(target=self.__threadOfDownload, kwargs={'downloadTask': self.downloadTaskList[index],
                                                                         'index': i,
                                                                         'whichTask':index})
            t.start()
            que.append(t)
        for i in que:
            i.join()
        if index not in self.startedIndex:
            print('该任务已经成功暂停！')
            return
        if not os.path.exists(self.saveFolder):
            os.mkdir(self.saveFolder)
        with open(os.path.join(self.saveFolder, thisTask.getName()), 'w+b') as completeFile:
            for i in range(0, self.threadNum):
                f = open(os.path.join(self.tempFolder, thisTask.getName() + str(i)), 'rb')
                while True:
                    a = f.read(1024000)
                    if a != b'':
                        completeFile.write(a)
                    else:
                        break
                f.close()
        thisTask.setHasCompleted(True)
        print('该任务已经下载完毕！')

    '''对于每一个下载任务，分部分下载，即多线程，该index是指第几个线程，属于内部函数'''

    def __threadOfDownload(self, downloadTask: DownloadTask, index,whichTask):
        if os.path.exists(self.tempFolder) == False:
            os.mkdir(self.tempFolder)
        path = os.path.join(self.tempFolder, downloadTask.getName() + str(index))
        tstart, tend = downloadTask.getContinueStartEndList()
        ostart, oend = downloadTask.getOriStartEndList()
        start, end = tstart[index], tend[index]
        oriStart, oriEnd = ostart[index], oend[index]
        hasDownloaded = start - oriStart
        if start == end:
            return
        print('线程 %d 已经创建完毕，开始下载！'%index)
        thisHeader = {'Range': 'bytes=%d-%d' % (start, end)}
        link = requests.get(downloadTask.getUrl(), stream=True, headers=thisHeader)
        with open(path, 'a+b',buffering=self.soloSize) as f:
            for content in link.iter_content(self.soloSize):
                if whichTask in self.startedIndex:
                    f.write(content)
                    downloadTask.logDownloaded(index, len(content))
                    downloadTask.addDownloadedSize(len(content))
                else:
                    link.close()
                    return
        print('线程 %d 已经下载完毕！'%index)
        link.close()

    def registerExitDownloader(self):
        atexit.register(self.saveInfo)

    # 将当前下载器对象进行保存
    def saveInfo(self):
        # os.makedirs(self.dataFolder, exist_ok=True)
        # os.remove(self.dataPath)
        f = open(self.dataPath, 'wb')
        pickle.dump(self, f)
        f.close()
        with open('t.txt', 'w') as f:
            for i in self.downloadTaskList:
                f.write(i.__str__())
                f.write('\n')

    #  读取上一次关闭掉的下载器对象
    def load(self):
        if os.path.exists(self.dataPath):
            f = open(self.dataPath, 'rb')
            t = pickle.load(f)
            return t
        else:
            return self

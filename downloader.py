import time
import requests
import os
import threading
import atexit
import pickle


class Downloader:
    def __init__(self):
        self.downloadTaskList = []
        self.threadNum = 5
        self.soloSize = 10240
        self.tempFolder = os.path.abspath('./tempSave')
        self.saveFolder = os.path.abspath('./downloadFiles')
        self.dataFolder = os.path.abspath('./')
        self.dataPath = os.path.join(self.dataFolder, 'downloader.data')
        atexit.register(self.saveInfo)

    def setThreadNum(self, num):
        # num = (int)(num)
        if num > 64 or num <= 0:
            raise Exception('线程数错误', num)
        self.threadNum = num

    def addDownloadTask(self, task):
        # assert isinstance(task, Downloader)
        pass

    def setSaveFolder(self, folder):
        self.saveFolder = folder

    def createTask(self, url, fileFolder=None):
        if not fileFolder:
            fileFolder = self.saveFolder
        task = DownloadTask(url, fileFolder, self.threadNum)
        self.downloadTaskList.append(task)
    def start(self,index):
        t = threading.Thread(target=self.startDownload,kwargs={'index':index})
        t.start()


    def startDownload(self, index):
        thisTask = self.downloadTaskList[index]
        assert isinstance(thisTask, DownloadTask)
        startList, endList = thisTask.getStartEndList()
        que = []
        for i, a, b in zip(range(0, self.threadNum), startList, endList):
            t = threading.Thread(target=self.threadOfDownload, kwargs={'downloadTask': self.downloadTaskList[index],
                                                                       'start': a,
                                                                       'end': b,
                                                                       'tempSavePath': self.tempFolder,
                                                                       'index': i})
            t.start()
            que.append(t)
        for i in que:
            i.join()
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

    def threadOfDownload(self, downloadTask, start, end, tempSavePath, index):
        if  os.path.exists(tempSavePath)==False:
            os.mkdir(tempSavePath)
        path = os.path.join(tempSavePath, downloadTask.getName() + str(index))
        thisHeader = {'Range': 'bytes=%d-%d' % (start, end)}
        link = requests.get(downloadTask.getUrl(), stream=True, headers=thisHeader)
        with open(path, 'w+b') as f:
            for content in link.iter_content(self.soloSize):
                f.write(content)
                downloadTask.logDownloaded(index, self.soloSize)
        link.close()

    def saveInfo(self):
        os.makedirs(self.dataFolder, exist_ok=True)
        f = open(self.dataPath, 'wb')
        pickle.dump(self, f)
        f.close()

    def load(self):
        if os.path.exists(self.dataPath):
            f = open(self.dataPath, 'rb')
            t = pickle.load(f)
            return t
        else:
            return self


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
        self.hasDownloaded = []
        self.threadNum = threadNum
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
            for i in self.startList[0:-2]:
                self.endList.append(i + soloSize - 1)
            self.endList.append(length - 1)
        # self.hasDownloaded = self.startList

    def getName(self):
        return self.name

    def setDownloadStatus(self, hasDownloaded):
        pass

    def getStartEndList(self):
        # if self.hasDownloaded == None:
        #     for i in range(0, self.hasDownloaded.__sizeof__()):
        #         self.startList[i] = self.hasDownloaded[i] + 1
        return self.startList, self.endList

    def getUrl(self):
        return self.url

    def logDownloaded(self, index, size):
        self.startList[index] = self.startList[index] + size

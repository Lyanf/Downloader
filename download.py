import requests
import threading
import os
import time
# url = 'http://dota2.dl.wanmei.com/dota2/client/DOTA2Setup20180206.zip'
def downloadSpeed(func):
    pass
allSize = 0
reDownload = []
lock = threading.Lock()
def getSpeed():
    while True:
        last = allSize
        time.sleep(1)
        print((allSize-last)/1024,' KB/s')
# @downloadSpeed
def download(start,end,filePath,url):
    # print('ok?')
    thisHeader = {'Range':'bytes=%d-%d' % (start, end)}
    link = requests.get(url,stream = True,headers=thisHeader)
    hasDownloaded = 0
    with open(filePath,'w+b') as f:
        # f.seek(start)
        soloSize = 8192
        global allSize
        try:
            for i in link.iter_content(soloSize):
                f.write(i)
                allSize = allSize+soloSize
                hasDownloaded = hasDownloaded+1
        except:
            global reDownload
            reDownload.append((start+soloSize*hasDownloaded+1,end))
    link.close()

def divideFile(url,num):
    link = requests.get(url,stream = True)
    length = (int)(link.headers['Content-Length'])
    startList = []
    endList = []
    if(length%num==0):
        soloSize = (int)(length/num)
        for i in range(0,length,soloSize):
            startList.append(i)
        for i in startList:
            endList.append(i+soloSize-1)
    else:
        # 这里的soloSize因为除不尽，所以只是整数部分，这里把小数部分都整合到最后一个块里面
        soloSize = (int)(length/num)
        for i in range(0,length,soloSize):
            startList.append(i)
        for i in startList[0:-2]:
            endList.append(i+soloSize-1)
        endList.append(length-1)
    return startList,endList

url = input('请输入下载地址，文件将被下载到当前目录下:')
url = url.strip()
num = input('请输入线程数')
num = (int)(num)

name = url.split(r'/')[-1]
filePath = os.path.join(os.path.abspath('.'),name)
print(filePath)
startList,endList = divideFile(url,num)

f = open(filePath,'w')
f.close()
for i,j,k in zip(startList,endList,range(1,num+1)):
    tempT = threading.Thread(target=download,kwargs={'start':i,'end':j,'filePath':filePath+str(k),'url':url})
    tempT.start()
tempT = threading.Thread(target=getSpeed())
tempT.start()

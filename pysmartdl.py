import os
import downloader

# dota2 = downloader.DownloadTask('http://dota2.dl.wanmei.com/dota2/client/DOTA2Setup20180206.zip','.',5)
downloader = downloader.Downloader()

downloader.setThreadNum(5)
# downloader.createTask('http://dota2.dl.wanmei.com/dota2/client/DOTA2Setup20180206.zip')
downloader.createTask('http://mxd.clientdown.sdo.com/150/Data150.zip')
downloader.createTask('http://mxd.clientdown.sdo.com/150/Data15001.cab')
downloader.createTask('http://mxd.clientdown.sdo.com/150/Data15002.cab')
downloader.createTask('http://mxd.clientdown.sdo.com/150/Maplestory150.exe')
downloader.start(0)
downloader.start(1)
downloader.start(2)
downloader.start(3)

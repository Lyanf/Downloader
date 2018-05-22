import socket


class linker:
    def __init__(self):
        self.serverIP = '23.83.250.163'
        self.port = 6091
        self.address = (self.serverIP, self.port)
        self.socket = socket.socket()
        try:
            self.socket.connect(self.address)
        except Exception as a:
            raise a
        self.linkType = {0: 'log in', 1: 'log out', 2: 'send url', 3: 'get download url'}

    def login(self, userID, userPW):
        # pass
        sendMessage = str.join(' ', [str(0), userID, userPW])
        self.socket.send(sendMessage)
        getRecv = self.socket.recv(10240)
        recvList = getRecv.strip()
        error = recvList[0]
        if error == 'none':
            return
        elif error == 'wrongid':
            raise Exception('wrongid')
        elif error == 'wrongpw':
            raise Exception('wrongpw')


    def sendUrl(self, userID, url):
        sendMessage = str.join(' ', [str(2), userID, url])
        self.socket.send(sendMessage)

    def getUrl(self, oriUrl):
        sendMessage = str.join(' ', [str(3), oriUrl])
        self.socket.send(sendMessage)
        getRecv = self.socket.recv(10240)
        recvList = getRecv.strip()
        error = recvList[0]
        if error == 'none':
            #             说明返回成功，那么紧接着的就是url
            return recvList[1]
        elif error == 'uncompleted':
            #             说明服务器还没下载完成呢
            raise Exception('uncompleted')
        elif error == 'empty':
            #             说明压根就没有这个东西在下载
            raise Exception('empty')

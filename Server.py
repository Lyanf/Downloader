# coding=UTF-8
import socketserver
import os     #运行shell命令
import FUNC


class MyServer(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()     #得到一个1kb的请求
        List = self.data.split('#')                     #用'#'分割

        if List[0] == 'log in':                         #登陆
            account = List[1]
            pw = List[2]

            flag = FUNC.login(account,pw)
            self.request.sendall(bytes(flag, 'utf8'))



        if List[0] == 'send url':
            userID = List[1]
            URL = List[2]
            flag = FUNC.sendURL(userID,URL)
            self.request.sendall(bytes(flag, 'utf8'))



                   #这里写linux内下载命令 比如axel + url


        if List[0] == 'get url':
            userID = List[1]
            fileName = List[2]

            flag = FUNC.getURL(userID,fileName)
            self.request.sendall(bytes(flag, 'utf8'))                #服务器的

        if List[0] == 'get list':
            userID = List[1]

            flag = FUNC.getList(userID)
            self.request.sendall(bytes(flag, 'utf8'))

        if List[0] == 'register':
            account = List[1]
            pw = List[2]
            flag = FUNC.register(account,pw)
            self.request.sendall(bytes(flag, 'utf8'))

if __name__ == '__main__':

    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8009), MyServer)

    server.serve_forever()






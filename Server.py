import socketserver
import os     #运行shell命令


class MyServer(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()     #得到一个1kb的请求
        List = self.data.split('#')                     #用'#'分割

        if List[0] == 'log in':                         #登陆
            account = List[1]
            pw = List[2]

        if List[0] == 'log out':                        #登出
            func = List[1]

        if List[0] == 'send url':
            url = List[1]
            os.system('download url')        #这里写linux内下载命令 比如axel + url

        if List[0] == 'get url':
            self.request.sendall('url')                 #服务器的


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('23.83.250.163', 6091), MyServer)
    server.serve_forever()





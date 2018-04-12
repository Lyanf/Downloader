import socket

s = socket.socket()
serverIP = '23.83.250.163'
port = 6091
address = (serverIP,port)
try:
    s.connect(address)
except:
    print('服务器连接失败')

linkType = {0:'log in',1:'log out',2:'send url',3:'get download url'}
s.send()
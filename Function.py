import socket
HOST = '127.0.0.1'    # The remote host
PORT = 8009             # The same port as used by the server




def login(userID,userPW):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('log in#'+userID+'#'+userPW,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data

def register(userID,userPW):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('register#'+userID+'#'+userPW,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data

def sendURL(userID,URL):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('send url#'+userID+'#'+URL,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data

def getURL(userID,fileName):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('get url#'+userID+'#'+fileName,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data

def getList(userID):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('get list#'+userID,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data

def delete(userID,fileName):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(bytes('delete#'+userID+'#'+fileName,encoding='utf8'))
    data = s.recv(1024)
    s.close()
    return data
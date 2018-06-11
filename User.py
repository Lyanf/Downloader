from Function import *
class User:
    def __init__(self):
        self.userName = ''
        self.passWord = ''
        self.fileList = []
        self.fileListStr = ''
    def signIn(self,userName,password):
        get = register(userName,password).decode()
        if get == '1':
            return True
        else:
            return False

    def logIn(self,userName,password):
        get = login(userName,password).decode()
        if get == '1':
            self.userName = userName
            self.passWord = password
            fileStr = getList(userName).decode()
            self.fileListStr = fileStr
            assert isinstance(fileStr,str)
            for i in fileStr.split('#'):
                self.fileList.append(i)
            return True
        else:
            return False
    def logOut(self):
        self.userName = ''
        self.passWord = ''
        self.fileList = []

    def getUserName(self):
        return self.userName.decode()

    def getUrl(self,filename):
        return getURL(self.userName,filename).decode()

    def sendUrl(self,url):
        sendURL(self.userName,url)

    def reLogIn(self):
        self.logIn(self.userName,self.passWord)

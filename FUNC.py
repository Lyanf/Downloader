import sqlite3
import os

def login(account,pw):
    while 1:
        user_ID = account
        sql = sqlite3.connect("user.db")
        data = sql.execute("select * from user where id='%s'" % user_ID).fetchone()
        sql.close()
        if data:
            if data[1] == pw:

                return '1'
            else:
                return '2'
        else:
            return '3'

def register(account,pw):
    while 1:
        user_ID = account
        sql = sqlite3.connect("user.db")
        data = sql.execute("select * from user where id='%s'" % user_ID).fetchone()
        if not data:
            user_PW = pw
            sql.execute("insert into user(id,pw) values(?,?)",
                        (user_ID, user_PW))
            sql.commit()
            print("添加成功")
            sql.execute("create table '%s'(file varchar(50) primary key,URL varchar(200))" % user_ID)



            sql.commit()
            os.system('mkdir ' + account)
            print("文件目录已创建")
            sql.close()
            return '1'
            break
        else:
            print("用户已存在")
            sql.close()
            return '2'
            break

def sendURL(userID,URL):
    while 1:
        fileName = URL.split(r'/')[-1]
        os.system('cd ' + userID)
        os.system('wget ' + URL)
        newURL = 'liyanfeng.xyz/downloader/'+userID+'/'+fileName


        sql = sqlite3.connect("user.db")
        sql.execute("insert into '%s'(file,URL) values(?,?)" % userID,(fileName,newURL))
        sql.commit()
        sql.close()

        os.system('cd ..')
        return '这里下载文件'+fileName+'并入库'
        break


def getURL(userID, fileName):
    while 1:


        sql = sqlite3.connect("user.db")
        data = sql.execute("select * from '%s' where file = ?" % userID, (fileName,)).fetchone()
        sql.close()
        flag = data[1]
        return flag
        break

def getList(userID):
    while 1:
        sql = sqlite3.connect("user.db")
        cursor = sql.cursor()
        data = cursor.execute("select file from '%s'" % userID).fetchall()
        cursor.close()
        sql.close()
        fileList = [x[0] for x in data]
        flag = ''
        for i in range(0, len(fileList)):
            flag = flag+'#'+fileList[i]
        return flag
        break

import sqlite3



def create_tableUser():
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    cursor.execute('create table user(id varchar(20) primary key,pw varchar(20))')
    cursor.close()

create_tableUser()




import Function
data = Function.register('TianAndrew','123').strip().decode()
print(data)

data = Function.login('TianAndrew','123').strip().decode()
if data == "1":
    print("成功登陆")

if data == "2":
    print("账号错误")

if data == "3":
    print("密码错误")

data = Function.sendURL('TianAndrew','www.baidu.con/test/test.txt').strip().decode()
print(data)

data = Function.sendURL('TianAndrew','www.google.con/test/Game.db').strip().decode()
print(data)

data = Function.getURL('TianAndrew','test.txt').strip().decode()
print(data)

data = Function.getList('TianAndrew').strip().decode()
print(data)

#data = Function.delete('TianAndrew','fileName').strip().decode()
#print(data)
# Downloader
客户端函数 都是输入 返回值 都是字符串
Function.login    (userID,userPW)  :登陆        返回值：1成功 2密码错误 3不存在账号
Function.register (userID,userPW)  :注册        返回值：1成功 2用户已存在
Function.sendURL  (userID,URL)     :发送要下载的链接给服务器        返回值：还没定 想要和其他的统一 找不到链接之类的，目前是'这里下载文件'+fileName+'并入库'
Function.getURL   (userID,fileName):获取服务器端的地址           返回值：服务器端的地址，也就是客户端的下载链接
Function.getList  (userID)         :获取用户的离线列表           返回值：文件名列表 用"#"分割

删除还没做 真删除的话就直接
os.system("cd "+userID)
os.system("rm "+fileName)
然后数据库删除那一条就行
假删除看怎么删 再看看？

Client.Function是客户端功能函数
第一次运行要运行
Server.database 创建user库
然后运行
Server就行

FUNC封装了Server里的方法

流程大概是
注册（user表加一条数据 新建一个userName的表 新建一个空目录）
登陆
提交链接（userName表里写入文件名+新链接 在userName目录下下载）
获取fileList
获取file的新链接

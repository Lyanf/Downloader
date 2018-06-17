# 软件简介

本软件是一个多功能的下载器，支持在线下载和离线下载，其中在下载过程中支持断点续传、多线程下载等功能。

# 软件结构

1. 本程序分为客户端和服务器端，其中服务端与客户端进行交互，下载客户端传递过来的文件，并返回新生成的url，让客户端可以从该服务器上进行高速下载。

2. 本程序的基础功能是下载，逻辑为输入一个url，下载器即开始进行多线程/断点续传。

3. 在使用离线下载时，必须先进行注册/登录，然后对服务器发出离线请求，在服务器下载过程中，程序不断向服务器发出请求，若服务器离线完毕，则返回一个新的url，进行客户端和服务端之间的数据传输。

4. 软件的结构图如下：

![软件整体结构](https://raw.githubusercontent.com/Lyanf/Downloader/test/img/struct.png "软件结构图")
----------
# 软件模板方案
### 模块划分
本程序大致分为以下模块：

1. GUI模块
2. 服务器/客户端交互模块
3. 服务器端
4. 在线下载模块
5. 数据库模块

### GUI模块
* 该模块使用pyqt5进行编写，主要提供用户与程序交互的图形化接口，通过该接口可以实现本程序所有功能。
    - 新建、开始、删除任务，提交离线下载
    - 实时显示当前下载进程
* GUI绘图占据主线程，所有有绘图需求(要展示到GUI上面)均通过pyqt中的信号——信号槽机制进行传递。
* GUI界面初版如下：

    <img src="https://raw.githubusercontent.com/Lyanf/Downloader/test/img/2.png" width="400" height="300">
### 服务器/客户端交互模块
使用python的socket编程，对于服务器和客户端进行交互，当程序有和服务器进行交互的需求时，调用该模块的函数。对于各需求预设了方法，主要有以下几项：

1. 注册、登录请求发往服务器————服务器回复登录状态
2. 离线下载请求发往服务器————服务器回复是否开始下载
3. 离线取回请求发往服务器————服务器返回url

### 服务器端
服务器端主要是在接收到客户端的离线下载请求后，调用linux的shell，使用wget进行下载，同时需要搭建nginx文件服务器，使得返回的url对于远程客户端来说是权限可达的。

### 在线下载模块
* 首先构建了对于某个已知url的http模式的下载的部分下载函数(即对于该文件进行部分请求，下载其文件的一部分)
* 将部分下载函数进行多线程封装，任务下载函数管理从属于本任务的多部分下载，即对于单个任务实现了多线程下载。
* 对于单个任务下载进行多线程封装，即实现了多任务、多线程下载。
* 在下载过程中，每个任务的每个线程维护一个临时文件，待所有临时文件下载完毕，进行整合，即下载好的文件。

### 数据库模块
数据库模块在服务器端，负责管理用户名及密码，以及该用户提交的离线下载任务，具体情况将在数据结构分析中进行介绍。

# 数据结构分析
- MySignal
: 该类继承自pySignal，并且实例化于一个单独的文件内，其他文件想用这个实例，需要将其import进来，事实上发挥了全局变量的作用。
该数据结构的作用是，在不同的线程之间进行信息传递，主要用于功能函数向GUI线程中传递绘图指令及参数
- DownloadTask
: 该类抽象一个下载任务，利用一个url进行初始化，并且可以设置该下载任务的下载地址、下载线程数等有关于下载任务的参数。初始化完毕后可以获取该下载任务的大小、名称，因为要进行多线程下载，所以该类还负责对文件大小及下载范围进行划分，从而分配给各个下载线程。
- Downloader
: 该类对于下载器进行抽象，在其中保存下载任务，并使用该实例变量的方法进行下载
- PyQt
: 
    - MainWindow:程序GUI的主界面
    - ListPage:下载详情列表
* 数据库
: 
使用sqlalchemy对数据库进行操作，便于后期迁移。
    * 总用户表（用户名、密码）
    * 单个用户表（用户名、离线下载提交的url、文件名）

    其中总用户表用来记录所有用户的登录信息，每个用户都有自己一个表，用于记录该用户的离线下载的相关操作。其中总用户表和单个用户表通过用户名相连接。

# 项目地址
[Github Click Here](https://github.com/Lyanf/Downloader)

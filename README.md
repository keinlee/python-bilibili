# Python-bilibili-danmu

## 一、日志更新

### 5.2017年9月13日更新，文件夹为bilibili<br>
（1）添加文件夹bilibili，将项目进行拆分，只需要运行main.py即可<br>

（2）添加哔哩哔哩登陆状态相关代码<br>

（3）为了保障账号安全，在roomcookies.py中的删除了相关cookies，需要添加自己账号相关的cookies<br>

（4）不进行任何代码修改的话，可以直接运行main.py获取弹幕<br>

（5）该文件夹的内容基于8月更新，没有后续添加数据库和字符过滤<br>

（6）上传之前还删除了房管自动感谢和命令封禁，暂时不上线<br>

### 4.2017年9月2日更新，文件名为bilibili_zip.py<br>
（1）添加pymysql第三方库<br>

（2）使用并连接MySQL数据库，添加数据表创建和弹幕、礼物数据存入数据库操作<br>

（3）运行该版本需要在数据库中创建test数据库，否则会报错<br>

（4）在MySQL中使用以下命令，创建默认编码字符为UTF8数据库<br>
    CREATE DATABASE test DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;<br>

（5）在MySQL中使用以下命令（test数据库名），查询数据库的字符集<br>
    SHOW CREATE DATABASE test;<br>
    SHOW VARIABLES LIKE '%char%';<br>

（6）在选择数据库后，使用以下命令（test是数据库名，bili_danmu是数据表名），查询数据表字符集<br>
    SHOW CREATE TABLE bili_danmu;<br>
    SHOW TABLE STATUS FROM test LIKE 'bili_danmu';<br>

（7）在MySQL中使用以下命令（test是数据库名，bili_danmu是数据表名），查询数据表中列信息<br>
    SHOW FULL COLUMNS FROM bili_danmu FROM test;<br>

### 3.2017年9月1日更新，文件名为bilibili_zip.py<br>
（1）添加过滤Emoji表情代码，Python3中的shell不支持4位字节显示会出错，直接替换为\u274e的"❎"Emoji表情<br>

（2）删除Non-BMP字符集和替换相关代码<br>
    self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)<br>
    content.translate(self.non_bmp_map))<br>

### 2.2017年8月更新，文件名为bilibili_zip.py<br>
（1）基本框架没有更新，数据解析新增一个zlib库，由原来的"protover":0，变成"protover":2。为0的情况数据接受后是可以直接解析的，为2的情况下数据是乱码，即gzip格式的数据，需要将数据解压后才能解析<br>

（2）哔哩哔哩的服务器端口变化：由原来的788端口，变成2243端口。这个可以GET请求/api/player?id=cid: 后面加房间号可以看到现在的弹幕端口变成了2243端口。原来的788端口也是可以用的<br>

（3）重新编辑README.md，使用Markdown语法进行格式排版<br>


### 1.2017年2月上传，文件名为bilibili.py<br>
（1）基本实现能够获取指定直播间弹幕<br>

（2）应用的库有：re、sys、time、json、socket、struct、random、threading、http.client、urllib.request、lxml<br>
&emsp;&emsp;re:正则表达式用于匹配网页<br>
&emsp;&emsp;sys:emoji表情不能正常解析，需要sys支持<br>
&emsp;&emsp;time:添加时间<br>
&emsp;&emsp;lxml:Xpath匹配网页<br>
&emsp;&emsp;json:解析json数据<br>
&emsp;&emsp;socket:用于数据发送和接受<br>
&emsp;&emsp;struct:用于数据打包和拆包<br>
&emsp;&emsp;random:随机数生成<br>
&emsp;&emsp;threading:多线程应用<br>
&emsp;&emsp;http.client:http请求<br>
&emsp;&emsp;urllib.request:打开网页<br>
    


## 二、技术解析

前面的网页匹配内容直接略过，重点分析网页异步数据。所谓的异步（ajax）就是不重新加载整个页面的情况下，更新网页某一部分的数据。弹幕就属于这个异步加载<br>

1.先关闭其他网页应用，单单请求哔哩哔哩网站。用wireshark分析，条件筛选为http，根据这个http条件筛选出来的数据不多，再找房间号相关的http请求,然后一条条追踪流，可以找到/api/player?id=cid:这个请求。追踪流可以发现弹幕端口是2243端口和弹幕服务器为livecmt-2.bilibili.com<br>

2.设置筛选条件为tcp.port==2243，查看\[PSH, ACK]样式的请求，这样的请求是包含数据的。很快可以发现一条与其他不一样的数据，其中能够看到roomid是所输入的房间号，这个就是服务器请求发送数据的指令，发送这个指令后，服务器就会发送弹幕<br>

3.当我们追踪这个流时，发现后面时不时会出现"......"这样的数据，分析发现这样的数据格式是一样的，而且时间是每隔30s，这个是心跳包，保持客户端与服务器之间的联系不中断。如果不发送这个心跳包，你会发现30s过后服务器就断开连接了<br>

4.追踪roomid这个流时，我们可以看到前面还有两个关键词一个是uid，还有一个是protover。uid是随机生成的一串数字，protover推测是弹幕发送的格式。手机客户端追踪的时候，protover是为0的，电脑浏览器追踪protover是2。还有一个很明显的区别就是当protover为0，弹幕的格式能够清楚的看出来，当protover为2时，弹幕的格式就是乱码，这个问题困扰了我好久，后来才知道这个是传输中的gzip压缩包格式，需要解压后才能看到源数据<br>

5.用Python编写程序，思路为向弹幕服务器（livecmt-2.bilibili.com）发送{"uid":xxxxx,"protover":0,"roomid":xxxxxxxxx}格式指令，再发送心跳包指令，每隔30秒发送一次心跳包，再json解析收到的数据，即可获得弹幕<br>

6.对于Emoji表情的问题，Python3只支持2-3位字节的Emoji,所以需要将4字节的Emoji替换或者删除掉，减少出错率<br>

7.Python3不支持mysqldb第三方库，故采用pymyql第三方库，创建数据库、数据表以及存入数据的时候记得都要设置编码为utf8(默认的字符编码是latin1，不支持中文)，不然存储中文会出现错误<br>

8.登陆的话采用的是直接copy网站请求头中的cookies，因为B站验证码采用的是滑动验证，需要用Selenium+Phantomjs模式运行，而这种运行会消耗大量的cup，目前没有打算采用这种模式模拟登陆<br>
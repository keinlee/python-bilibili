# Python-bilibili-danmu

## 一、日志更新

### 1.2017年2月上传本项目，项目名为bilibili.py<br>
（1）基本实现能够获取指定直播间弹幕<br>

（2）应用的库有：re、sys、time、json、socket、struct、random、threading、http.client、urllib.request、lxml<br>
  re:正则表达式用于匹配网页<br>
  sys:emoji表情不能正常解析，需要sys支持<br>
  time:添加时间<br>
  lxml:Xpath匹配网页<br>
  json:解析json数据<br>
  socket:用于数据发送和接受<br>
  struct:用于数据打包和拆包<br>
  random:随机数生成<br>
  threading:多线程应用<br>
  http.client:http请求<br>
  urllib.request:打开网页<br>
    
    
### 2.2017年8月更新本项目，项目名为bilibili_zip.py<br>
（1）基本框架没有更新，数据解析新增一个zlib库，由原来的"protover":0，变成"protover":2。为0的情况数据接受后是可以直接解析的，为2的情况下数据是乱码，即gzip格式的数据，需要将数据解压后才能解析<br>

（2）哔哩哔哩的服务器端口变化：由原来的788端口，变成2243端口。这个可以GET请求/api/player?id=cid: 后面加房间号可以看到现在的弹幕端口变成了2243端口。原来的788端口也是可以用的<br>

（3）重新编辑README.md，使用Markdown语法进行格式排版<br>


## 二、技术解析

前面的网页匹配内容直接略过，重点分析网页异步数据。所谓的异步（ajax）就是不重新加载整个页面的情况下，更新网页某一部分的数据。弹幕就属于这个异步加载<br>

1.先关闭其他网页应用，单单请求哔哩哔哩网站。用wireshark分析，条件筛选为http，根据这个http条件筛选出来的数据不多，再找房间号相关的http请求,然后一条条追踪流，可以找到/api/player?id=cid:这个请求。追踪流可以发现弹幕端口是2243端口和弹幕服务器为livecmt-2.bilibili.com<br>

2.设置筛选条件为tcp.port==2243，查看\[PSH, ACK]样式的请求，这样的请求是包含数据的。很快可以发现一条与其他不一样的数据，其中能够看到roomid是所输入的房间号，这个就是服务器请求发送数据的指令，发送这个指令后，服务器就会发送弹幕<br>

3.当我们追踪这个流时，发现后面时不时会出现"......"这样的数据，分析发现这样的数据格式是一样的，而且时间是每隔30s，这个是心跳包，保持客户端与服务器之间的联系不中断。如果不发送这个心跳包，你会发现30s过后服务器就断开连接了<br>

4.追踪roomid这个流时，我们可以看到前面还有两个关键词一个是uid，还有一个是protover。uid是随机生成的一串数字，protover推测是弹幕发送的格式。手机客户端追踪的时候，protover是为0的，电脑浏览器追踪protover是2。还有一个很明显的区别就是当protover为0，弹幕的格式能够清楚的看出来，当protover为2时，弹幕的格式就是乱码，这个问题困扰了我好久，后来才知道这个是传输中的gzip压缩包格式，需要解压后才能看到源数据<br>

5.用Python编写程序，思路为向弹幕服务器（livecmt-2.bilibili.com）发送{"uid":xxxxx,"protover":0,"roomid":xxxxxxxxx}格式指令，再发送心跳包指令，每隔30秒发送一次心跳包，再json解析收到的数据，即可获得弹幕

1.在wireshock分析中

（1）过滤规则设置为“tcp.port==788”发现直播主机IP为：101.69.131.11
客户端发送的tcp[PSH, ACK]中，进入直播间的数据  3c为数据包长度

（已登录状态）
0000   00 00 00 3c 00 10 00 01 00 00 00 07 00 00 00 01  ...<............
0010   7b 22 75 69 64 22 3a 33 32 37 38 33 34 35 35 2c  {"uid":32783455,
0020   22 70 72 6f 74 6f 76 65 72 22 3a 32 2c 22 72 6f  "protover":2,"ro
0030   6f 6d 69 64 22 3a 33 31 34 34 31 7d              omid":31441}

（未登录状态）
0000   00 00 00 36 00 10 00 01 00 00 00 07 00 00 00 01  ...6............
0010   7b 22 72 6f 6f 6d 69 64 22 3a 34 32 30 31 32 2c  {"roomid":42012,
0020   22 75 69 64 22 3a 32 31 32 30 30 30 36 39 33 35  "uid":2120006935
0030   34 36 30 30 38 7d                                46008}

服务端：（把弹幕发过来了...）
0000   00 00 00 10 00 10 00 01 00 00 00 08 00 00 00 01  ................

每隔30秒
客户端发送的tcp[PSH, ACK]中，有一个数据包（16bt心跳包）
0000   00 00 00 10 00 10 00 01 00 00 00 02 00 00 00 01  ................

服务端响应的tcp[PSH, ACK]中，回复数据包（在线人数4701）
0000   00 00 00 14 00 10 00 01 00 00 00 03 00 00 00 01  ................
0010   00 00 12 5d                                      ...]

（2）过滤规则设置为“http.request.method=="GET"”发现网站主机IP为：221.204.199.135
客户端发送http中
GET /api/player?id=cid:31441&ts=159cff133b1 HTTP/1.1
Host: live.bilibili.com

追踪流http

服务端：
<uid>32783455</uid>
<uname>.....................</uname>
<login>true</login>
<isadmin>0</isadmin>
<time>1485248118</time>
<rank>10000</rank>
<level>35</level>
<state>LIVE</state>
<chatid>31441</chatid>
<server>livecmt-2.bilibili.com</server>
<sheid_user></sheid_user>
<block_time>0</block_time>
<block_type>0</block_type>
<room_shield>1</room_shield>
<level_sheid>0</level_sheid>
<user_sheid_keyword>......</user_sheid_keyword>
<room_silent_type></room_silent_type>
<room_silent_level>0</room_silent_level>
<room_silent_second>0</room_silent_second>
<user_silent_level>0</user_silent_level>
<user_silent_rank></user_silent_rank>
<user_silent_verify>1</user_silent_verify>
<vip>0</vip>
<msg_mode>1</msg_mode>
<msg_color>16777215</msg_color>
<msg_length>30</msg_length>
<need_authority>0</need_authority>
<authority_range>......</authority_range>
<forbidden>0</forbidden>

发现弹幕主机域名：livecmt-2.bilibili.com 
ping livecmt-2.bilibili.com  发现IP为101.69.131.11
由此可得到弹幕姬的主机端口是788

（3）过滤规则设置为“tcp contains "info" and ip.src==101.69.131.11”发现弹幕数据包
根据"cmd"可分为：
DANMU_MSG
WELCOME
SEND_GIFT
SYS_MSG
(编码显示为：UTF-8)

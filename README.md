1.��wireshock������
��1�����˹�������Ϊ��tcp.port==788������ֱ������IPΪ��101.69.131.11
�ͻ��˷��͵�tcp[PSH, ACK]�У�����ֱ���������  3cΪ���ݰ�����
���ѵ�¼״̬��
0000   00 00 00 3c 00 10 00 01 00 00 00 07 00 00 00 01  ...<............
0010   7b 22 75 69 64 22 3a 33 32 37 38 33 34 35 35 2c  {"uid":32783455,
0020   22 70 72 6f 74 6f 76 65 72 22 3a 32 2c 22 72 6f  "protover":2,"ro
0030   6f 6d 69 64 22 3a 33 31 34 34 31 7d              omid":31441}
��δ��¼״̬��
0000   00 00 00 36 00 10 00 01 00 00 00 07 00 00 00 01  ...6............
0010   7b 22 72 6f 6f 6d 69 64 22 3a 34 32 30 31 32 2c  {"roomid":42012,
0020   22 75 69 64 22 3a 32 31 32 30 30 30 36 39 33 35  "uid":2120006935
0030   34 36 30 30 38 7d                                46008}
����ˣ����ѵ�Ļ��������...��
0000   00 00 00 10 00 10 00 01 00 00 00 08 00 00 00 01  ................

ÿ��30��
�ͻ��˷��͵�tcp[PSH, ACK]�У���һ�����ݰ���16bt��������
0000   00 00 00 10 00 10 00 01 00 00 00 02 00 00 00 01  ................

�������Ӧ��tcp[PSH, ACK]�У��ظ����ݰ�����������4701��
0000   00 00 00 14 00 10 00 01 00 00 00 03 00 00 00 01  ................
0010   00 00 12 5d                                      ...]

��2�����˹�������Ϊ��http.request.method=="GET"��������վ����IPΪ��221.204.199.135
�ͻ��˷���http��
GET /api/player?id=cid:31441&ts=159cff133b1 HTTP/1.1
Host: live.bilibili.com

׷����http

����ˣ�
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

���ֵ�Ļ����������livecmt-2.bilibili.com 
ping livecmt-2.bilibili.com  ����IPΪ101.69.131.11
�ɴ˿ɵõ���Ļ���������˿���788

��3�����˹�������Ϊ��tcp contains "info" and ip.src==101.69.131.11�����ֵ�Ļ���ݰ�
����"cmd"�ɷ�Ϊ��
DANMU_MSG
WELCOME
SEND_GIFT
SYS_MSG
(������ʾΪ��UTF-8)
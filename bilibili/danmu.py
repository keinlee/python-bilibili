import json
import time
import sys

def nowtime():
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('[%s]'%nowTime,end='')


def danmu(dic):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    sendor = dic['info'][2][1]
    content = dic['info'][1]
    isadmin = dic['info'][2][2]
    isVIP = dic['info'][2][3]
    if dic['info'][3]:
        medal = dic['info'][3][1]
        grade = dic['info'][3][0]
        medal = ' [' + medal +' ' + str(grade) +']'
    else:
        medal=''
        
    if isadmin:                         
        msg='[房管]【'+sendor+"】：" + content.translate(non_bmp_map)        
    else:
       msg = medal+'【'+sendor+'】：' + content.translate(non_bmp_map)
    return msg
    
    

def gift(dic):
    giftName = dic['data']['giftName']
    giftNum = dic['data']['num']
    sendor = dic['data']['uname']
    msg='【'+ sendor +'】' + "赠送" + str(giftNum) + '个' + giftName
    return msg
     
    
    
def welcome(dic):
    isvip = dic['data']['uname']
    isadmin = dic['data']['isadmin']
    if isadmin:
        msg=" 欢迎【房管】【%s】老爷进入直播间"%isvip
    else:
        msg= " 欢迎【%s】老爷进入直播间"%isvip
    
    return msg
        
def guard(dic):
    guard = dic['data']['username']
    msg= " 欢迎【" + guard +"】守护进入直播间"
    return msg
    
    
def SysGift(dic):
    msg = dic['msg']
    msg = msg.replace(':?','')
    msg = " 礼物公告："+ msg
    return msg
   
    
def SysMsg(dic):
    msg = dic['msg']
    msg = msg.replace(':?','')
    return msg
    #系统公告、小电视
    
    
 
def Info(msgData):
    try:
        dic  = json.loads(msgData)
    except json.decoder.JSONDecodeError as r:
        print(msgData)
    cmd = dic['cmd']
    if cmd=='DANMU_MSG':
        #print(dic)
        info = danmu(dic)
        
    elif cmd == 'SEND_GIFT':
        info= gift(dic)
    elif cmd =='ROOM_BLOCK_USER':
        uname = dic['uname']
        info = uname + '已被房管禁言'
        #print("封禁")
        #print(dic)
    elif cmd == 'WELCOME':
        info=welcome(dic)
    elif cmd =='WELCOME_GUARD':
        info=guard(dic)   
    elif cmd =='SYS_GIFT':
        info=SysGift(dic)
        #print(dic)
    elif cmd == 'SYS_MSG':
        info=SysMsg(dic)
    elif cmd == 'LIVE':
        nowtime() 
        info='===主播开始直播啦==='
        print(dic )
    elif cmd == 'PREPARING':
        nowtime()
        info='===主播关闭直播啦==='
        print(dic)
    else:
        info = dic
        print(dic)
    return info
#弹幕样本        
'''
#弹幕
{"info":[[0,1,25,16777215,1497497239,473249355,0,"e87439f2",0],"崩",[32378732,"Lovemiko殿下",0,0,0,10000,1],
[7,"下限","下限酱Orz",149,5805790],[18,0,6406234,">50000"],["title-58-1","title-58-1"],0,0],"cmd":"DANMU_MSG"}

#礼物
{"cmd":"SEND_GIFT","data":{"giftName":"亿圆","num":1,"uname":"泓伊豆Cic","rcost":250095249,"uid":490225,"top_list":[],
"timestamp":1497497232024,"giftId":6,"giftType":0,"action":"赠送","super":0,"price":1000,"rnd":"1234617158","newMedal":0,
"newTitle":0,"medal":1,"title":"","beatId":0,"remain":0,"eventScore":0,"eventNum":0,"notice_msg":[],
"capsule":{"normal":{"coin":17,"change":0,"progress":{"now":6000,"max":10000}},
"colorful":{"coin":0,"change":0,"progress":{"now":0,"max":5000}}}}}

#欢迎
{"cmd":"WELCOME","data":{"uid":1527837,"uname":"\u9ea6\u5c6f\u7684\u5c0f\u8bb8","isadmin":0,"vip":1},"roomid":5279}

#守护
{'cmd': 'WELCOME_GUARD', 'data': {'uid': 10828760, 'username': 'Koutatsu', 'guard_level': 3}, 'roomid': 5279}

#小电视
{'cmd': 'SYS_MSG', 'msg': '【红秋落叶】:?在直播间:?【1012】:?赠送 小电视一个，请前往抽奖', 'rep': 1, 'styleType': 2,
'url': 'http://live.bilibili.com/1012', 'roomid': 1012, 'real_roomid': 1012, 'rnd': 1497498366, 'tv_id': '21977'}

#系统
{'cmd': 'SYS_MSG', 'msg': '恭喜本次弹幕抽奖获得小米Max 2的观众，大家都记得来发弹幕哟！',
'url': 'http://live.bilibili.com/545342', 'rep': 1, 'styleType': 1}

#封禁
{'cmd': 'ROOM_BLOCK_MSG', 'uid': '14568052', 'uname': '额，大丶帅比', 'roomid': 378236}

#礼物公告
{'cmd': 'SYS_GIFT', 'msg': '种花老K:?  在亚洲图片的:?直播间1149:?内赠送:?74:?连击X50', 'rnd': 1498030147, 'uid': 1376364}
'''
    
               
        
 

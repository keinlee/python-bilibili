import sys
import time
from server import *
from data import *
from danmu import *
from roomcookies import *
from operation import *
import threading


def thread(s):
    threads = []
    t1 = threading.Thread(target=heartBeat,args=(s,))
    threads.append(t1)
    

    t1.setDaemon(True)#设置t1守护线程 随主程序一同退出
    t1.start()

def loop(s):
    count = 0
    while True:
        msgData,net = recvData(s)
        if not net:
            break
        
        choose = dealData(msgData,count)
        count+=1
        
        if not choose:
            continue
        else:
            msgData = msgData.decode('utf-8',errors='ignore')
            #print(msgData)
        info = Info(msgData)
        nowtime()
        print(info)
        #autosend(info,roomId,BlackCookies,SendCookies)
    
        
def nonet(NoNet):
    nowtime()
    if NoNet <= 6:
        print('网络请求失败，请检查网络...30秒后重试')
        time.sleep(30)
    elif NoNet <= 12:
        print('网络请求失败，请检查网络...1分钟后重试')
        time.sleep(60)
    elif NoNet <= 19:
        print('网络请求失败，请检查网络...3分钟后重试')
        time.sleep(180)
    elif NoNet <= 25:
        print('网络请求失败，请检查网络...5分钟后重试')
        time.sleep(300)
    else:
        print('由于长时间无网络，程序退出...')
        sys.exit()
    

if __name__ == '__main__':
    webPage = enterRoom()
    roomId,upName = getTitle(webPage)
    NoNet=0
    while True:
        EnterCookies,SendCookies,BlackCookies = get_cookies()
        #登录进直播间
        result = cookEnter(roomId,EnterCookies)
        if not result:
            NoNet += 1
            nonet(NoNet)
            continue
        else:
            NoNet=0
            print()
            print('成功登录直播间【%d】'%roomId)  
        #获取弹幕服务器
        server = getServer(roomId,upName)
        #print(server)
        s = socketName()
        #链接弹幕服务器
        sendData(server,s,roomId)
        #心跳包
        thread(s)
        loop(s)
        
        time.sleep(30)
        continue
    
    

    
    
    


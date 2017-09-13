from roomcookies import *
import json
import urllib.request
import http.client

def cookGetask(URL,headers):
    
    request = urllib.request.Request(URL,headers = headers)
    try:
        response = urllib.request.urlopen(request)
        result = response.read().decode('utf-8')
    except  (urllib.error.URLError,TimeoutError,http.client.IncompleteRead,http.client.RemoteDisconnected) as reason:
        print('GET失败：',end='')
        print(reason)
        result = ''
    return result

def cookPostask(URL,data,headers):
    request = urllib.request.Request(URL,data=data,headers = headers)
    try:
        response = urllib.request.urlopen(request)
        result = response.read().decode('utf-8')
    except (urllib.error.URLError,TimeoutError,http.client.IncompleteRead,http.client.RemoteDisconnected) as reason:
        print('POST失败：',end='')
        print(reason)
        result = ''
    return result

def cookBlack(roomId,BlackCookies,uname,hour):
        BlackUrl = "http://api.live.bilibili.com/liveact/room_block_user"
        roomUrl = 'http://live.bilibili.com/' + str(roomId)
        BlackHeader = black_header(BlackCookies,roomUrl)
        BlackData = black_user_data(uname,hour,roomId)
        result= cookPostask(BlackUrl,BlackData,BlackHeader)
        dic = json.loads(result)
        code = dic['code']
        if code ==0:
            uid = dic['data']['id']
            uname = dic['data']['uname']
            result =  "成功屏蔽 ["+uname +"]\t封禁ID：" + uid
            print("成功屏蔽 [%s]\t封禁ID：%s"%(uname,uid))
        elif code ==-400 or code ==-101 or code ==-403:
            msg = dic['msg']
            result =  "封禁失败\t"+msg 
            print("封禁失败\t原因：%s"%msg)
        else:
            result =  "封禁失败"
            print("封禁失败")
            print(dic)
        return result

def cookEnter(roomId,EnterCookies):
    roomUrl = "http://live.bilibili.com/"+str(roomId)
    EnterHeader = room_header(EnterCookies)
    result =cookGetask(roomUrl,EnterHeader)
    return result

def cookSend(roomId,SendCookies,msg):
    SendUrl = "http://live.bilibili.com/msg/send"
    SendHeader = send_header(SendCookies)
    SendData = send_data(msg,roomId)
    result= cookPostask(SendUrl,SendData,SendHeader)
    #print(result )
    try:
        dic = json.loads(result)
        info = dic['msg']
        if info:
            print('%s\t发送失败\t原因：%s'%(msg,info))
    except json.decoder.JSONDecodeError:
        pass
    
    




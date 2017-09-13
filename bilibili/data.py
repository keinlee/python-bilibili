import socket
import random
import struct
import time

def nowtime():
      nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
      print('[%s]'%nowTime,end='')

def socketName():
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      return s
      
def sendData(server,s,roomId):
    s.connect((server,2243))
    print("连接弹幕服务器：%s:%d"%(s.getpeername()[0],s.getpeername()[1]))
    print()
    uid = int(100000000000000.0 + 200000000000000.0*random.random())
    body = '{"roomid":%d,"uid":%d}'%(roomId,uid)
    bodyCode = body.encode('utf-8')
    dataLen =len(bodyCode) + 16
    dataFront = struct.pack('!iHHII',dataLen,16,1,7,1)
    data = dataFront + bodyCode
    try:
        s.send(data)
    except ConnectionResetError:
        print('服务器连接失败，正在尝试重新连接...')
        time.sleep(3)
        sendData(server,s,roomId)
    print('成功连接服务器')
    
    
    

def recvData(s):
      net= True
      try:
            msgHead = s.recv(16)
      except (ConnectionResetError,TimeoutError,ConnectionAbortedError) as reason:
            print("="*70)
            nowtime()
            print(reason)
            msgData= ''
            net= False
            return msgData,net
       
      if not len(msgHead) or len(msgHead) <16:
        print("="*70)
        nowtime()
        print('服务器断开连接')
        msgData= ''
        net= False
        return msgData,net
       #接收数据过大
      msgHead = struct.unpack('!iHHII',msgHead)
      msgLen = msgHead[0]
      msgData = s.recv(msgLen-16)
      while True:
            if msgLen - 16 > len(msgData):
                   RestmsgData = s.recv(msgLen-16-len(msgData))
                   msgData += RestmsgData
            else:
                   break

      return msgData,net


def  dealData(msgData,count):
    choose = 1
    if not msgData:
        choose = 0
    elif len(msgData) == 4:
        msgData =struct.unpack('!i',msgData)
        choose = 0
        #print(count)
        if  count%10==1:
            nowtime()
            print("当前在线人数：%d"%msgData)
        
    else:
        choose = 1      
    return choose
        
def heartBeat(s):
      while True:
            heartbeat = struct.pack('!iHHII',16,16,1,2,1)
            try:
                  s.send(heartbeat)
            except ConnectionResetError as reason:
                  nowtime()
                  print('线程退出：',end='')
                  print(reason)
                  print("="*70)
                  break
            time.sleep(30)
               






               

import re
import sys
import zlib
import time
import json
import struct
import socket
import random
import pymysql
import threading
import http.client
import urllib.request
from lxml import etree



class client():
     def __init__(self):
          self.liveUrl='http://live.bilibili.com'
          self.roomId = 0
          self.host = 'live.bilibili.com'
          self.port = 2243
          self.protover = 0
               
     def getServer(self):
          while True:
               #测试房间号
               roomId = input('请输入房间号：')
               while not roomId.isdigit():
                    print("格式错误，请重新输入！")
                    roomId = input('请输入房间号：')
                    
               roomUrl = self.liveUrl +'/'+ str(roomId)
               #测试网址
               webheaders = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
               req = urllib.request.Request(url=roomUrl, headers=webheaders)
               try:
                    webPage=urllib.request.urlopen(req)
                    break
               except urllib.error.HTTPError as reason:
                    print('网址出错啦！'+ str(reason))
                    
          #获取直播间号
          html = webPage.read().decode('utf-8')
          m = re.findall(r'ROOMID\s=\s(\d+)', html)
          ROOMID = m[0]
          self.roomId = int(ROOMID)
          print('正在进入【%d】房间...'%self.roomId)
          #获取直播间标题
          html = etree.HTML(html)
          title = html.xpath('//title/text()')
          upName = html.xpath('//span[@class="info-text"]/text()')
          print('房间名称：%s'%title[0])
          webPage.close()
          
          #获取弹幕服务器
          conn = http.client.HTTPConnection(self.host)
          conn.request("GET",'/api/player?id=cid:'+ str(self.roomId)) 
          response = conn.getresponse()
          res= response.read()
          #print(res)
          res = etree.HTML(res)
          server = res.xpath('//server/text()')
          self.server = server[0]
          login = res.xpath('//login/text()')
          print("账号状态：",end="")
          if login and login=="true":
               print("账号已登录！")
          else:
               print("账号未登录！")
          state = res.xpath('//state/text()')
          print("主播状态：",end="")
          if state[0] == 'PREPARING':
               print('主播【%s】尚未直播...'%upName[0])
          elif state[0] == 'LIVE':
               print('主播【%s】正在直播...'%upName[0])
          elif state[0] == 'ROUND':
               print('主播【%s】正在轮播...'%upName[0])
          else:
               print('直播状态未知')
               
          #self.createDb()
          self.sendData()
     
     def sendData(self):
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((self.server,self.port))
          #print(s.getpeername())
          print("连接弹幕服务器：%s:%d"%(s.getpeername()[0],s.getpeername()[1]))
          print()
          self.uid = int(100000000000000.0 + 200000000000000.0*random.random())
          body = '{"roomid":%d,"protover":2,"uid":%d}'%(self.roomId,self.uid)
          bodyCode = body.encode('utf-8')
          dataLen =len(bodyCode) + 16
          dataFront = struct.pack('!iHHII',dataLen,16,1,7,1)
          data = dataFront + bodyCode
          s.send(data)
          self.thread(s)
          self.recvData(s)
          
     def heartBeat(self,s):          
          while True:
               heartbeat = struct.pack('!iHHII',16,16,1,2,1)
               try:
                    s.send(heartbeat)
               except:
                    print("="*72)
                    print("网络连接失败，程序即将退出")
                    break
               time.sleep(30)
               
         
     def recvData(self,s):
          while True:
               
               try:
                    msgHeadData = s.recv(16)
                    #print("数据头 ：",end="")
                    #print(msgHead)
               except:
                    print("="*72)
                    self.nowtime()
                    print(' 您已经进入木有网络的二次元啦！请检查网络...')
                    time.sleep(30)
                    break
               
               if not len(msgHeadData):
                    print("="*72)
                    print('服务器断开连接')
                    break
               #接收数据过大
               try:
                    msgHead = struct.unpack('!iHHII',msgHeadData)
                    #print(msgHead)
               except:
                    print("-"*72)
                    print("数据头解析错误")
                    print(msgHeadData)
                    print("-"*72)
                    continue
               msgLen = msgHead[0]
               #print("数据总长度：%d"%msgLen)
               if msgLen <= 16:
                    continue
               #数据不完整
               
               msgData = s.recv(msgLen-16)
               #print("主体内容长度：%d"%len(msgData))
               if msgLen == 20:
                    msgData =struct.unpack('!i',msgData)
                    print("当前在线人数：%d"%msgData)
                    continue
               #循环网络堵塞，接受不完整的数据
               while True:
                    if msgLen - 16 > len(msgData):
                         print("数据不完整",end = "-->")
                         print("数据总长度：%d"%msgLen,end=" ")
                         print("主体内容长度：%d"%len(msgData))
                         RestmsgData = s.recv(msgLen-16-len(msgData))
                         msgData += RestmsgData
                         print(msgHead)
                         print(msgData)
                         print("现总长度%d"%(16+len(msgData)))
                    else:
                         break
               #print(msgData)
               try:
                     DemsgData=zlib.decompress(msgData)
               except zlib.error as reason:
                     reason = str(reason)
                     if "-3" in reason:
                         DemsgData = msgHeadData + msgData
                     else:
                        print("-"*72)
                        print("zlib.error",end=" :")
                        print(reason)
                        print(msgHeadData)
                        print(msgData)
                        
                        msgHeadData = s.recv(16)
                        print(msgHeadData)
                        print("-"*72)
                        
         
               location = 0
               while True:
                   msgHead = struct.unpack('!iHHII',DemsgData[location:location+16])
                   #print(msgHead)
                   data = DemsgData[location+16:location+msgHead[0]]
                   #print(data)
                   data= self.subEmoji(data)
                   try:
                        JsonMsgData=data.decode("utf-8")
                   except:
                         print("-"*72)
                         print(data)
                         print("-"*72)
                         
                   self. printMsg(JsonMsgData)
                   location = location + msgHead[0]
                   #print(location)
                   if location == len(DemsgData):
                       break
              

               
     def printMsg(self,msgData):
          #print(msgData)
          try:
               dic = json.loads(msgData)
          except:
               return
          #print(dic)
          cmd = dic['cmd']
               
          if cmd == 'DANMU_MSG':                         
               sendor = dic['info'][2][1]
               content = dic['info'][1]
               isadmin = dic['info'][2][2]
               isVIP = dic['info'][2][3]
               sendid = dic['info'][2][0]
               rank = dic['info'][4][0]
               if dic['info'][3]:
                    model = dic['info'][3][1]
                    upid = dic['info'][3][4]
                    upname = dic['info'][3][2]
                    uproom = dic['info'][3][3]
               else:
                    model=upid=upname=uproom=''
                    
               self.nowtime()
               if isadmin:                         
                    print('【房管】【'+sendor+"】：" + content)            
               else:
                    print('【'+sendor+"】：" + content)
               self.insertDanmu(sendor,content,sendid,rank,upid,model,upname,uproom)

          elif cmd == 'WELCOME':
               isvip = dic['data']['uname']
               isadmin = dic['data']['isadmin']
               self.nowtime()
               if isadmin:
                    print(" 欢迎【房管】【%s】老爷进入直播间"%isvip)
               else:
                    print(" 欢迎【%s】老爷进入直播间"%isvip)
               
          elif cmd =='WELCOME_GUARD':
               guard = dic['data']['username']
               
               print(" 欢迎【%s】守护进入直播间"%guard)

          elif cmd == 'LIVE':
               self.nowtime()
               print('主播开始直播啦！')
               
          elif cmd == 'PREPARING':
               self.nowtime()
               print('主播已经下播啦！')
          
          elif  cmd == 'SEND_GIFT':
               giftName = dic['data']['giftName']
               giftNum = dic['data']['num']
               sendor = dic['data']['uname']
               uid = dic['data']['uid']
               giftId = dic['data']['giftId']
               action= dic['data']['action']
               self.nowtime()     
               print('【'+ sendor +'】' + "赠送" + str(giftNum) + '个' + giftName)
               self.insertGift(sendor,action,giftNum,giftName,uid,giftId)
                         
          elif cmd =='SYS_GIFT':                        
               msg = dic['msg']
               msg = msg.replace(':?','')
               print("-"*72)
               self.nowtime()
               print(" 礼物公告："+ msg)
               print("-"*72)
                     
          elif cmd == 'SYS_MSG':
               msg = dic['msg']
               msg = msg.replace(':?','')
               #系统公告、小电视
               print("-"*72)
               self.nowtime()
               print(" "+msg)
               print("-"*72)
          else:
               print("其他消息类型：",end="")
               print(dic)

     def thread(self,s):
          threads = []
          t1 = threading.Thread(target=self.heartBeat,args=(s,))
          threads.append(t1)
          
          if __name__ == '__main__':
               t1.setDaemon(True)#设置t1守护线程 随主程序一同退出
               t1.start()

     def nowtime(self):
          nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
          print('[%s]'%nowTime,end='')

     def subEmoji(self,data):
          emoji = re.compile(r'[\U0001F000-\U0001FFFF]|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\udeff]')
          data = emoji.sub('\u274e',data.decode())
          return data.encode()
          
     def createDb(self):
          #root为数据库用户，00000为数据库密码，test为数据库名
          db = pymysql.connect('localhost','root','00000','test',use_unicode=True, charset="utf8")
          cursor = db.cursor()
          cursor.execute('drop table if exists Bili_danmu')
          sql='''create table Bili_danmu (id int(8) not null AUTO_INCREMENT,
                 时间 datetime,
                 发送者 char(30) not null,
                 内容 char(30),
                 sendid int(9) not null,
                 等级 int(2) not null,
                 upid char(9),
                 勋章 char(4),
                 主播 char(30),
                 房间号 char(8),
                 primary key (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
          cursor.execute(sql)
          cursor.execute('drop table if exists Bili_gift')
          sql='''create table Bili_gift (id int(8) not null AUTO_INCREMENT,
                 时间 datetime,
                 赠送者 char(30) not null,
                 动作 char(2),
                 数量 int(5) not null,
                 礼物名字 char(5) not null,
                 sendid int(9) not null,
                 giftid int(2) not null,
                  primary key (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
          cursor.execute(sql)
          db.close()
                          
     def insertDanmu(self,sendor,content,sendid,rank,upid,model,upname,uproom):
         db = pymysql.connect('localhost','root','00000','test',use_unicode=True, charset="utf8")
         cursor = db.cursor()
         #print(sendor,content,sendid,rank,upid,model,upname,uproom)
         sql="insert into Bili_danmu (时间,发送者,内容,sendid,等级,upid,勋章,主播,房间号)\
         values(now(),'%s','%s','%d','%d','%s','%s','%s','%s')"%\
         (sendor,content,int(sendid),int(rank),str(upid),model,upname,uproom)
         try:
              cursor.execute(sql)
              db.commit()
         except:
              print('插入失败')
              db.rollback()
         db.close()
     def insertGift(self,sendor,action,giftNum,giftName,uid,giftId):
         db = pymysql.connect('localhost','root','00000','test',use_unicode=True, charset="utf8")
         cursor = db.cursor()
         #print(sendor,action,giftNum,giftName,uid,giftId)
         sql="insert into Bili_gift (时间,赠送者,动作,数量,礼物名字,sendid,giftid)\
         values(now(),'%s','%s','%d','%s','%d','%d')"%\
         (sendor,action,int(giftNum),giftName,int(uid),int(giftId))
         
         try:
              cursor.execute(sql)
              db.commit()
         except:
              print('插入失败')
              db.rollback()
         db.close()
          
danmu = client()
danmu.getServer()


import re
import sys
import time
import json
import socket
import struct     
import random
import threading
import http.client
import urllib.request
from lxml import etree



class client():
     def __init__(self):
          self.liveUrl='http://live.bilibili.com'
          self.roomId = 0
          self.host = 'live.bilibili.com'
          self.port = 788
          self.protover = 0          
          # 防止emoji表情编码出错
          self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
          
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
          res = etree.HTML(res)
          server = res.xpath('//server/text()')
          self.server = server[0]
          state = res.xpath('//state/text()')
          if state[0] == 'PREPARING':
               print('主播【%s】尚未直播...'%upName[0])
          elif state[0] == 'LIVE':
               print('主播【%s】正在直播...'%upName[0])
          elif state[0] == 'ROUND':
               print('主播【%s】正在轮播...'%upName[0])
          else:
               print('直播状态未知')
               
          
          self.sendData()
     
     def sendData(self):
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((self.server,self.port))
          print("连接弹幕服务器：%s:%d"%(s.getpeername()[0],s.getpeername()[1]))
          print()
          self.uid = int(100000000000000.0 + 200000000000000.0*random.random())
          body = '{"roomid":%d,"uid":%d}'%(self.roomId,self.uid)
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
                    print("===============================================================================")
                    print("网络连接失败，程序即将退出")
                    break
               time.sleep(30)
               
         
     def recvData(self,s):
          while True:
               try:
                    msgHead = s.recv(16)
               except:
                    print("===============================================================================")
                    self.nowtime()
                    print(' 您已经进入木有网络的二次元啦！请检查网络...')
                    time.sleep(30)
                    break
               if not len(msgHead):
                    print("===============================================================================")
                    print('服务器断开连接')
                    break
               #接收数据过大
               try:
                    msgHead = struct.unpack('!iHHII',msgHead)
               except:
                    continue
               msgLen = msgHead[0]
               if msgLen <= 16:
                    continue
               #数据不完整
               try:
                    msgData = s.recv(msgLen-16)
               except:
                    continue
               if msgLen == 20:
                    msgData =struct.unpack('!i',msgData)
                    print("当前在线人数：%d"%msgData)
                    continue
               else:
                    msgData = msgData.decode('utf-8',errors='ignore')

               self. printMsg(msgData)

               
     def printMsg(self,msgData):
          try:
               dic = json.loads(msgData)
          except:
               return
          cmd = dic['cmd']
               
          if cmd == 'DANMU_MSG':                         
               sendor = dic['info'][2][1]
               content = dic['info'][1]
               isadmin = dic['info'][2][2]
               isVIP = dic['info'][2][3]
               self.nowtime()
               if isadmin:                         
                    print('【房管】【'+sendor+"】：" + content.translate(self.non_bmp_map))            
               else:
                    print('【'+sendor+"】：" + content.translate(self.non_bmp_map))
                   

          if cmd == 'WELCOME':
               isvip = dic['data']['uname']
               isadmin = dic['data']['isadmin']
               self.nowtime()
               if isadmin:
                    print(" 欢迎【房管】【%s】老爷进入直播间"%isvip)
               else:
                    print(" 欢迎【%s】老爷进入直播间"%isvip)
               
          if cmd =='WELCOME_GUARD':
               guard = dic['data']['username']
               
               print(" 欢迎【%s】守护进入直播间"%guard)

          if cmd == 'LIVE':
               self.nowtime()
               print('主播开始直播啦！')
               
          if cmd == 'PREPARING':
               self.nowtime()
               print('主播已经下播啦！')
          
          if  cmd == 'SEND_GIFT':
               giftName = dic['data']['giftName']
               giftNum = dic['data']['num']
               sendor = dic['data']['uname']
               self.nowtime()     
               print('【'+ sendor +'】' + "赠送" + str(giftNum) + '个' + giftName)
               
                         
          if cmd =='SYS_GIFT':                        
               msg = dic['msg']
               msg = msg.replace(':?','')
               print("-------------------------------------------------------------------------------")
               self.nowtime()
               print(" 礼物公告："+ msg)
               print("-------------------------------------------------------------------------------")
                     
          if cmd == 'SYS_MSG':
               msg = dic['msg']
               msg = msg.replace(':?','')
               #系统公告、小电视
               print("-------------------------------------------------------------------------------")
               self.nowtime()
               print(" "+msg)
               print("-------------------------------------------------------------------------------")
                
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
          

danmu = client()
danmu.getServer()




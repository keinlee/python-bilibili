import re
import urllib.request
from lxml import etree
import http.client

def enterRoom():
    while True:
    #测试房间号
       roomId = input('请输入房间号：')
       while not roomId.isdigit():
            print("格式错误，请重新输入！")
            roomId = input('请输入房间号：')
            
       roomUrl = 'http://live.bilibili.com/'+ str(roomId)
       #测试网址
       webheaders = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
       req = urllib.request.Request(url=roomUrl, headers=webheaders)
       try:
            webPage=urllib.request.urlopen(req)
            break
       except urllib.error.HTTPError as reason:
            print('网址出错啦！'+ str(reason))
       except urllib.error.URLError as reason:
            print('网址出错啦！'+ str(reason))
    return webPage

def getTitle(webPage):            
          #获取直播间号
          html = webPage.read().decode('utf-8')
          m = re.findall(r'ROOMID\s=\s(\d+)', html)
          ROOMID = m[0]
          roomId = int(ROOMID)
          print('正在进入【%d】房间...'%roomId)
          #获取直播间标题
          html = etree.HTML(html)
          title = html.xpath('//title/text()')
          upName = html.xpath('//span[@class="info-text"]/text()')
          print('房间名称：%s'%title[0])
          webPage.close()
          return roomId,upName

def getServer(roomId,upName):          
         #获取弹幕服务器
          conn = http.client.HTTPConnection('live.bilibili.com')
          conn.request("GET",'/api/player?id=cid:'+ str(roomId) )
          response = conn.getresponse()
          res= response.read()
          res = etree.HTML(res)
          server = res.xpath('//server/text()')
          server = server[0]
          state = res.xpath('//state/text()')
          if state[0] == 'PREPARING':
               print('主播【%s】尚未直播...'%upName[0])
          elif state[0] == 'LIVE':
               print('主播【%s】正在直播...'%upName[0])
          elif state[0] == 'ROUND':
               print('主播【%s】正在轮播...'%upName[0])
          else:
               print('直播状态未知')
               
          return server

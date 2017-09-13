import urllib.parse

def get_cookies():
    EnterCookies= ''''''
    #EnterCookies填写登陆后的请求头
    EnterCookies = EnterCookies.replace('\n','')
    sendel='attentionData=;' #填写请求头中的attentionData

    SendCookies = EnterCookies.replace(sendel,'')
    #print(SendCookies)
    Blackdel = 'tencentSig=;'#填写请求头中的tencentSig
    
    BlackCookies = EnterCookies.replace(Blackdel,'')
    #print(BlockCookies)
    return EnterCookies,SendCookies,BlackCookies


def room_header(cookies):
    headers = {'Accept':'text/html',
    'Accept-Encoding':'deflate',
    'Accept-Language':'zh-CN',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'cookie':cookies,
    'Host':'live.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.203 Safari/537.36'}
    return headers


def black_user_data(uname,hour,roomId):
    BlackData ={
    'roomid':str(roomId),
    'content':uname,
    'type':'1',
    'hour':hour}
    data = urllib.parse.urlencode(BlackData).encode('utf-8')
    return data

def black_header(cookies,roomUrl):
    headers = {'Accept':'text/html',
    'Accept-Encoding':'deflate',
    'Accept-Language':'zh-CN',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie':cookies,
    'Host':'api.live.bilibili.com',
    'Origin':'http://live.bilibili.com',
    'Referer':roomUrl,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.203 Safari/537.36'}
    return headers

def send_header(cookies):
    headers = {'Accept':'text/html',
    'Accept-Encoding':'deflate',
    'Connection':'keep-alive',
    'cookie':cookies,
    'Host':'live.bilibili.com',
    'Origin':'http://static.hdslb.com',
    'Referer':'http://static.hdslb.com/live-static/swf/LivePlayerEx_1.swf?_=1-1-c5a315d',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    return headers

def send_data(msg,roomId):
    #这里的数据根据自己的账号情况写
    SendData ={
    'color':'8322816',
    'fontsize':'25',
    'mode':'1',
    'msg':msg,
    'rnd':'1498012515',
    'roomid':roomId}
    data = urllib.parse.urlencode(SendData).encode('utf-8')
    return data

    
    
    
    
    

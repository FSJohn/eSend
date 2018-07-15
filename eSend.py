#-*- coding: UTF-8 -*-
#Author:FSJohn
#Time:2017年12月26日 18:11:10
#Version:1.21
import requests
from bs4 import BeautifulSoup
import feedparser
import time

user = "" #登录用户名
passwd = "" #登录密码

def main():
    status = 0
    while status==0:
        cronTab = time.strftime("%H%M")
        cronTab=int(cronTab)
        if cronTab==600:
            login()
            send(content())
            time.sleep(60)
            status=1
        else:
            time.sleep(10)
        time.sleep(10)
        status=0


def login():
    url=("http://120.76.190.14:8030/JXT3/jxt.api.APIForAPP3!patriarchLogin.hdz"+"?pwd="+passwd+\
         "&login_name="+user+"&device_type=android&app_type=patriarch&student_id=&app_version_no=8\
         &user_id=&type=user_code&device_version_no=4%2e4%2e4&hash=0881AA36240D7D3584576718C2B810AA%20")
    r = requests.post(url)
    print(r.text)
    cookies=({c.name:c.value for c in r.cookies})
    response_dict=r.json()
    print(getTimes(),response_dict['msg'])
    return cookies


def content():
    text1 = str(hitokoto())
    if getInfo()==200:
        text2 = "服务器一切正常."
    else:
        text2 = "服务器Http返回值为"+ str(getInfo()) +"."
    content = (text2 + "\n" + text1)
    send = (content + "FSJohn_CN Meidochan\t\nTimes:" + getTimes())
    #send = ("来自Meidochan的纸条：\n" +content + "\t\nFrom FSJohn_CN Meidochan\t\nTimes:" + getTimes())
    return send

def send(send):
    print(send)
    send = {'type': '普通', 'msg_content': send}
    r = requests.post("http://120.76.190.14:8030/JXT3/mobile.my.PatriarchMessageAction!add.hdz",data=send,cookies=login())
    #如果成功 r.text="<result><code><![CDATA[1]]></code><text><![CDATA[留言成功!]]></text></result>"
    print(r.text)
    soup=BeautifulSoup(r.content,'html.parser')
    #print(getTimes(),soup.text[1:5])
    if soup.text[1:5]=="留言成功":
        print(getTimes(),"Success,Length is",len(str(send)),".")
    else:
        print(getTimes(),"Errors,Length is",len(str(send)),".")
        print(getTimes(),send)
        send(content())

def list():
    headers = {'Connection': 'keep-alive',
               'Cookie': 'JSESSIONID=151156352512472372'}
    send = {'pageSize':'1','pageIndex':'1','current_row':'0'}
    r = requests.post("http://jxt3.jxt580.com:8030/JXT3/mobile.my.PatriarchMessageAction!list.hdz",headers=headers,data=send)
    print(r.text)
    soup = BeautifulSoup(r.content, 'html.parser')

#获取服务器状态信息
def getInfo():
    def Listen(add):
        try:
            r = requests.get(add)
            return r.status_code
        except:
            pass
    statusCode=Listen(listenAdd)
    return statusCode

#lwl一言api
def hitokoto():
    url='https://api.lwl12.com/hitokoto/main/get'
    r=requests.get(url)
    return r.text
def getTimes():
    global times
    times = ("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]")
    return times

#由于传输文本有限，rss文本传输功能停止开发
def doc():
    d = feedparser.parse('https://planet.nyaa.cat/rss.xml')
    print(d.feed.title)
    print(d.entries[1].content)

if __name__ == '__main__':
    main()

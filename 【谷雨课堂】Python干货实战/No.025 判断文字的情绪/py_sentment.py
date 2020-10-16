# coding:utf-8
# 【谷雨课堂】干货实战 No.025 判断文字的情绪
# 作者：谷雨


from aip import AipNlp
import json
import win32com.client

#语音合成输出
def speak(s):
    print("-->"+s)
    win32com.client.Dispatch("SAPI.SpVoice").Speak(s)


APP_ID = '22674385'
API_KEY = 'iqgi7YfA7gFiAr5eQvOr9wsa'
SECRET_KEY = '0gxX7KsDSNyG2PPyYxvCeOOTGAzpOcD4'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#text="《谷雨课堂》是一个好课堂"
#text = "真烦人，今天又下雨了"
text = "今天天气真不错"

ret=client.sentimentClassify(text)
sentiment=ret['items'][0]['sentiment']


if sentiment==0:
    s="带有负面情绪"
if sentiment==1:
    s="中性"
if sentiment==2:
    s="带有正面情绪"

speak(text+"，，"+s)

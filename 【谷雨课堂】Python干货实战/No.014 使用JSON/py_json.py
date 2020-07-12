# coding:utf-8
# 【谷雨课堂】干货实战 No.013 访问HTTP网络
# 作者：谷雨

import requests


def HttpGet(url):
    ret=requests.get(url)
    ret.encoding='utf-8'
    return ret.text

def HttpPost(url,form_data):
    ret=requests.post(url,form_data)
    ret.encoding='utf-8'
    return ret.text

s=HttpGet("https://www.baidu.com/s?wd=谷雨课堂")
print(s)

post_data={
    'username':'admin',
    'password':'123456'
}

s=HttpPost("http://t.hn1517.com/",post_data)
print(s)

# coding:utf-8
# 【谷雨课堂】干货实战 No.027 五行代码做一个网站
# 作者：谷雨

from flask import Flask
import time
app = Flask(__name__)

@app.route("/")
def hello():
    return "Now is: "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

@app.route("/abc")
def abc():
    return "hello abc"



app.run()

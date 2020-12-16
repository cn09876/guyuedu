# coding:utf-8
# 【谷雨课堂】干货实战 No.031 网站开发之-使用SQLite数据库
# 作者：谷雨

from flask import Flask,url_for,redirect,render_template,request
import time
import os
from _inc import *

app = Flask(__name__)



@app.route("/")
def index():
    #删除表
    dbs().q("drop table users")
    #建立表
    dbs().q("create table users (uid,pwd) ")

    #批量添加记录
    for i in range(1,11):
        dbs().q("insert into users values ('user%d','pass%d') " % (i,i))

    #查询记录
    rs=dbs().query("select * from users")    
    s=""
    for r in rs:
        s=s+"uid="+r['uid']+",pwd="+r['pwd']+"<br>"
    return s



app.run()

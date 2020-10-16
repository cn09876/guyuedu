# coding:utf-8
# 【谷雨课堂】干货实战 No.028 网站开发之获取输入数据
# 作者：谷雨

from flask import Flask,url_for,redirect,render_template,request

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def hello():
    str_form="<form method=post action=''><input type=text name=username value='guyu python'><input type=submit value='Send'></form>"
    get_name=request.args.get('username')
    if get_name==None:
        get_name=''

    post_name=request.form.get('username')
    if post_name==None:
        post_name=''
        
    return str_form+"get_name is："+get_name+"<br>post_name is: "+post_name

if __name__ == "__main__":
    app.run()

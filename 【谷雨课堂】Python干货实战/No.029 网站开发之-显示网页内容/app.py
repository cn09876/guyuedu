# coding:utf-8
# 【谷雨课堂】干货实战 No.029 网站开发之-显示网页内容
# 作者：谷雨

from flask import Flask,url_for,redirect,render_template,request

app = Flask(__name__)
app.debug = True

@app.route("/")
def out_1():        
    return "hello"
 
@app.route("/json")
def out_2():        
    t = {
            'count': 100,
            'msg': 'ok',
            'rows': [
                {'id':1,'username':'user1'},
                {'id':2,'username':'user2'},
                {'id':3,'username':'user3'},
            ]
        }
    return t

@app.route("/tpl")
def out_3():        
    t = {
            'count': 100,
            'msg': 'ok',
            'rows': [
                {'id':1,'username':'user1'},
                {'id':2,'username':'user2'},
                {'id':3,'username':'user3'},
            ]
        }
    return render_template('hello.html', dt=t)

if __name__ == "__main__":
    app.debug = True
    app.run()

# coding:utf-8
# 【谷雨课堂】干货实战 No.036 网站开发之-上传图片并生成图片缩略图
# 作者：谷雨


from flask import Flask,url_for,redirect,render_template,request,Response
import time
import os
import io
import mimetypes
import xhtml2pdf.pisa as pisa
from werkzeug.datastructures import Headers
from urllib.parse import quote
import xlrd,xlwt
from PIL import Image

app = Flask(__name__)

#基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#static路径
STATIC_DIR = os.path.join(BASE_DIR,'static')

#上传路径
UPLOAD_DIR = os.path.join(STATIC_DIR,'upload')

# 上传文件处理,自动找上传的参数名
def upfile(field='',dir=''):
 
    if len(request.files)<1:
        return ""

    if field=='':
        for k in request.files:
            field=k
            break

    f = request.files[field]
    if f==None:
        print("没有上传的字段"+field)
        return ""
    fname = f.filename

    if fname=='':
        return ''

    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    str_ymd = time.strftime("%Y-%m-%d", timeStruct)
    if dir=='':dir=str_ymd
    if not os.path.exists(UPLOAD_DIR+"/"+dir):
        os.makedirs(UPLOAD_DIR+"/"+dir)
    print(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    f.save(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    return dir+'/'+new_filename


def process_image(filename,filename_save,mwidth=200, mheight=400):
    image = Image.open(filename)
    w,h = image.size
    if w<=mwidth and h<=mheight:
        print(filename,'is OK.')
        return 
    if (1.0*w/mwidth) > (1.0*h/mheight):
        scale = 1.0*w/mwidth
        new_im = image.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)
 
    else:
        scale = 1.0*h/mheight
        new_im = image.resize((int(w/scale),int(h/scale)), Image.ANTIALIAS)     
    new_im.save(filename_save)
    new_im.close()


@app.route("/api/upload",methods=['POST'])
def uploader():
    upload_file=upfile()
    if upload_file=='':
        return "您没有上传文件 <a href='/'>返回</a>"
    
    process_image(UPLOAD_DIR+"/"+upload_file,UPLOAD_DIR+"/"+upload_file.replace(".","_small."))

    s="您已经上传文件<hr>生成的缩略图为:<br><img src='/static/upload/"+upload_file.replace(".","_small.")+"'>"
    s+="<hr><a href='/?'>返回</a>"
    return s



@app.route("/")
def index():
    return render_template("upload.html")

app.run()



 
# coding:utf-8
# 【谷雨课堂】干货实战 No.037 网站开发之-上传图片并添加水印
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
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import matplotlib.pyplot as plt

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


# 图片添加水印
def img_water_mark(img_file, wm_file,save_path):
    try:
        img = Image.open(img_file) 
        watermark = Image.open(wm_file)  
        img_size = img.size
        wm_size = watermark.size
        
        # 默认设定水印位置为右下角
        wm_position = (img_size[0]-wm_size[0]-20,img_size[1]-wm_size[1]-20) 
        layer = Image.new('RGBA', img.size)  # 新建一个图层
        layer.paste(watermark, wm_position)  # 将水印图片添加到图层上
        mark_img = Image.composite(layer, img, layer)
        mark_img.save(save_path)
    except Exception as e:
        print(traceback.print_exc())


@app.route("/api/upload",methods=['POST'])
def uploader():
    upload_file=upfile()
    if upload_file=='':
        return "您没有上传文件 <a href='/'>返回</a>"
    
    img_water_mark(UPLOAD_DIR+"/"+upload_file,"wm.jpg",UPLOAD_DIR+"/"+upload_file.replace(".","_watermark."))

    s="您已经上传文件<hr>增加水印后的图片为:<br><img src='/static/upload/"+upload_file.replace(".","_watermark.")+"'>"
    s+="<hr><a href='/?'>返回</a>"
    return s



@app.route("/")
def index():
    return render_template("upload.html")

app.run()



 
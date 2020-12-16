# coding:utf-8
# 【谷雨课堂】干货实战 No.032 网站开发之-生成图片验证码
# 作者：谷雨

from flask import Flask,url_for,redirect,render_template,request,Response
import time
import os
import io
import mimetypes
import xhtml2pdf.pisa as pisa
from werkzeug.datastructures import Headers
from urllib.parse import quote
from random import choice, randint, randrange
import string
from PIL import Image, ImageDraw, ImageFont

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

# 验证码图片文字的字符集
characters = string.ascii_letters + string.digits

def selectedCharacters(length):

    result = ''.join(choice(characters) for _ in range(length))
    return result


def getColor():

    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


def gencode_img(size=(200, 100), characterNumber=6, bgcolor=(255, 255, 255)):
    # 创建空白图像和绘图对象
    imageTemp = Image.new('RGB', size, bgcolor)
    draw01 = ImageDraw.Draw(imageTemp)     

    # 生成并计算随机字符串的宽度和高度
    text = selectedCharacters(characterNumber)
    font = ImageFont.truetype('Dengl.ttf', 48)
    width, height = draw01.textsize(text, font)
    if width + 2 * characterNumber > size[0] or height > size[1]:
        print('尺寸不合法')
        return

    # 绘制随机字符串中的字符
    startX = 0
    widthEachCharater = width // characterNumber
    for i in range(characterNumber):
        startX += widthEachCharater + 1
        position = (startX, (size[1] - height) // 2 + randint(-10, 10))
        draw01.text(xy=position, text=text[i], font=font, fill=getColor())

    # 对像素位置进行微调，实现扭曲的效果
    imageFinal = Image.new('RGB', size, bgcolor)
    pixelsFinal = imageFinal.load()
    pixelsTemp = imageTemp.load()
    for y in range(size[1]):
        offset = randint(-1, 0)
        for x in range(size[0]):
            newx = x + offset
            if newx >= size[0]:
                newx = size[0] - 1
            elif newx < 0:
                newx = 0
            pixelsFinal[newx, y] = pixelsTemp[x, y]

    # 绘制随机颜色随机位置的干扰像素
    draw02 = ImageDraw.Draw(imageFinal)
    for i in range(int(size[0] * size[1] * 0.07)):
        draw02.point((randrange(0, size[0]), randrange(0, size[1])), fill=getColor())

    # 绘制8条随机干扰直线
    for i in range(8):
        start = (0, randrange(size[1]))
        end = (size[0], randrange(size[1]))
        draw02.line(start + end, fill = getColor(), width=1)

    # 绘制8条随机弧线
    for i in range(8):
        start = (-50, -50)
        end = (size[0] + 10, randint(0, size[1] + 10))
        draw02.arc(start + end, 0, 360, fill=getColor())

    # 保存并显示图片
    imageFinal.save(STATIC_DIR+"/result.jpg")


@app.route("/")
def index():
    gencode_img()
    return "验证码<hr><img src='/static/result.jpg?"+str(time.time())+"'>"

app.run()

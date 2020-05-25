# coding:utf-8
# 【谷雨课堂】干货实战 No.006 图片缩放、旋转和裁剪
# 作者：谷雨
#
from PIL import Image
import base64
from io import BytesIO

img = Image.open("cat.jpg")

#图片的缩放
resize_img=img.resize((50,50))
resize_img.save("cat_缩小图.jpg")

#图片的旋转
img1=img.rotate(45)
img1.save("cat_旋转45度.jpg")

#图片的裁剪
box = (0, 0, 200, 200)          
rect_img = img.crop(box)                  
rect_img.save("cat_裁剪图.jpg")


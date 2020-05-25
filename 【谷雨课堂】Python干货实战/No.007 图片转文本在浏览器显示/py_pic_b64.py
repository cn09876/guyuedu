# coding:utf-8
# 【谷雨课堂】干货实战 No.007 图片转文本在浏览器显示
# 作者：谷雨
#
from PIL import Image
import base64
from io import BytesIO

img = Image.open("cat.jpg")
img=img.resize((50,50))
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_str = str(base64.b64encode(buffered.getvalue()))
img_str=img_str.replace("b'","")
img_str=img_str.replace("'","")

print("data:image/jpg;base64, "+ img_str)


# coding:utf-8
#【谷雨课堂】Python干货实战 No.004，用Python进行屏幕截图

from PIL import ImageGrab

pic = ImageGrab.grab((0,0,300,300))
pic.save("1.jpg")

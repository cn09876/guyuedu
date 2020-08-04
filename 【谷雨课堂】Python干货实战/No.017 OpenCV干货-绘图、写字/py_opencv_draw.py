# coding:utf-8
# 【谷雨课堂】干货实战 No.017 OpenCV干货-绘图、写字
# 作者：谷雨

import numpy as np
import cv2
 
#创建一幅空白图像,512*512的彩色图
img=np.zeros((512,512,3), np.uint8)

#画一个5像素粗细的，红色的，线 BGR
cv2.line(img,(0,0),(511,511),(0,0,255),5)

#画一个，绿色的，矩形
cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
 
#画一个圆
cv2.circle(img,(200,100), 100, (0,0,255), -1)
 
#椭圆
cv2.ellipse(img,(256,256),(100,50),30,0,360,255,3)
 
#画一条路径（由多个点连接而成）
pts=np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts=pts.reshape((-1,1,2))
cv2.polylines(img,[pts],True,(0,0,255),3)#如果去掉中括号，只是画四个点
 
#写一些文字 
font=cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'GuyuCV',(10,500), font, 4,(255,255,255),2)
 
cv2.imshow('GuyuCV',img)
cv2.waitKey(0)

# -*- coding: utf-8 -*-
# 【谷雨课堂】干货实战 No.018 OpenCV干货-猫脸识别!
# 作者：谷雨

import cv2

#猫脸检测器
classPath = './haarcascade_frontalcatface.xml'
face_cascade=cv2.CascadeClassifier(classPath)

#读取图片并转为黑白图
img = cv2.imread('./cat3.jpg')  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#识别出猫
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor= 1.02,
    minNeighbors=5,
    minSize=(120, 120),
    flags=cv2.CASCADE_SCALE_IMAGE
) 

#框出猫脸框
for (x, y, w, h) in faces:
   cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
   cv2.putText(img,'MiaoMiao',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

cv2.imshow('Cat', img)
c = cv2.waitKey(0)
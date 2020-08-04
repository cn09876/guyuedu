# coding:utf-8
# 【谷雨课堂】干货实战 No.016 OpenCV干货-调用USB摄像头
# 作者：谷雨

#引用OpenCV库
import cv2

#打开摄像头
cap = cv2.VideoCapture(1)

#永远执行一段语句
while True:
  #从摄像头获取一幅图像
  ret,frame = cap.read()
  #将图像显示出来
  cv2.imshow("cap", frame)
  #按键判断，如果按下q就退出程序
  if cv2.waitKey(100) & 0xff == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
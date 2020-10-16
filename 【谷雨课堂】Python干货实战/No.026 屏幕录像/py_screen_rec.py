# coding:utf-8
# 【谷雨课堂】干货实战 No.026 屏幕录像
# 作者：谷雨

from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard
import threading

#停止标志位
flag=False  

#录像进程
def video_record():
    #当前的时间
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    # 获得当前屏幕
    p = ImageGrab.grab()  
    # 获得当前屏幕的大小,改动此处可以只录屏幕一部分区域
    a, b = p.size  
    # 编码格式
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  
    video = cv2.VideoWriter('录像_%s.mp4'%name, fourcc, 20, (a, b))
    while True:
        im = ImageGrab.grab()
        #将RGB格式转为opencv的BGR格式，否则图像颜色不对
        imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        video.write(imm)
        if flag:
            print("录制结束！")
            break
    video.release()

#全局监听键盘事件，按ESC退出录像
def on_press(key):
    global flag
    if key == keyboard.Key.esc:
        flag=True
        return False  

#主程序
#开启一个线程，进行录像 
th=threading.Thread(target=video_record)
th.start()
print("开始录像")

#全局进行键盘事件监听，回调函数为on_press
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
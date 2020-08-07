# _*_ coding:utf-8 _*_
# 【谷雨课堂】干货实战 No.019 OpenCV干货-目标跟踪
# 作者：谷雨
# 需要安装imutils和opencv-contrib-python
 
 
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2

tracker_name="csrt"
 

#初始化跟踪方法
#OpenCV中一共有以下这么几种跟踪算法，效果有些差异，同学们可以都试一下
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# 定义跟踪方法
tracker = OPENCV_OBJECT_TRACKERS['csrt']()

#要跟踪的对象
initBB = None

print("打开摄像头...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

while True:
    # 从摄像头获取一幅图像
    frame = vs.read()

    if frame is None:
        break

    #图像左右翻转一下
    frame=cv2.flip(frame,1)

    #把图像缩小一下，为了提高运行速度    
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
    
    #如果有需要跟踪的对象，就开始在这个图像里查找跟踪
    if initBB is not None:
        #返回跟踪结果
        (success, box) = tracker.update(frame)
        #如果找到跟踪的目标就画出框
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)


    #把图片显示出来
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        #按键盘的S键，开始用鼠标框选要跟踪的目标，按回车或空格结束 
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,showCrosshair=True)
        #初始化跟踪目标
        tracker.init(frame, initBB)

    #按键盘Q退出
    if key == ord("q"):
        break


#关闭程序后释放资源
vs.stop()
cv2.destroyAllWindows()
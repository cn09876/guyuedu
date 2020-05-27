import sys
import cv2
from PIL import Image

#给人脸画个框
def drawFace(frame,faceRects):
    if len(faceRects) > 0: #找到人脸了                                   
        for faceRect in faceRects:  
            #单独框出每一张人脸
            x, y, w, h = faceRect        
            cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 2)

#视频来源，来自USB摄像头
cap = cv2.VideoCapture(0)                
#人脸识别分类器
model = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

while cv2.waitKey(10)!=ord('q'):
    #第1行：从摄像头读取一副图像
    ok,frame = cap.read() 
    #第2行：将当前帧转换成灰度图像
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
    #第3行：人脸检测
    faceRects = model.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
    #第4行：给人脸画个框
    drawFace(frame,faceRects)                    
    #第5行：显示图像    
    cv2.imshow("Face", frame)    







#释放摄像头并销毁所有窗口
cap.release()
cv2.destroyAllWindows() 
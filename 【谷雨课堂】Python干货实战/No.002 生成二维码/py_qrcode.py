# coding:utf-8
# 【谷雨课堂】干货实战 No.002 生成二维码
# 作者：谷雨

#导入二维码函数库
import qrcode

#要生成的文字，可以是中文或者是网址
txt="大蟒蛇公司"

#生成二维码，此时是一张图片
img=qrcode.make(txt)

#把图片保存在硬盘中
img.save('qrcode.jpg')


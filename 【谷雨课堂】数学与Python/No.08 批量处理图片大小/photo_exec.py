# -*- coding: UTF-8 -*-

"""
@author: 谷雨老师
@function：批量修改某目录下的所有图片大小
"""

from PIL import Image
from PIL import ImageFile
import os.path
import sys
import glob

#
ImageFile.LOAD_TRUNCATED_IMAGES = True

savePath = "./处理后的图片/"


def resize_image(img_path,new_width):
    try:
        # 分离路径和后缀
        mPath, ext = os.path.splitext(img_path)
        # 是否是图片格式
        if ext=='.jpg':
            # 打开图片
            img = Image.open(img_path)
            # 获取图片的原始大小
            (width, height) = img.size
            # 根据新的宽度获得缩放新的高度
            new_height = int(height * new_width / width)
            # 开始改变大小，大于600才修改
            if width > new_width:
                out = img.resize((new_width, new_height), Image.ANTIALIAS)
            else:
                out = img.resize((width, height),Image.ANTIALIAS)
                

            # 分割获取图片名称
            new_file_name = os.path.split(img_path)[1]
            new_file_path = '%s%s' % (savePath,new_file_name)
            # 保存图片
            out.save(new_file_path, quality=100)
            print(new_file_path)
        else:
            print("非图片格式")
    except Exception as e:
        print("Error: "+img_path+"\t"+ str(e))



# 批量修改，使用glob模块
for imgPath in glob.glob("./要处理的图片/*.jpg"):
    # 循环去改变图片大小
    resize_image(imgPath,200)
    

print("批量处理完成")


    
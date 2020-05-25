# coding:utf-8
# 【谷雨课堂】干货实战 No.008 图片生成字符画
# 作者：谷雨

from PIL import Image

chars = list("A-% ,+1n&M-B/\?<8&WM#$_+~*|(){}[]>i!lI;:,\"^`'. ")
num = 4
chars = chars[:num]
width,height =40,20

#分节因子
factor = int(256 / len(chars))

# 依据灰度值阶梯返回不同的字符
def get_char(pix):
    for i in range(0,len(chars)):
        if pix < factor * (i+1):
            return chars[i]


img = Image.open('kn.jpg')

if img.mode=='P' or img.mode =='RGBA':
     im=Image.new('RGB',img.size,'white')
     im.paste(img.convert('RGBA'),img.convert('RGBA'))
     img= im

# 转化为灰度图
img = img.convert("L")
w,h = 0,0

w,h = img.size
img = img.resize((w,int(h/2)),Image.NEAREST)
h= int(h/2)


data=[]
pix = img.load()
length = len(chars)
data = ""
#扫描整个图片，按灰度置换图片
for i in range(0,h):
    line = ""
    for j in range(0,w):
        line += get_char(pix[j,i])
    data += line+"\n"

print(data)

with open("a.txt",'w') as f:
    f.write(data)

 

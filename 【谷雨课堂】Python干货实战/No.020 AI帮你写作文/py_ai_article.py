# coding:utf-8
# 【谷雨课堂】干货实战 No.020 "AI"帮你写作文
# 作者：谷雨
import random
import win32com.client

#语音合成输出
def speak(s):
    print("-->"+s)
    win32com.client.Dispatch("SAPI.SpVoice").Speak(s)

#内容数据
a1=['我','星际战士','西红柿','小白兔','大喇叭花']
a2=['在火星上','在海底里','在菜板上','在希望的田野上','在月球上']
a3=['用无线电给妈妈打电话','与海王用木棒打架','约土豆一起泡澡','和乌龟赛跑','大喊一声妈妈']
a4=['外星人','旁观者','土豆','蜗牛','全地球人']
a5=['激动的留下了泪水','直呼内行','瑟瑟发抖','疑惑为什么不带他','都被震聋了']

#随机在各数组取一句话
i1=random.randint(0,len(a1)-1)
s1=a1[i1]
i2=random.randint(0,len(a2)-1)
s2=a2[i2]
i3=random.randint(0,len(a3)-1)
s3=a3[i3]
i4=random.randint(0,len(a4)-1)
s4=a4[i4]
i5=random.randint(0,len(a5)-1)
s5=a5[i5]

#组合出来
s=s1+s2+","+s3+","+s4+s5
print(s)

#读出来
speak(s)


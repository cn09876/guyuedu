# coding:utf-8
# 【谷雨课堂】干货实战 No.012 读写文本文件
# 作者：谷雨



def ReadFile(filename,mode = 'r'):
    """
    读取文件内容
    @filename 文件名
    return string(bin) 若文件不存在，则返回空字符串
    """
    import os
    if not os.path.exists(filename): return ""

    fp = open(filename, mode,encoding="utf-8")
    f_body = fp.read()
    fp.close()
    return f_body


def WriteFile(filename,s_body,mode='w+'):
    """
    写入文件内容
    @filename 文件名
    @s_body 欲写入的内容
    """
    fp = open(filename, mode)
    fp.write(s_body)
    fp.close()

#读取文本文件
str=ReadFile("诗.txt")
print(str)

#写入文本文件
WriteFile("1.txt","hello tom cat")


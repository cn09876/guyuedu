# coding:utf-8
# 【谷雨课堂】干货实战 No.009 读取Excel文件
# 作者：谷雨

import xlrd

workbook = xlrd.open_workbook("员工信息.xlsx")
#第一个工作表
sheet1 = workbook.sheet_by_index(0)
#共多少行
nrows = sheet1.nrows
#共多少列
ncols = sheet1.ncols
row_values = sheet1.row_values(rowx=0)

#看看第一行（表头）是什么
print("共%d行%d列" % (nrows,ncols))
idx=0
for s in row_values:
    idx=idx+1
    print("第%d列=%s," % (idx,s))

#打每行的数据显示出来
for i in range(1,nrows):
    #这个record就是每行数据包装在一起的数组了
    record=sheet1.row_values(rowx=i)
    #可以单独取某列的数据
    s1=record[1]
    print(s1)
    
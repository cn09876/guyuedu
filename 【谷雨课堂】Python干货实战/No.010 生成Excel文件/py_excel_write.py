# coding:utf-8
# 【谷雨课堂】干货实战 No.010 生成Excel文件
# 作者：谷雨

#导入函数库
import xlwt

#新建一个workbook
workbook = xlwt.Workbook(encoding = 'utf-8')

#加入一个工作表
sheet1 = workbook.add_sheet('Sheet1')

#向单元格写入数据
#sheet1.write(行号,列号,数据)

#定义表头（第1行）
fields=['员工姓名','部门','性别']
idx=0
for x in fields:
    sheet1.write(0,idx, x)
    idx=idx+1

#写入1000条测试用的数据
for i in range(1,10001):
    col=0
    dt=["员工%d" % i,'工程部','男']
    for x in fields:
        sheet1.write(i,col,dt[col])
        col=col+1

#保存Excel文件
workbook.save("入职员工信息.xls")

#如果需要进行网络处理，也可以不保存文件，直接在内存中操作这个文件
#output = io.BytesIO()
    
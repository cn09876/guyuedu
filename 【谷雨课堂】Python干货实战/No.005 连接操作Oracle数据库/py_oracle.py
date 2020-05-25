<<<<<<< HEAD
# coding:utf-8
#【谷雨课堂】Python干货实战 No.005，用Python连接Oracle数据库

#导入cx_Oracle
import cx_Oracle

#建立连接
conn = cx_Oracle.connect("c##user1","user1","192.168.31.77:1521/hn")
cursor = conn.cursor()

#执行SQL语句
result=cursor.execute("select * from v$version")

#取返回的数据
all_data=cursor.fetchall()

#显示返回的数据
print(all_data)
=======
# coding:utf-8
#【谷雨课堂】Python干货实战 No.005，用Python连接Oracle数据库

#导入cx_Oracle
import cx_Oracle

#建立连接
conn = cx_Oracle.connect("c##user1","user1","192.168.31.77:1521/hn")
cursor = conn.cursor()

#执行SQL语句
result=cursor.execute("select * from v$version")

#取返回的数据
all_data=cursor.fetchall()

#显示返回的数据
print(all_data)
>>>>>>> 0c00c8166839b6e2267238f531145483435511c0

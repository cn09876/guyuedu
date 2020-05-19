## Oracle数据库在各大行业拥用不可替代的作用，
## 那么Python如何使用Oracle数据库呢？
## 谷雨老师干货实战走起~

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
 

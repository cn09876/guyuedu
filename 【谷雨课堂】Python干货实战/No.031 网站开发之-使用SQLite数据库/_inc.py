#-*- coding: UTF-8 -*-
import urllib
import json,uuid
import base64
import io
import os
import time 
import pymysql
import sqlite3
import mimetypes
from datetime import timedelta
from flask import request,Response,session,current_app,g
import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
import hashlib
from functools import update_wrapper,wraps
import struct
import datetime
import decimal
from decimal import Decimal
import itertools
from werkzeug.datastructures import Headers
from urllib.parse import quote
import re
from redis import Redis

POOL=None
DB_DS_POOL=None
swCache={}

true=True
false=False

#解决Object of type 'Decimal' is not JSON serializable的问题
#在app里调用 app.json_encoder = JSONEncoder
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,Decimal):
          return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self,o)

def redis_get(k):
    c =Redis(host='127.0.0.1',port=6379,password='vivian')
    data = c.get(k)
    return data
 
 
def redis_set(k,v,exp=None):
    c = Redis(host='127.0.0.1',port=6379,password='vivian')
    c.set(
        name=k,
        value=v,
        ex=exp  # 第三个参数表示Redis过期时间,不设置则默认不过期
    )

def loadCache():
    global swCache
    if os.path.isfile('_cache.bin'):
        with open("_cache.bin", "rb") as f:
            print("载入缓存信息")
            swCache = pickle.load(f)
loadCache()

def saveCache(): 
    global swCache
    with open("_cache.bin", "wb") as f:
        pickle.dump(swCache, f)

def c_del(k):
    global swCache
    if k in swCache:
        swCache.pop(k)

def c(k,v=None,exp=-1):
    global swCache
    if v==None:
        if k in swCache:
            if swCache[k]['e']==-1:
                return swCache[k]['v']
            else:
                if int(time.time())<=swCache[k]['e']:
                    return swCache[k]['v']
                else:
                    swCache.pop(k)
                    saveCache()
                    return None
        else:
            return None
    else:
        if exp>0:
            exp=int(time.time())+exp
        swCache[k]={
            'v':v,
            'e':exp,
        }
        saveCache()
        return v

def genUuid():
    s=str(uuid.uuid4())
    s=s.replace('-','').upper()
    return s

def hn_err(code=0,msg='',pl=''):
    return {
        'code':code,
        'msg':msg,
        'pl':pl
    }

def GetRandomString(length):
    """
       取随机字符串
       @length 要获取的长度
       return string(length)
    """
    from random import Random
    strings = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chrlen = len(chars) - 1
    random = Random()
    for i in range(length):
        strings += chars[random.randint(0, chrlen)]
    return strings


def GetJson(data):
    """
    将对象转换为JSON
    @data 被转换的对象(dict/list/str/int...)
    """
    from json import dumps
    if data == bytes: data = data.decode('utf-8')
    return dumps(data)



def ReadFile(filename,mode = 'r'):
    """
    读取文件内容
    @filename 文件名
    return string(bin) 若文件不存在，则返回None
    """
    import os
    if not os.path.exists(filename): return False
    try:
        fp = open(filename, mode)
        f_body = fp.read()
        fp.close()
    except:
        fp = open(filename, mode,encoding="utf-8")
        f_body = fp.read()
        fp.close()

    return f_body


def DataService_GetInfo(service_sn):
    srv_info=c("__ds.info."+service_sn)
    if srv_info==None:
        srv_info=dbs(tbl_name).query("select * from %s where sn='%s' " % (tbl_name,service_sn) )
        c("__ds.info."+service_sn,srv_info)
    else:
        print("dataservice get meta use cache")
        pass

    if len(srv_info)==0:
        return None
    return srv_info[0]


#如果有逗号分隔的，就直接写，否则就从数据源中获取
def get_etc_info(etc):
    etc=etc.replace("，",",")
    etc=etc.replace("|",",")
    etc=etc.replace("/",",")
    etc=etc.replace("、",",")
    rows=[]
    rows.append({'k':'','v':'请选择'})
    if ',' in etc:
        for s in etc.split(','):
            rows.append({'k':s,'v':s})
    else:
        ds_etc_info=DataService_GetInfo(etc)
        if ds_etc_info==None:
            rows.append({'k':'','v':'数据服务配置错误，没有数据源：'+etc})
        else:
            ret=db_rest_api(ds_etc_info['ds_sn'],ds_etc_info['sql'],'list',None,{})
            for r in ret['data']:
                k=''
                v=''
                idx1=0
                for ks in r.keys():
                    if idx1==0:k=ks
                    if idx1==1:v=ks
                    idx1=idx1+1
                if v=='':v=k
                rows.append({'k':r[k],'v':r[v]})
    return rows


def WriteFile(filename,s_body,mode='w+'):
    """
    写入文件内容
    @filename 文件名
    @s_body 欲写入的内容
    return bool 若文件不存在则尝试自动创建
    """
    try:
        fp = open(filename, mode);
        fp.write(s_body)
        fp.close()
        return True
    except:
        try:
            fp = open(filename, mode,encoding="utf-8");
            fp.write(s_body)
            fp.close()
            return True
        except:
            return False    


def ExecShell(cmdstring, cwd=None, timeout=None, shell=True):
    #通过管道执行SHELL
    import shlex
    import datetime
    import subprocess
    import time

    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE,shell=shell,bufsize=4096,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s"%cmdstring)
    a,e = sub.communicate()
    try:
        if type(a) == bytes: a = a.decode('utf-8')
        if type(e) == bytes: e = e.decode('utf-8')
    except:pass
    return a,e


def GetHost(port = False):
    from flask import request
    host_tmp = request.headers.get('host')
    if host_tmp.find(':') == -1: host_tmp += ':80';
    h = host_tmp.split(':')
    if port: return h[1]
    return h[0]

def GetClientIp():
    from flask import request
    return request.remote_addr.replace('::ffff:','')

#过滤输入
def checkInput(data):
   if not data: return data;
   if type(data) != str: return data;
   checkList = [
                {'d':'<','r':'＜'},
                {'d':'>','r':'＞'},
                {'d':'\'','r':'‘'},
                {'d':'"','r':'“'},
                {'d':'&','r':'＆'},
                {'d':'#','r':'＃'},
                {'d':'<','r':'＜'}
                ]
   for v in checkList:
       data = data.replace(v['d'],v['r']);
   return data;

#字节单位转换
def to_size(size):
    d = ('b','KB','MB','GB','TB')
    s = d[0]
    for b in d:
        if size < 1024: return ("%0.2f" % size) + ' ' + b
        size = size / 1024
        s = b
    return ("%0.2f" % size)  + ' ' + b

def downloadFile(url,filename):
    try:
        if sys.version_info[0] == 2:
            import urllib
            urllib.urlretrieve(url,filename=filename ,reporthook= downloadHook)
        else:
            import urllib.request
            urllib.request.urlretrieve(url,filename=filename ,reporthook= downloadHook)
    except:
        return False
    
def downloadHook(count, blockSize, totalSize):
    speed = {'total':totalSize,'block':blockSize,'count':count}
    #print('%02d%%'%(100.0 * count * blockSize / totalSize))
 

#检查是否为IPv4地址
def checkIp(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False
    
def getDate(format='%Y-%m-%d %X'):
    #取格式时间
    return time.strftime(format,time.localtime())

#取文件或目录大小
def get_path_size(path):
    if not os.path.exists(path): return 0;
    if not os.path.isdir(path): return os.path.getsize(path)
    size_total = 0
    for nf in os.walk(path):
        for f in nf[2]:
            filename = nf[0] + '/' + f
            if not os.path.exists(filename): continue;
            if os.path.islink(filename): continue;
            size_total += os.path.getsize(filename)
    return size_total



#字符串取中间
def getPart(srcStr,startStr,endStr):
    start = srcStr.find(startStr)
    if start == -1: return None
    end = srcStr.find(endStr)
    if end == -1: return None
    return srcStr[start+1:end]

#取CPU类型
def getCpuType():
    cpuinfo = open('/proc/cpuinfo','r').read();
    rep = "model\s+name\s+:\s+(.+)"
    tmp = re.search(rep,cpuinfo);
    cpuType = None
    if tmp:
        cpuType = tmp.groups()[0];
    return cpuType;

#获取mac
def get_mac_address():
    import uuid
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


#返回MD5值
def md5(s):
    s = hashlib.md5(s.encode('utf-8'))# MD5加密
    s = s.hexdigest()# MD5加密
    return s

def get_pwd(s):
    return md5(s+'sdf')
#转换为整数，失败返回0
def cint(s):
    try:
        return int(s)
    except:
        return 0

#记录日志
def l(s):
    logging.info(s)
    db_log=dbs("hn_sys_logs","logs")
    db_log.f("uid",g.uid)
    db_log.f("txt",s)
    db_log.f("ip",ip())
    db_log.f("ptime",now())
    db_log.add()

def ip():
    return request.remote_addr

def now():
    return str(datetime.datetime.now())

#取得get参数
def rq(k):
    '''
    返回HTTP GET请求值
    :param k: GET的KEY
    :return: 返回值，不存在返回空
    '''
    return request.args.get(k,type=str,default='')

#取得form表单参数
def rf(k):
    try:
        return request.form[k]
    except:
        return ""

def model(tbl='',cn=None):
    return cls_getrs(tbl,cn)

#执行SQL返回第一行第一列
def query(sql):
    cn=get_conn()
    #cursor=pymysql.cursors.DictCursor,返回的结果集是以键值对的形式
    c=cn.cursor(cursor=pymysql.cursors.DictCursor)
    c.execute(sql)
    #print(c.description)
    data=c.fetchall()
    return data

def d(sql):
    '''
    查询数据库，返回结果集
    :param sql: 要执行的SQL查询语句
    :return: 结果集
    '''
    return query(sql)

#执行SQL返回第一行第一列
def sv(sql):
    cn=get_conn()
    print(type(cn))
    c=cn.cursor()
    c.execute(sql)
    data=c.fetchone()
    if data==None:return ""
    if data[0]==None:return ""
    return str(data[0])

#执行SQL语句无返回
def q(sql):
    cn=get_conn()
    c=cn.cursor()
    c.execute(sql)
    cn.commit()
    return ""

def rnd(l=32):
    '''
    生成指定长度的随机字符串
    :param l: 长度，默认32
    :return:
    '''
    return os.urandom(l)

def ses(k,v=None):
    if v==None:
        ret=session.get(k)
        if ret==None:
            ret=""
        return ret
    else:
        session[k]=v

class csw_msg():
    code=0
    msg=""
    def __init__(self,code_,msg_):
        self.code=code_
        self.msg=msg_

def msg(code,msg=''):
    return {'code':code,'msg':msg}


def fileexists(ff):
    return os.path.exists(ff)



def upfile_ex_stu_pic(field=''):

    if len(request.files)<1:
        return ""

    if field=='':
        for k in request.files:
            field=k
            break

    f = request.files[field]
    if f==None:
        print("没有上传的字段"+field)
        return ""
    fname = f.filename
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time)  # 修改了上传的文件名
    new_filename_ok=new_filename+ '.' + ext 
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    dir_=os.path.join(STATIC_DIR,'photos')
    f.save(dir_+'/'+new_filename_ok)
    return new_filename,fname,ext,field



def upfile(field='',dir=''):

    if len(request.files)<1:
        return ""

    if field=='':
        for k in request.files:
            field=k
            break

    f = request.files[field]
    if f==None:
        print("没有上传的字段"+field)
        return ""
    fname = f.filename
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    str_ymd = time.strftime("%Y-%m-%d", timeStruct)
    if dir=='':dir=str_ymd
    if not os.path.exists(UPLOAD_DIR+"/"+dir):
        os.makedirs(UPLOAD_DIR+"/"+dir)
    f.save(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    return dir+'/'+new_filename

def upfile_ex(field='',dir=''):

    if len(request.files)<1:
        return ""

    if field=='':
        for k in request.files:
            field=k
            break

    f = request.files[field]
    if f==None:
        print("没有上传的字段"+field)
        return ""
    fname = f.filename
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    str_ymd = time.strftime("%Y-%m-%d", timeStruct)
    if dir=='':dir=str_ymd
    if not os.path.exists(UPLOAD_DIR+"/"+dir):
        os.makedirs(UPLOAD_DIR+"/"+dir)
    f.save(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    return dir+'/'+new_filename,fname,ext,field

class cls_getrs():

    __tablename = ""
    __sql = ""
    __where=""
    __fields=""
    __page=1
    __pageSize=10
    __cn=None
    fields_info = {}

    def __init__(self, sql_or_tablename='',cn=None):
        self.__tablename = ""
        self.__sql = ""
        self.__where=""
        self.__fields=""
        self.__page=1
        self.__pageSize=10
        self.__cn=None
        self.fields_info = {}
                
        sql_or_tablename = str(sql_or_tablename)
        self.__cn=cn
        if sql_or_tablename.upper().find("SELECT ") >= 0 or sql_or_tablename.upper().find("DESCRIBE ") >= 0 or sql_or_tablename.upper().find("SHOW ") >= 0:
            self.__sql = sql_or_tablename
        else:
            self.__tablename = sql_or_tablename
        
    #执行SQL返回第一行第一列
    def query(self,sql):
        if self.__cn==None:
            self.__cn=get_conn()

        cc=self.__cn.cursor(cursor=pymysql.cursors.DictCursor)
        cc.execute(sql)     
        print("fields....")           
        print(cc.description)
        data=cc.fetchall()
        print(data)
        return data
    

    def cols(self,sql):
        if self.__cn==None:
            self.__cn=get_conn()
        c=self.__cn.cursor()
        if sql.upper().find("SELECT")>=0:
            pass
        else:
            sql="select * from "+sql+" where 1>2 "
        c.execute(sql)
        col = c.description
        cols=[]
        for x in col:
            cols.append({
                'title':x[0],
                'typ':'varchar',
                'len':0,
                'info':x[0]
            })
        print(cols)
        tbl=self.suggestTableNameBySql(sql)
        print("TableName="+tbl)
        sql="SELECT column_name,data_type,character_maximum_length AS l,is_nullable,CASE WHEN extra = 'auto_increment' THEN 1 ELSE 0 END AS auto_inc,column_default,column_comment FROM Information_schema.columns WHERE table_Name='"+tbl+"'  "
        for x in self.query(sql):
            #print(x['column_comment'])
            for c in cols:
                if c['title']==x['column_name']:
                    info=x['column_comment']
                    info=info.replace('，',',')
                    if ',' in info:
                        info=info[0:info.find(',')]
                    c['len']=x['l']
                    c['typ']=x['data_type']
                    c['info']=info
        return cols

    #执行SQL返回第一行第一列
    def sv(self,sql):
        if self.__cn==None:
            self.__cn=get_conn()
        c=self.__cn.cursor()
        c.execute(sql)
        data=c.fetchone()
        if data==None:return ""
        if data[0]==None:return ""
        return str(data[0])

    #执行SQL语句无返回
    def q(self,sql):
        if self.__cn==None:
            self.__cn=get_conn()
        print(sql)
        c=self.__cn.cursor()
        c.execute(sql)
        self.__cn.commit()
        return self

    def suggestTableNameBySql(self,sql):
        i_from=sql.lower().find(" from ")
        i_where=sql.lower().find(" where ")
        i_order=sql.lower().find(" order ")
        i_group=sql.lower().find(" group ")
        i_limit=sql.lower().find(" limit ")
        tbl=sql[i_from+5:]
        if i_order>0:tbl=tbl=sql[i_from+5:i_order]
        if i_group>0 and i_group<i_order:tbl=tbl=sql[i_from+5:i_group]
        if i_where>0:tbl=tbl=sql[i_from+5:i_where]
        return tbl.strip()

    #根据SQL语句检测表名
    def suggestTableName(self):
        if self.__sql=='':
            return self.__tablename
        
        i_from=self.__sql.lower().find(" from ")
        i_order=self.__sql.lower().find(" order ")
        i_group=self.__sql.lower().find(" group ")
        tbl=self.__sql[i_from+5:]
        if i_order>0:tbl=tbl=self.__sql[i_from+5:i_order]
        if i_group>0 and i_group<i_order:tbl=tbl=self.__sql[i_from+5:i_group]
        return tbl.strip()

    def all(self,page=-1,limit=15):
        print("page=%d,limit=%d,where=%s" % (page,limit,json.dumps(self.__where)))
        if limit<1:limit=15
        offset=(page-1)*limit
        
        sql=self.__sql
        if sql=="":sql="select * from "+self.__tablename
        if self.__where!='':
            sql=sql+" where 1 "+self.__where

        if ('limit' not in sql) and page>0:
            sql=sql+" limit %d,%d " % (offset,limit)

        print(sql)
        return self.query(sql)

    def field(self, k, v):
        if k=='id':
            return self
        #print("set %s=%s" % (k,v))
        self.fields_info[k] = v
        return self

    def f(self, k, v):
        return self.field(k, v)

    def value(self, k):
        if k in self.fields_info.keys():
            s = self.fields_info[k]
            if s == None: s = ""
            return s
        else:
            return ""

    def v(self, k):
        return self.value(k)

    def __setattr__(self,k,v):
        self.__dict__[k]=v

    def __getattr__(self, item):
        return self.v(item)

    def count(self):
        sql=""
        if self.__sql=="":
            sql="select count(*) from "+self.__tablename
            if self.__where!="":
                sql=sql+" where 1 "+self.__where
        else:
            sql=self.__sql
            if self.__where!="":
                sql=sql+" where 1 "+self.__where
        #print('111111111111111111111111')
        i_select=sql.lower().find("select ")
        i_from=sql.find(" from ")
        i_order=sql.find(" order ")
        i_group=sql.find(" group ")
        #print("i_select=%d" % i_select)
        #print("i_from=%d" % i_from)
        #print("i_order=%d" % i_order)
        #print("i_group=%d" % i_group)
        #print("TableName=%s" % self.suggestTableName())

        print(sql)
        s_from=sql[i_from:]
        sql_count="select count(*) "+s_from
        print(sql_count)

        return cint(self.sv(sql_count))

    def get(self,id_):
        tbl_name=self.suggestTableName()
        sql="select * from "+tbl_name
        if cint(id_)>0:
            sql=sql+" where id=0"+id_
        else:
            sql=sql+' where '+id_
        sql=sql+' limit 1'
        
        r=self.query(sql)
        if len(r)>0:
            return r[0]
        return None

    def add(self):
        arrk = []
        arrv_p = []
        arrv = []
        for (k, v) in self.fields_info.items():
            arrk.append(k)
            arrv.append(v)
            arrv_p.append('%s')

        sql = "insert into `" + self.suggestTableName() + "` (" + ",".join(arrk) + ") values (" + ",".join(arrv_p) + ")"

        if self.__cn==None:
            self.__cn=get_conn()
        c = self.__cn.cursor()
        try:
            c.execute(sql,arrv)
            self.__cn.commit()
        except Exception as e1:
            print("SQL.add=%s" % sql)
            raise e1

        return self

    def delete(self,id_or_where):
        '''
        删除记录
        :param id_or_where:如果传入大于0的数值则删除指定ID，否则当作where处理
        :return:
        '''
        if cint(id_or_where)>0:
            self.q("delete from `" + self.suggestTableName() + "` where id=0"+str(id_or_where))
        else:
            self.q("delete from `" + self.suggestTableName() + "` where "+id_or_where)
        return self

    def save(self,id_or_where):
        where=""
        if cint(id_or_where)>0:
            where=" id=0"+str(id_or_where)
        else:
            where=id_or_where

        if cint(sv("select count(*) from "+self.suggestTableName()+" where "+where))>0:
            return self.update(id_or_where)
        else:
            return self.add()

    def update(self, id_or_where):
        arrk = []
        arrv = []
        for (k, v) in self.fields_info.items():
            arrk.append("`"+k+"`=%s")
            arrv.append(v)
            print("%s=%s" % (k,v))

        where=""
        if cint(id_or_where)>0:
            where=" id=0"+str(id_or_where)
        else:
            where=id_or_where
        sql = "update `" + self.suggestTableName() + "` set  "+(",".join(arrk))+" where "+where

        print(sql)
        if self.__cn==None:
            self.__cn=get_conn()
        c = self.__cn.cursor()
        try:
            c.execute(sql,arrv)
        except Exception as e:
            raise Exception("SQL Error: %s , %s" % (sql,str(e) ))
        self.__cn.commit()
        return self

    def fields(self,dt):
        if isinstance(dt,str):
            self.__fields=dt
            return self
        self.__fields=",".join(dt)
        return self

    def where(self,dt):
        self.__where=""
        if isinstance(dt,str):
            self.__where=dt
            return self

        if len(dt)>0:
            for k in dt.keys():
                if dt[k]!='':
                    self.__where=self.__where+" and  `%s` like '%%%s%%' " % (k,dt[k])
        return self
    
    def page(self,p,pageSize=10):
        self.__page=p
        self.__pageSize=pageSize
        return self
    
    def limit(self,p,pageSize=10):
        return self.page(p,pageSize)
    
    def countSelect():
        self.__count=self.count()
        sql=''
        if self.__sql=='':
            sql="select %s from %s " % (self.__fields,self.__tablename)
            if self.__where!='':
                sql=sql+" where "+self.__where
        else:
            sql=self.__sql
        sql=sql+" limit %d,%d " % ((self.__page-1)*self.__pageSize,self.__pageSize)

        ret={
            'page':self.__page,
            'count':self.__count,
            'data':self.query(sql)
        }
        return ret

def http_direct_view(stream,filename):
    response = Response()
    response.status_code = 200
    response.data = stream
    mimetype_tuple = mimetypes.guess_type(filename)
    response_headers = Headers({
            'Content-Type': mimetype_tuple[0],
            'Content-Transfer-Encoding': 'binary',
            'Content-Length': len(response.data)
        })
    response.headers = response_headers
    return response

def http_download(stream,filename):
    response = Response()
    response.status_code = 200
    response.data = stream
    mimetype_tuple = mimetypes.guess_type(filename)
    response_headers = Headers({
            'Pragma': "public",  # required,
            'Expires': '0',
            'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
            'Content-Type': mimetype_tuple[0],
            'Content-Disposition': 'attachment; filename=\"%s\";' % quote(filename),
            'Content-Transfer-Encoding': 'binary',
            'Content-Length': len(response.data)
        })
    response.headers = response_headers
    return response

def sw_cache(exp=-1):
    @wraps(exp)
    def wraper(fn):
        def run(*args, **kwargs):
            k=md5(fn.__name__+json.dumps(args))
            print("test cache "+k)
            v=c(k)
            if v==None:
                v=fn(*args, **kwargs)
                print("实际执行的结果："+json.dumps(v))
                c(k,v,exp)
            return v
        return run
    return wraper


def sw_login(func):
    '''
    需要登录的装饰器,如果没有登录会引导到登录页/login
    '''
    '''
    需要权限的装饰器
    '''
    @wraps(func)
    def wraper(*args, **kwargs):
        token_v=get_token()
        if token_v==None:
            return "<a href='/login?rnd="+now()+"' style='color:red;'>您的会话无效，请登录</a><script>location.href='/login?rnd="+now()+"';</script>"
        return func(*args, **kwargs)
    return wraper

def suggestTableNameBySql(sql):
    i_from=sql.lower().find(" from ")
    i_where=sql.lower().find(" where ")
    i_order=sql.lower().find(" order ")
    i_group=sql.lower().find(" group ")
    tbl=sql[i_from+5:]
    if i_order>0:tbl=tbl=sql[i_from+5:i_order]
    if i_group>0 and i_group<i_order:tbl=tbl=sql[i_from+5:i_group]
    if i_where>0:tbl=tbl=sql[i_from+5:i_where]
    return tbl.strip()


def sw_token(fn):
    '''
    此装饰器用于需要保护的REST API接口
    分别尝试从get,form,header中获取token,并进行匹配，不通过的输出JSON错误code=-200
    '''
    @wraps(fn)
    def run():
        token_v=get_token()
        if token_v==None:
            return {'code':-200,'msg':'token expired or error','token':token}
        g.token=token_v
        return fn()
    return run

def get_token():
    token=rq("token")
    if token=='':
        token= rf("token")
    if token=='':
        token= request.headers.get("token")
    if token=='':token=None
    if token==None:return None
    token_v=c(token)
    if token_v!=None:token_v['token']=token
    return token_v

def sw_auth(role=''):
    '''
    需要权限的装饰器
    '''
    @wraps(role)
    def wraper(fn):
        def run(*args, **kwargs):
            #if ses("login_role")!=role:
            #    return "role %s required " % role
            return fn(*args, **kwargs)
        return run
    return wraper



#压缩ZIP文件
def to_zip(f_from,f_to,f_name):
    z = zipfile.ZipFile(f_to, 'w',zipfile.ZIP_DEFLATED) 
    z.write(f_from,f_name)
    z.close()

############################################################################################
############################################################################################
#
# 以下是全局变量
# 
############################################################################################
############################################################################################

ac=""
id=0
http_method="GET"
request_path=""

#基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#static路径
STATIC_DIR = os.path.join(BASE_DIR,'static')

#templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

#上传路径
UPLOAD_DIR = os.path.join(STATIC_DIR,'upload')

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR) 


#本地SQLITE数据库
class HN_DBLocal:
    global BASE_DIR
    __dbname=os.path.join(BASE_DIR,'maindb.db')
    __tablename = ""
    __sql = ""
    __limit_offset=-1
    __page_size=15
    __page=1
    __orderby=''
    __where=""


    fields = {}
    
    def __init__(self, sql_or_tablename='',db_name=None):
        self.fields={}
        if db_name!=None:
            self.__dbname=os.path.join(BASE_DIR,"db/"+db_name+".db")
        sql_or_tablename = str(sql_or_tablename)
        if sql_or_tablename.upper().find("SELECT ") >= 0:
            self.__sql = sql_or_tablename
        else:
            self.__tablename = sql_or_tablename
    def getconn(self):
        return sqlite3.connect(self.__dbname)
    #取第一条记录
    def get(self,id):
        ret={}
        if id==None:
            return ret
            
        rs=self.query("select * from "+self.__tablename+" where id=0"+str(id))
        if len(rs)>0:
            ret=rs[0]
        return ret
    def q(self,sql):
        cn = self.getconn()
        c=cn.cursor()
        c.execute(sql)
        cn.commit()
        cn.close()
        return ""
    def maxid(self):
        return self.sv("select max(id) from "+self.__tablename)
    def sv(self,sql):
        cn = self.getconn()
        c=cn.cursor()
        c.execute(sql)
        data=c.fetchone()
        if data==None:return ""
        if data[0]==None:return ""
        cn.close()
        return str(data[0])
    def create(self,tbl_name,fld_def):
        self.q('CREATE TABLE ['+tbl_name+'] ([ID] INTEGER PRIMARY KEY,'+fld_def+');')
    def create_(self,tbl_name,fld_def):
        try:
            self.create(tbl_name,fld_def)
        except:
            pass
    def drop(self,tbl_name):
        self.q('drop TABLE ['+tbl_name+'] ;')
    def drop_(self,tbl_name):
        try:
            self.drop(tbl_name)
        except:
            pass
    def data(self,dt):
        if type(dt) is dict:
            for k,v in dt.items():
                self.field(k,v)
            return self
        else:
            raise Exception("batch data need dict,input type is %s " % type(dt))
        return self

    def where(self,dt):
        self.__where=""
        if len(dt)>0:
            for k in dt.keys():
                if dt[k]!='':
                    self.__where=self.__where+" and  `%s` like '%%%s%%' " % (k,dt[k])
        return self

    def limit(self,a,b=None):
        self.__limit_offset=a
        if b!=None:self.__page_size=b
        return self
    def orderby(self,orderby_):
        self.__orderby=orderby_
        return self

    def page(self,p,page_size):
        self.__page=p
        self.__page_size=page_size
        return self
    def suggestTableName(self):
        if self.__sql=='':
            return self.__tablename
        
        i_from=self.__sql.lower().find(" from ")
        i_order=self.__sql.lower().find(" order ")
        i_group=self.__sql.lower().find(" group ")
        tbl=self.__sql[i_from+5:]
        if i_order>0:tbl=tbl=self.__sql[i_from+5:i_order]
        if i_group>0 and i_group<i_order:tbl=tbl=self.__sql[i_from+5:i_group]
        return tbl.strip()
    def all(self,page=-1,limit=15):
        sql=self.__sql
        if sql=="":
            sql="select * from "
        sql=sql+self.__tablename
        if self.__where!="":
            sql=sql+" where 1 "+self.__where
        if self.__orderby!="":
            sql=sql+" order by "+self.__orderby
        if page>0:
            offset=(page-1)*limit
            sql=sql+" limit %d,%d " % (offset,limit)

        return self.query(sql)

    def count(self):
        sql=""
        if self.__sql=="":
            sql="select count(*) from "+self.__tablename
            if self.__where!="":
                sql=sql+" where 1 "+self.__where
        else:
            sql=self.__sql
            if self.__where!="":
                sql=sql+" where 1 "+self.__where
        print('111111111111111111111111')
        i_select=sql.lower().find("select ")
        i_from=sql.find(" from ")
        i_order=sql.find(" order ")
        i_group=sql.find(" group ")
        print("i_select=%d" % i_select)
        print("i_from=%d" % i_from)
        print("i_order=%d" % i_order)
        print("i_group=%d" % i_group)
        print("TableName=%s" % self.suggestTableName())

        print(sql)
        s_from=sql[i_from:]
        sql_count="select count(*) "+s_from
        print(sql_count)

        return cint(self.sv(sql_count))

    def query(self,sql):
        cn=self.getconn() 
        c=cn.cursor()
        c.execute(sql)
        col_name_list = [tuple[0] for tuple in c.description] 
        print(col_name_list)
        data=c.fetchall()
        lst=[]
        for r in data:
            row={}
            idx=0
            for fld in col_name_list:
                row[fld]=r[idx]
                if row[fld]==None:
                    row[fld]=''
                idx=idx+1
            lst.append(row)
        cn.close()
        return lst
    def items(self,page=1,pagezie=10):
        pass
    def field(self, k, v):
        self.fields[k] = v
        return self

    def f(self, k, v):
        return self.field(k, v)

    def value(self, k):
        if k in self.fields.keys():
            s = self.fields[k]
            if s == None: s = ""
            return s
        else:
            return ""

    def v(self, k):
        return self.value(k)

    def __setattr__(self,k,v):
        self.__dict__[k]=v

    def __getattr__(self, item):
        return self.v(item)

    def add(self):
        arrk = []
        arrv_p = []
        arrv = []
        for (k, v) in self.fields.items():
            arrk.append(k)
            arrv.append(v)
            arrv_p.append('?')

        sql = "insert into `" + self.__tablename + "` (" + ",".join(arrk) + ") values (" + ",".join(arrv_p) + ")"
        cn = self.getconn()
        c = cn.cursor()
        try:
            c.execute(sql,arrv)
        except Exception as e:
            raise Exception('SQL Error: ' +sql+'<br>'+str(e) )
        cn.commit()
        return self

    def delete(self,id_or_where):
        '''
        删除记录
        :param id_or_where:如果传入大于0的数值则删除指定ID，否则当作where处理
        :return:
        '''
        if cint(id_or_where)>0:
            self.q("delete from `" + self.__tablename + "` where id=0"+str(id_or_where))
        else:
            self.q("delete from `" + self.__tablename + "` where "+id_or_where)
        return self

    def save(self,id_or_where=None):

        if id_or_where==None:
            return self.add()

        where=""
        if cint(id_or_where)>0:
            where=" id=0"+str(id_or_where)
        else:
            where=id_or_where

        return self.update(id_or_where)

    def update(self, id_or_where):
        arrk = []
        arrv = []
        for (k, v) in self.fields.items():
            arrk.append("`"+k+"`=?")
            arrv.append(v)

        where=""
        if cint(id_or_where)>0:
            where=" id=0"+str(id_or_where)
        else:
            where=id_or_where
        sql = "update `" + self.__tablename + "` set  "+(",".join(arrk))+" where "+where
        cn = self.getconn()
        c = cn.cursor()
        c.execute(sql,arrv)
        cn.commit()
        cn.close()
        return self


#返回数据库连接cursor,ds_name是数据源名称，如果没指定就是默认的
def get_conn(ds_name=''):
    global DB_DS_POOL
    if DB_DS_POOL==None:
        DB_DS_POOL={}
    
    sql="select * from hn_sys_data_sources where sn='"+ds_name+"' "

    #查找默认数据库
    if ds_name=='':
        sql="select * from hn_sys_data_sources where is_default='1' "
    

    rs=dbs(sql).all()
    if len(rs)==0:
        if ds_name=='':
            raise Exception("no default datasource defined ")
        else:
            raise Exception("datasource [%s] not found" % (ds_name))

    typ=rs[0]['typ']
    host=rs[0]['host']
    port=rs[0]['port']
    uid=rs[0]['uid']
    pwd=rs[0]['pwd']
    db=rs[0]['db']

    if ds_name not in DB_DS_POOL:
        DB_DS_POOL[ds_name]=None    
        
    if DB_DS_POOL[ds_name]==None:
        DB_DS_POOL[ds_name] = PooledDB(
            creator=pymysql,
            ping=0,
            host=host,
            port=int(port),
            user=uid,
            password=pwd,
            database=db,
            charset='utf8'
        )
    
    conn=None
    conn=DB_DS_POOL[ds_name].connection()
    
    return conn

def test_conn(host,port,uid,pwd,db):
    ok=false
    msg=''
    try:
        ccn=PooledDB(
                creator=pymysql,
                ping=0,
                host=host,
                port=int(port),
                user=uid,
                password=pwd,
                database=db,
                charset='utf8'
            )        
        conn=ccn.connection()
        ok=true
        msg="数据源连接成功 %s@%s:%s" % (uid,host,str(port))
    except Exception as e:
        ok=false
        msg=str(e)
    
    return ok,msg


#数据访问的中间件，所有数据访问都通过此方法进行
def db_rest_api(ds,tbl,ac,id_,dt):
    
    code=0
    data=[]
    msg=''
    count=0

    if ds=='local':
        if ac=='list':
            try:
                data=dbs(tbl).all()
                code=1
            except Exception as e:
                code=-1
                msg=str(e)
        if ac=='del':
            try:
                dbs(tbl).delete(id_)
                code=1
            except Exception as e:
                code=-1
                msg=str(e)
        if ac=='get':
            try:
                data=dbs(tbl).get(id_)
                code=1
            except Exception as e:
                code=-1
                msg=str(e)
        if ac=='add':
            try:
                r=dbs(tbl)
                for (k,v) in  dt.items():
                    r.field(k,v)
                r.add()
                code=1
            except Exception as e:
                code=-1
                msg=str(e)
        if ac=='edit':
            try:
                r=dbs(tbl)
                for (k,v) in  dt.items():
                    r.field(k,v)
                r.update(id_)
                code=1
            except Exception as e:
                code=-1
                msg=str(e)
    else:
        conn=get_conn(ds)
        if conn==None:
            return {'code':-1,"msg":'error connect db'}
        if tbl=='show_tables':
            r=cls_getrs("SHOW TABLES",conn).all()
            data=[]
            for x in r:
                for k,v in x.items():
                    data.append(v)            
        if ac=='list':
            page=0
            limit=15
            where=[]
            if 'page' in dt:page=cint(dt['page'])
            if 'limit' in dt:limit=cint(dt['limit'])
            if 'where' in dt:where=dt['where']

            rs=cls_getrs(tbl,conn)
            rs.where(where)

            count=rs.count()
            data=rs.all(page,limit)
            
            code=1

        if ac=='del':
            try:
                cls_getrs(tbl,conn).delete(id_)
                code=1
            except Exception as e:
                return {'code':-2,"msg":str(e)}
        if ac=='schema':
            data=cls_getrs(tbl,conn).cols(tbl)
        if ac=='get':
            try:
                data=cls_getrs(tbl,conn).get(id_)
                #print(data)
                code=1
            except Exception as e:
                return {'code':-2,"msg":str(e)}
        if ac=='add':
            r=cls_getrs(tbl,conn)
            for (k,v) in  dt.items():
                print("%s=%s" % (k,v))
                r.field(k,v)
            r.add()
            code=1

        if ac=='edit':
            print("edit a mysql record")
            r=cls_getrs(tbl,conn)
            print("payload:")
            print(dt)
            print("r __fields now")
            print(r.fields_info)
            for (k,v) in  dt.items():
                r.field(k,v)
            print("r __fields after")
            print(r.fields_info)
            r.update(id_)
            code=1
                            
    return {
        'datasource':ds
        ,'code':code
        ,'msg':msg
        ,'table_name':tbl
        ,'action':ac
        ,'count':count
        ,'data':data
        ,'payload':dt
    }

dblocal=HN_DBLocal()
def dbs(tbl='',db_name=None):
    return HN_DBLocal(tbl,db_name)

def reg_(k,v=None):
    ret=""
    if v==None:
        ret=c("_reg."+k)
        if ret==None:
            ret=dbs().sv("select v from hn_sys_reg where k='%s' " % k)
            c("_reg."+k,ret)
        else:
            pass
    else:
        dbs().q("delete from hn_sys_reg where k='%s' " % k)
        dbs("hn_sys_reg").f("k",k).f("v",v).add()
        c("_reg."+k,v)

    return ret

def get_roles_by_dept_id(id):
    ret=[]
    rs=dbs("hn_sys_roles").where({'group_id':id}).all()
    for r in rs:
        ret.append(r['role_id'])
    return ret


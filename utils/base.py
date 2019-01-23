import winreg,socket,time,sys,os,shutil
from smb.SMBHandler import SMBHandler
import urllib.request
from utils import gol
from string import Template
import platform
import zipfile
from collections import OrderedDict
# funcName = sys._getframe().f_back.f_code.co_name  #获取调用函数名
# lineNumber = sys._getframe().f_back.f_lineno      #获取行号
# print(sys._getframe().f_code.co_name)             # 获取当前函数名


# 获取桌面地址
def desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    return winreg.QueryValueEx(key, "Desktop")[0]

def get_system():
    # 根据系统版本 不靠谱
    # system = platform.platform()
    # if 'Windows-7' in system:
    #     return 'win7'
    # elif 'Windows-XP' in system:
    #     return 'winxp'
    # else:
    #     return False
    # 根据python版本 3.4 XP  3.5及以上win7
    if '3.4' in platform.python_version():
        return 'winxp'
    else:
        return 'win7'

def hostname():
    try:
        return socket.getfqdn(socket.gethostname())
    except Exception as e:
        return '未知主机'

def hostip():
    try:
        return socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    except Exception as e:
        return '未知IP'

def str2(para):
    if not para:
        return ''
    else:
        if isinstance(para,str):
            if para.isdigit():           # 是否都是数字
                return para
            else:
                try:
                    return para.encode('latin-1').decode('gbk')
                except Exception as e:
                    # print('%s 转换失败！错误信息：%s' %(para,e))
                    return para
        else:
            return str(para)

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

def cur_date():
    return time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

# 初始化-查找文件
def fileiter(root_path):
    for root, dirs, files in os.walk(root_path):
        if files and not dirs:  # 必须是指定目录的下级目录
            for file in files:
                yield os.path.join(root, file), file

# 获取图片/文件
class RemoteFileHandler(object):

    def __init__(self,user,passwd):
        self.user =user
        self.passwd= passwd
        self.smbconn = urllib.request.build_opener(SMBHandler)

    def down(self,file_remote,file_local):
        file_url = "smb://%s:%s@%s" %(self.user,self.passwd,file_remote)
        try:
            with self.smbconn.open(file_url) as f:
                fh = open(file_local, "wb")
                fh.write(f.read())
                f.close()
                fh.close()
                return True,''
        except Exception as e:
            return False,e

def get_key(p_dict, p_value):

    tmp = [k for k, v in p_dict.items() if v == p_value]
    if tmp:
        return tmp[0]
    else:
        return '00000'

def version_sort(versions):
    # versions = ['v2.0.1', 'v1.0.2', 'v1.0.21', 'v2.2.9', 'v1.2.11']
    # ['v1.0.2', 'v1.0.21', 'v1.2.11', 'v2.0.1', 'v2.2.9']
    return sorted(versions, key=lambda x: tuple(int(v) for v in x.replace('v', '').split(".")))

# 模板替换变量采用的是$符号，而不是%，它的使用要遵循以下规则：
# 1、$$ 是需要规避，已经采用一个单独的 $代替（$$相当于输出$,而不是变量）
# 2、$identifier 变量由一个占位符替换(key)，key去匹配变量 "identifier"
# 3、${identifier}相当于 $identifier. 它被用于当占位符后直接跟随一个不属于占位符的字符，列如 "${noun}ification"
# Template中有两个重要的方法：substitute和safe_substitute
# 1、substitute      比较严格，必须每一个占位符都找到对应的变量，不然就会报错，
# 2、safe_substitute 则会把未找到的$XXX直接输出


def sql_init(sqlfile,paras:dict):
    log = gol.get_value("log")
    sqlfile = os.path.join(gol.get_value("path_sql"),'%s' %sqlfile)
    try:
        content = open(sqlfile).read()
        try:
            return Template(content).substitute(paras)
        except Exception as e:
            log.info('SQL文件：%s 初始化解析有误，会影响查询结果，请检查！错误信息：%s' % (sqlfile, e))
            try:
                return Template(content).safe_substitute(paras)
            except Exception as e:
                log.info('SQL文件：%s 初始化解析错误，请检查！' % e)
                return ''
    except Exception as e:
        log.info('SQL文件：%s 读取失败，请检查文件编码！错误信息：%s' %(sqlfile,e))
        return ''

# 文件处理
def timeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d',timeStruct)

#'''获取文件的大小,结果保留两位小数，单位为MB'''
def fileSize(filepath):
    fsize = os.path.getsize(filepath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

# '''获取文件的访问时间'''
def fileAccessTime(filepath):
    return timeStampToTime(os.path.getatime(filepath))

# '''获取文件的创建时间'''
def fileCreateTime(filepath):
    return timeStampToTime(os.path.getctime(filepath))

# '''获取文件的修改时间'''
def fileModifyTime(filepath):
    return timeStampToTime(os.path.getmtime(filepath))

# '''获取文件重命名 按原文件名+文件修改日期'''
def fileRename(filepath):
    path,filename = os.path.split(filepath)
    new_filepath=os.path.join(path,'%s_%s%s' %(os.path.splitext(filename)[0],fileModifyTime(filepath),os.path.splitext(filename)[1]))
    if os.path.exists(new_filepath):
        os.remove(filepath)
    else:
        os.rename(filepath,new_filepath)

# 固定短信
report_sms_content = '''尊敬的客户：您好！
    您的体检报告已经可以取了。请您携带身份证并于收到短信后的第二天下午2点至4点半来领取您的体检报告。
    明州国际保健关心您！'''

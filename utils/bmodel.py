from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from utils.base import str2,zipfile
from datetime import datetime
from collections import OrderedDict
# import os
# from datetime import datetime as cdatetime
# from datetime import date as tdate,time as ttime

# 1、sqlalchemy  支持的字段类型
# 类型名       python中类型           说明
# Integer       int            普通整数，一般是32位
# Float         float          浮点数
# String        str            变长字符串
# Text          str            变长字符串，对较长字符串做了优化
# Boolean       bool            布尔值
# PickleType    任何Python对象   自动使用Pickle序列化

# 2、sqlalchemy  支持的字段限制
# primary_key       表示主键
# unique            表示此列不重复
# index             创建索引，提升查询效率
# nullable          如果为True，允许空值
# default           定义默认值

# 增删改查
# 4 查
# query(*entities, **kwargs)
# query(classname) or query(classname.column1,classname.column2) or query(func.max())

# 4.1 查->过滤器函数
# filter(*criterion)    示例：filter(classname.column=='xxxxxx')   描述：过滤器，使用关键字变量过滤查询结果
# filter_by(**kwargs)   示例：filter_by(column==’xxxxxx’)          描述：过滤器，使用关键字变量过滤查询结果
#
# filter与filter_by都是帮助过滤查询结果的函数，区别：
# 1、filter用classname.column，支持运算符、and、or等作为参数。
# 2、filter_by不必加上classname，不支持运算符、and、or等做参数，因为参数为**kwargs支持组合查询。

# 其他查询操作条件
# or 操作： filter(or_(TJ_TJDJB.somover=='1',TJ_TJDABH.sfzh==xxxxx))
# and 操作：filter(and_(TJ_TJDJB.somover=='1',TJ_TJDABH.sfzh==xxxxx))
# in 操作： filter(TJ_TJDJB.somover.in_(('0','9')))
# not in 操作： filter(~TJ_TJDJB.somover.in_(('0','9')))
# between 操作：filter(TJ_TJDJB.qdrq.between(('2019-01-01','2019-01-02')))
# like 操作：filter(TJ_TJDJB.area.like('明州%'))
# 空值 操作：filter(TJ_TJDJB.del.is_(None))

# 4.2 查->返回结果
# all()                                 描述：返回keyedTuple元组的列表
# first()                               描述：返回查询结果的第一个，如果没有，返回None
# first_or_404()                        描述：返回查询结果的第一个，如果没有，抛出404异常
# one()                                 描述：获取所有行，若查询不到or查询到多个对象or查询到一个对象但重复记录，抛出异常
# scalar()                              描述：在one()的基础上获得该行的第一列
# order_by(classname.column)	        描述：依据某列或某几列对查询结果按字典序排序
# label()                               描述：为某一列起别名
# get()                                 描述：返回主键对应记录，如果没有，返回None
# get_or_404()                          描述：返回主键对应记录，如果没有，抛出404异常
# count()                               描述：返回查询结果数量

# 5、连表查询
# 连表查询有两种方式，一种是通过filter，一种是通过join。

# 5.1 通过 query 与 filter 进行连表查询
# session.query(User, Address).filter(User.id==Address.user_id).filter(Address.city=='Peking')
#
# 5.2 通过join达到同样效果, 只有一个外键
# session.query(User).join(Address).filter(Address.city=='Peking')
#
# # 多个外键或者没有外键时，要给出明确条件
# session.query(User).join(Address，User.id==Address.user_id).filter(Address.city=='Peking')
# session.query(User).join(Address,User.addresses). filter(Address.city=='Peking')

# 6、特殊 用于封装功能
# 获取字段长度 User.name.property.columns[0].type.length

BaseModel = declarative_base()

'''
模型类名：
1）MT_ 表示表     其中 M表示model  T表示table
2）MV_ 表示视图   其中 M表示model  V表示view
'''
# query2dict 思路可参考
# https://www.oschina.net/code/snippet_575790_35170
# https://www.cnblogs.com/wancy86/p/6421792.html
#
# 多个对象
# def dobule_to_dict(self):
#     result = {}
#     for key in self.__mapper__.c.keys():
#         if getattr(self, key) is not None:
#             result[key] = str(getattr(self, key))
#         else:
#             result[key] = getattr(self, key)
#     return result


class MT_TJDJB(BaseModel):

    __tablename__ = 'TJ_TJDJB'

    __table_args__ = (
        Index('_dta_index_TJ_TJDJB_8_852914110__K1_K79', 'TJBH', 'del'),
        Index('IX_CRBSB', 'CRBSB', 'CRBTJ', 'CRBSBYS')
    )

    TJBH = Column(String(16, 'Chinese_PRC_CI_AS'), primary_key=True)
    DABH = Column(String(30, 'Chinese_PRC_CI_AS'), index=True)
    DJR = Column(String(20, 'Chinese_PRC_CI_AS'))
    DJRQ = Column(DateTime, index=True)
    NL = Column(Integer)
    TJLB = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    DWBH = Column(String(30, 'Chinese_PRC_CI_AS'), index=True)
    FZBH = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    FKFS = Column(Numeric(8, 0))
    FKSJ = Column(DateTime)
    YSJE = Column(Numeric(8, 2))
    ZK = Column(Numeric(8, 2))
    YHJE = Column(Numeric(8, 2))
    SJJE = Column(Numeric(8, 2))
    SJHM = Column(String(16, 'Chinese_PRC_CI_AS'))
    JSBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    JSRQ = Column(DateTime)
    ZS = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    JY = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    JSR = Column(String(20, 'Chinese_PRC_CI_AS'))
    DEPART = Column(String(200, 'Chinese_PRC_CI_AS'))
    ZJYS = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZJRQ = Column(DateTime, index=True)
    SUMOVER = Column(CHAR(1, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('0')"))
    GDRQ = Column(DateTime)
    GDYS = Column(String(20, 'Chinese_PRC_CI_AS'))
    YYBH = Column(String(30, 'Chinese_PRC_CI_AS'))
    SFTC = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    TCBH = Column(String(12, 'Chinese_PRC_CI_AS'))
    dybj = Column(String(1, 'Chinese_PRC_CI_AS'))
    jdzs = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    jdjy = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    SFDC = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    TJRQ = Column(DateTime, index=True)
    YXRQ = Column(DateTime)
    DWJSJE = Column(Numeric(10, 2))
    TJLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    PASS = Column(String(20, 'Chinese_PRC_CI_AS'))
    FBBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    HIS_SSJE = Column(Numeric(8, 2))
    HIS_JSBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    YSKH = Column(String(20, 'Chinese_PRC_CI_AS'))
    XRKH = Column(String(20, 'Chinese_PRC_CI_AS'))
    XKZT = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    jslx = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SMS = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    MAIL = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    IO_PACS = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    IO_LIS = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SHYS = Column(String(20, 'Chinese_PRC_CI_AS'))
    SHRQ = Column(DateTime, index=True)
    GL = Column(String(10, 'Chinese_PRC_CI_AS'))
    GZ = Column(String(100, 'Chinese_PRC_CI_AS'))
    DHYS = Column(String(100, 'Chinese_PRC_CI_AS'))
    sffdx = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    FBBZ_YB = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    joyharii_flag = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    HDC_Issue_Flag = Column(CHAR(1, 'Chinese_PRC_CI_AS'), server_default=text("('0')"))
    SHBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    CPAINTER = Column(String(20, 'Chinese_PRC_CI_AS'))
    FZXH = Column(String(20, 'Chinese_PRC_CI_AS'))
    QD = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    BZ = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    MFTJ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    TMDY = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    TMDYRQ = Column(DateTime)
    ZYDDY = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    ZYDDYRQ = Column(DateTime)
    SXXE = Column(Numeric(18, 0))
    TTBH = Column(String(12, 'Chinese_PRC_CI_AS'), index=True)
    JXXE = Column(Numeric(18, 0))
    QDRQ = Column(DateTime, index=True)
    BGRQ = Column(DateTime)
    zc = Column(CHAR(2, 'Chinese_PRC_CI_AS'))
    dwxh = Column(String(30, 'Chinese_PRC_CI_AS'), index=True)
    RYLB = Column(CHAR(2, 'Chinese_PRC_CI_AS'))
    io_bl = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    ywy = Column(String(20, 'Chinese_PRC_CI_AS'))
    _del = Column('del', CHAR(1, 'Chinese_PRC_CI_AS'))
    io_jkcf = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    sms_sendtime = Column(DateTime)
    tjqy = Column(String(2, 'Chinese_PRC_CI_AS'))
    tjqdqy = Column(String(2, 'Chinese_PRC_CI_AS'))
    SFSF = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFJG = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFQD = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFXS = Column(String(2, 'Chinese_PRC_CI_AS'))
    SFZZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    ZKYS = Column(String(20, 'Chinese_PRC_CI_AS'))
    SFDY = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    DYRQ = Column(DateTime)
    HDC_JoyharII_Flag = Column(CHAR(1, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('0')"))
    JHGL = Column(String(10, 'Chinese_PRC_CI_AS'))
    zyb_zjbz = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    zyb_zjys = Column(String(12, 'Chinese_PRC_CI_AS'))
    zyb_zjrq = Column(DateTime)
    FJ_GLBH = Column(String(20, 'Chinese_PRC_CI_AS'))
    FJ_DJRQ = Column(DateTime)
    FJ_DJR = Column(String(20, 'Chinese_PRC_CI_AS'))
    FJBZ = Column(String(1, 'Chinese_PRC_CI_AS'))
    FJNR = Column(String(400, 'Chinese_PRC_CI_AS'))
    FJ_XMBH = Column(String(200, 'Chinese_PRC_CI_AS'))
    FJQK = Column(String(2, 'Chinese_PRC_CI_AS'))
    ZYBLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    FJTZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    zhaogong = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    DWJSDH = Column(String(20, 'Chinese_PRC_CI_AS'))
    DWJSBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    DWJSRQ = Column(DateTime)
    CJ = Column(String(40, 'Chinese_PRC_CI_AS'))
    GH = Column(String(20, 'Chinese_PRC_CI_AS'))
    HKSZD = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZYB_TJBH = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZYB_BH = Column(Integer)
    JKZ_LB = Column(Integer)
    JKZ_GZ = Column(String(4, 'Chinese_PRC_CI_AS'))
    JKZ_ADDR = Column(String(400, 'Chinese_PRC_CI_AS'))
    JKZ_ADDR_CODE = Column(String(9, 'Chinese_PRC_CI_AS'))
    JKZ_WHCD = Column(Integer)
    JKZ_GL = Column(Integer)
    JKZ_DWMC = Column(String(100, 'Chinese_PRC_CI_AS'))
    JKZ_SFHG = Column(Integer)
    JKZ_BH = Column(String(100, 'Chinese_PRC_CI_AS'))
    appdh = Column(String(50, 'Chinese_PRC_CI_AS'))
    jgid = Column(DECIMAL(10, 0))
    out_flag = Column(Numeric(1, 0), server_default=text("(0)"))
    scbz = Column(Numeric(1, 0), server_default=text("(0)"))
    lqbj = Column(Integer)
    lqrq = Column(DateTime)
    QXSHYY = Column(String(200, 'Chinese_PRC_CI_AS'))
    FSYZL = Column(String(100, 'Chinese_PRC_CI_AS'))
    YSZC = Column(Integer)
    ECQDRQ = Column(DateTime)
    BGLQFS = Column(Integer)
    QXSHZJYS = Column(String(50, 'Chinese_PRC_CI_AS'))
    ZGJL_EXCEL = Column(Integer, server_default=text("((0))"))
    TJRYGH = Column(String(10, 'Chinese_PRC_CI_AS'))
    YBSCBZ = Column(Numeric(1, 0))
    TJZT = Column(CHAR(1, 'Chinese_PRC_CI_AS'), index=True, server_default=text("('1')"))
    YZJYS = Column(String(20, 'Chinese_PRC_CI_AS'), index=True)
    YSHYS = Column(String(20, 'Chinese_PRC_CI_AS'), index=True)
    BGCC = Column(Integer, server_default=text("((0))"))
    CRBSB = Column(Integer, server_default=text("((0))"))
    CRBTJ = Column(Integer, server_default=text("((0))"))
    CRBSBYS = Column(String(30, 'Chinese_PRC_CI_AS'))
    XCGCL = Column(Integer)
    FJ_FJBZ = Column(String(200, 'Chinese_PRC_CI_AS'))

class MT_TJDAB(BaseModel):

    __tablename__ = 'TJ_TJDAB'
    __table_args__ = (
        Index('_dta_index_TJ_TJDAB_8_820913996__K1_K5_K4_K3_K2', 'DABH', 'SFZH', 'CSNY', 'XB', 'XM'),
        Index('_dta_index_TJ_TJDAB_8_820913996__K1_K2_K3_K5_K7_K14', 'DABH', 'XM', 'XB', 'SFZH', 'HYZK', 'SJHM')
    )

    DABH = Column(String(30, 'Chinese_PRC_CI_AS'), primary_key=True)
    XM = Column(String(40, 'Chinese_PRC_CI_AS'), nullable=False, index=True)
    XB = Column(Numeric(8, 0))
    CSNY = Column(DateTime)
    SFZH = Column(String(18, 'Chinese_PRC_CI_AS'), index=True)
    WHCD = Column(Numeric(8, 0))
    HYZK = Column(Numeric(8, 0))
    ZY = Column(Numeric(8, 0))
    SH = Column(String(100, 'Chinese_PRC_CI_AS'))
    JG = Column(Numeric(8, 0))
    LXDH = Column(String(32, 'Chinese_PRC_CI_AS'))
    BGDH = Column(String(32, 'Chinese_PRC_CI_AS'))
    ZZDH = Column(String(32, 'Chinese_PRC_CI_AS'))
    SJHM = Column(String(32, 'Chinese_PRC_CI_AS'), index=True)
    ADDR = Column(String(128, 'Chinese_PRC_CI_AS'))
    HTTPADDR = Column(String(100, 'Chinese_PRC_CI_AS'))
    TJLY = Column(Numeric(8, 0))
    LXRM = Column(String(256, 'Chinese_PRC_CI_AS'))
    ZC = Column(Numeric(8, 0))
    ZW = Column(Numeric(8, 0))
    YYBH = Column(String(30, 'Chinese_PRC_CI_AS'))
    PYJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    WBJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    ZDYM = Column(String(50, 'Chinese_PRC_CI_AS'))
    JDR = Column(String(20, 'Chinese_PRC_CI_AS'))
    JDRQ = Column(DateTime, nullable=False, index=True)
    BMGH = Column(String(20, 'Chinese_PRC_CI_AS'))
    DWBH = Column(String(30, 'Chinese_PRC_CI_AS'))
    FZBH = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    GZDW = Column(String(100, 'Chinese_PRC_CI_AS'))
    HISID = Column(Numeric(18, 0))
    MZ = Column(CHAR(8, 'Chinese_PRC_CI_AS'))
    EMPID = Column(String(40, 'Chinese_PRC_CI_AS'))


# 短信模板
class MT_TJ_SMSTemplate2(BaseModel):

    __tablename__ = 'TJ_SMS_Template2'

    TID = Column(Integer, primary_key=True, autoincrement=True)
    # 模板名称
    TNAME = Column(String(30, 'Chinese_PRC_CI_AS'), nullable=False)
    # 模板内容
    CONTENT = Column(Text, nullable=False)
    # 性别
    TXB = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    # 备注
    BZ = Column(String(100, 'Chinese_PRC_CI_AS'),)
    # 有效标记
    YXBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('0')"))
    modify_time = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        tmp = {}
        for col_obj in self.__table__.columns:
            values = self.property_dict(col_obj.name)
            if values:
                tmp[col_obj.name] = values.get(str2(getattr(self, col_obj.name, None)),None)
            else:
                tmp[col_obj.name] = str2(getattr(self, col_obj.name, None))
        return tmp
        # return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

    # 字段字典属性
    def property_dict(self,name):
        if name == 'TXB':
            return OrderedDict([
                ('','所有'),
                ('1','男'),
                ('0','女')
            ])

#用户登录信息表
class MT_TJ_LOGIN(BaseModel):

    __tablename__ = 'TJ_LOGIN'

    lid= Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(VARCHAR(10),nullable=True)
    login_name = Column(VARCHAR(10),nullable=True)
    login_area = Column(VARCHAR(20),nullable=True)
    login_in = Column(DateTime,nullable=True)
    login_out = Column(DateTime, nullable=False)
    login_interval = Column(INTEGER, nullable=False)
    login_ip = Column(VARCHAR(15), nullable=True)
    login_host = Column(VARCHAR(50), nullable=True)

    def to_dict(self):
        return {
            'login_name':getattr(self, "login_name"),
            'login_area': getattr(self, "login_area"),
            'login_in': getattr(self, "login_in"),
            'login_ip': getattr(self, "login_ip"),
            'login_host': getattr(self, "login_host")
        }

#代码字典
class MT_GY_DMZD(BaseModel):

    __tablename__ = 'GY_DMZD'

    dmlb = Column(NUMERIC(4),primary_key=True)
    dmsb = Column(NUMERIC(8), primary_key=True)
    srdm = Column(VARCHAR(10),nullable=False)
    dmmc = Column(VARCHAR(40),nullable=False)

#用户代码表
class MT_TJ_YGDM(BaseModel):

    __tablename__ = 'TJ_YGDM'

    yggh = Column(VARCHAR(20),primary_key=True)
    ygxm = Column(VARCHAR(40),nullable=False)


#自增表
class MT_GY_IDENTITY(BaseModel):

    __tablename__ = 'GY_IDENTITY'

    tname = Column(VARCHAR(30),primary_key=True)
    value = Column(Numeric(18),nullable=True)
    origin_value = Column(INTEGER, nullable=True)
    inc_value = Column(INTEGER, nullable=True)


#用户科室表
class MT_TJ_YGQSKS(BaseModel):

    __tablename__ = 'TJ_YGQSKS'

    # __table_args__ = {"useexisting": True}  表示已建立，可追加

    xh = Column(Integer, primary_key=True)
    yggh = Column(VARCHAR(10),primary_key=True)
    ksbm = Column(VARCHAR(10), primary_key=True)
    xssx = Column(Integer, nullable=False)



# 公共模型
class MT_TJ_TJJLMXB(BaseModel):

    __tablename__ = 'TJ_TJJLMXB'

    tjbh = Column(String(16), primary_key=True)      #体检编号 自动生成
    xmbh = Column(String(12), primary_key=True)      # 体检编号 自动生成
    zhbh = Column(String(12), nullable=False)        # 组合编号
    xmmc = Column(String(60), nullable=True)
    jg = Column(Text, nullable=True)
    xmdw = Column(String(20), nullable=True)
    ckfw = Column(String(100), nullable=True)
    ycbz = Column(CHAR(1), nullable=True)
    ycts = Column(String(20), nullable=True)
    sfzh = Column(CHAR(1), nullable=True)
    xssx = Column(Integer(), nullable=True)
    ksbm = Column(CHAR(6), nullable=True)
    jcrq = Column(DateTime, nullable=True)
    jcys = Column(String(20), nullable=True)
    zhsx = Column(Integer(), nullable=True)
    zd = Column(Text, nullable=True)
    zxpb = Column(CHAR(1), nullable=True)
    jsbz = Column(CHAR(1), nullable=True)
    qzjs = Column(CHAR(1), nullable=True)
    shrq = Column(DateTime, nullable=True)
    shys = Column(String(20), nullable=True)
    tmxh = Column(String(20), nullable=True)
    tmbh1 = Column(String(20), nullable=False)

    @property
    def item_state(self):
        if getattr(self, "qzjs", '') == '1':
            return '已拒检'
        else:
            if getattr(self, "jsbz", '') == '1':
                return '已小结'
            else:
                if getattr(self, "zxpb", '') == '0':
                    return '核实'
                elif getattr(self, "zxpb", '') == '1':
                    return '已回写'
                elif getattr(self, "zxpb", '') == '2':
                    return '已接收'
                elif getattr(self, "zxpb", '') == '3':
                    return '已检查'
                elif getattr(self, "zxpb", '') == '4':
                    return '已抽血'
                elif getattr(self, "zxpb", '') == '5':
                    return '已留样'
                else:
                    return '未知'

    @property
    def item_result(self):
        return {
            'xmmc':str2(getattr(self, "xmmc", '')),
            'xmbh': getattr(self, "xmbh", ''),
            'state': self.item_state,
            'ksbm':getattr(self, "ksbm", ''),
            'btn_dy':'',                                    # 打印
            'btn_jj':'',                                    # 拒检
            'btn_hs':''                                     # 核实
        }

    @property
    def item_result2(self):
        return {
            'xmmc':str2(getattr(self, "xmmc", '')),
            'xmbh': getattr(self, "xmbh", ''),
            'state': self.item_state,
            'btn':''                                     # 状态修改
        }

    @property
    def get_shys(self):
        if getattr(self, "shys", ''):
            return getattr(self, "shys", '')
        else:
            if  getattr(self, "jcys", ''):
                return getattr(self, "jcys", '')
            else:
                return ''

    @property
    def get_shrq(self):
        if getattr(self, "shrq", ''):
            return str(getattr(self, "shrq", ''))[0:19]
        else:
            if getattr(self, "jcrq", ''):
                return str(getattr(self, "jcrq", ''))[0:19]
            else:
                return ''

    @property
    def get_edit_items(self):
        return {
            'xmbh': getattr(self, "xmbh", ''),
            'xmmc': str2(getattr(self, "xmmc", '')),
            'xmjg': str2(getattr(self, "jg", '')),
            'ycbz': str2(getattr(self, "ycbz", '')),
            'ycts': str2(getattr(self, "ycts", '')),
            'ckfw': str2(getattr(self, "ckfw", '')),
            'xmdw': str2(getattr(self, "xmdw", ''))
        }

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

class MT_TJ_CZJLWHB(BaseModel):

    __tablename__ = 'TJ_CZJLWHB'

    czbh = Column(CHAR(4),nullable=False, primary_key=True)
    czdzd = Column(VARCHAR(20),nullable=True)
    JSGS = Column(Float(53), server_default=text("((0))"))
    BZ = Column(String(50, 'Chinese_PRC_CI_AS'))
    YXBJ = Column(Integer, server_default=text("((0))"))
    ZHXGR = Column(String(16, 'Chinese_PRC_CI_AS'))
    ZHXGSJ = Column(DateTime)
    PYJM = Column(String(10, 'Chinese_PRC_CI_AS'))

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

class MT_TJ_PACS_PIC(BaseModel):

    __tablename__ = 'TJ_PACS_PIC'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16),nullable=True)
    ksbm = Column(CHAR(6),nullable=True)
    picpath = Column(String(220),nullable=False)
    picname = Column(String(220),nullable=False)
    zhbh = Column(String(16), nullable=False)
    flag = Column(CHAR(1), nullable=False)
    path = Column(String(220), nullable=False)
    pk = Column(String(30), nullable=False)
    ftp_bz = Column(CHAR(1), nullable=False)

class MT_TJ_DW(BaseModel):

    __tablename__ = 'TJ_DWDMB'

    dwbh = Column(String(30), primary_key=True)
    mc = Column(String(100),nullable=True)
    pyjm = Column(String(50),nullable=True)

    @property
    def to_dict_bh(self):
        return {
            getattr(self, "dwbh", ''):str2(getattr(self, "mc", ''))
        }

    @property
    def to_dict_py(self):
        return {
            getattr(self, "pyjm", ''):str2(getattr(self, "mc", ''))
        }

# 公共模型
class MT_TJ_FILE_ACTIVE(BaseModel):

    __tablename__ = 'TJ_FILE_ACTIVE'

    tjbh = Column(String(16), primary_key=True)      #体检编号 自动生成
    dwbh = Column(CHAR(5), nullable=True)
    ryear = Column(CHAR(4), nullable=True)
    rmonth = Column(CHAR(7), nullable=True)
    rday = Column(CHAR(10), nullable=True)
    localfile = Column(String(250), nullable=True)
    ftpfile = Column(String(100), nullable=False)
    filename = Column(String(20), nullable=False)
    filetypename = Column(String(20), nullable=False)
    filesize = Column(Float, nullable=False)
    filemtime = Column(BIGINT, nullable=False)
    createtime = Column(DateTime, nullable=True)

class MT_TJ_CZJLB(BaseModel):

    __tablename__ = 'TJ_CZJLB'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    jllx = Column(CHAR(4), nullable=True)
    jlmc = Column(VARCHAR(30), nullable=True)
    tjbh = Column(VARCHAR(16), nullable=False)
    mxbh = Column(VARCHAR(20), nullable=True)
    czgh = Column(VARCHAR(20), nullable=True)
    czxm = Column(VARCHAR(20), nullable=True)
    czsj = Column(DateTime, nullable=True, default=datetime.now)
    czqy = Column(VARCHAR(2), nullable=True)
    jlnr = Column(Text, nullable=False)
    bz = Column(Text, nullable=False)
    jjxm = Column(VARCHAR(20), nullable=False)                              # 交接护士
    jjsj = Column(DateTime, nullable=False)                                 # 交接时间
    jsxm = Column(VARCHAR(20), nullable=False)                              # 签收人员
    jssj = Column(DateTime, nullable=False)                                 # 签收时间
    sjfs = Column(VARCHAR(20), nullable=False)                              # 送检人员

    @property
    def is_done(self):
        return {
            'tmzt':True if getattr(self, "jjsj") else False,
            'sgys': str2(getattr(self, "bz")),
            'tjbh': getattr(self, "tjbh"),
            'tmbh': getattr(self, "mxbh"),
            'xmhz': str2(getattr(self, "jlnr"))
        }

    @property
    def to_dict(self):

        return {
            'zt': '√',
            'jllx': str2(getattr(self, "jlmc")),
            'tjbh': getattr(self, "tjbh"),
            'tmbh': getattr(self, "mxbh"),
            'czxm': str2(getattr(self, "czxm")),
            'czqy': str2(getattr(self, "czqy")),
            'czsj': str(getattr(self, "czsj"))[0:19],
            'jlnr': str2(getattr(self, "jlnr")),
            'jjxm': str2(getattr(self, "jjxm")),
            'jjsj': self.jjsj_value,
            'jsxm': str2(getattr(self, "jsxm")),
            'jssj': self.jssj_value,
            'sjfs': str2(getattr(self, "sjfs")),
            'tmxm': str2(getattr(self, "jlnr")),
            'ck':'查看'
        }

    @property
    def jjsj_value(self):
        if getattr(self, "jjsj"):
            return str(getattr(self, "jjsj"))[0:19]
        else:
            return ''

    @property
    def jssj_value(self):
        if getattr(self, "jssj"):
            return str(getattr(self, "jssj"))[0:19]
        else:
            return ''

    @property
    def detail(self):
        return {
            'tjbh': getattr(self, "tjbh"),
            'mxbh': getattr(self, "mxbh"),
            'czxm': str2(getattr(self, "czxm")),
            'czqy': str2(getattr(self, "czqy")),
            'czsj': str(getattr(self, "czsj"))[0:23],
            'jlnr': str2(getattr(self, "jlnr"))
        }

# 设备表
class MT_TJ_EQUIP(BaseModel):

    __tablename__ = 'TJ_EQUIP'

    tjbh = Column(String(16), primary_key=True)  #体检编号
    equip_type = Column(CHAR(1), primary_key=True)  # 设备类型
    equip_name = Column(String(16), nullable=True)
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)
    patient = Column(String(20), nullable=False)
    file_path = Column(String(50), nullable=False)
    operator = Column(String(20), nullable=False)
    operate_time = Column(DateTime, nullable=False)
    equip_jg1 = Column(String(250), nullable=False)
    equip_jg2 = Column(String(50), nullable=False)
    xmbh = Column(String(12), nullable=False)
    hostname = Column(String(50), nullable=False)
    hostip = Column(String(25), nullable=False)
    operator2 = Column(String(20), nullable=False)
    operate_area = Column(String(50), nullable=False)

    @property
    def to_dict(self):
        return {
            'tjbh': getattr(self, "tjbh"),
            'patient': str2(getattr(self, "patient")),
            'ename': str2(getattr(self, "equip_name")),
            'jcrq': str(getattr(self, "operate_time"))[0:19],
            'jcys': str2(getattr(self, "operator2")),
            'jcqy': str2(getattr(self, "operate_area")),
            'fpath':self.fpath
        }

    @property
    def fpath(self):
        if getattr(self, "file_path"):
            return getattr(self, "file_path").replace(r'D:/activefile','')
        else:
            return ''



# 心电图
class MT_DCP_files(BaseModel):

    __tablename__ = 'DCP_files'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    cusn = Column(String(32), nullable=False)                       #体检编号
    department = Column(String(16), nullable=False)
    filename = Column(String(128), nullable=False)
    filecontent = Column(BLOB, nullable=False)
    uploadtime = Column(DateTime, nullable=False)
    flag = Column(CHAR(1), nullable=True)

class MV_RYXX(BaseModel):

    __tablename__ = 'V_RYXX'

    tjbh = Column(VARCHAR(20), primary_key=True)
    tjlx = Column(VARCHAR(10), nullable=False)
    tjqy = Column(VARCHAR(10), nullable=False)
    xm = Column(VARCHAR(20),nullable=False)
    xb = Column(VARCHAR(20),nullable=False)
    nl = Column(Integer, nullable=False)
    sjhm = Column(VARCHAR(20), nullable=False)
    sfzh = Column(VARCHAR(20), nullable=False)
    depart = Column(VARCHAR(50), nullable=False)
    dwmc = Column(VARCHAR(100), nullable=False)
    djrq = Column(VARCHAR(20), nullable=False)
    djgh = Column(VARCHAR(20), nullable=False)
    djxm = Column(VARCHAR(20), nullable=False)
    qdrq = Column(VARCHAR(20), nullable=False)
    zjrq = Column(String(20), nullable=False)
    shrq = Column(String(20), nullable=False)
    zjxm = Column(String(20), nullable=False)
    shxm = Column(String(20), nullable=False)
    yzjxm = Column(String(20), nullable=False)
    yshxm = Column(String(20), nullable=False)
    zjys = Column(String(20), nullable=False)
    shys = Column(String(20), nullable=False)
    yzjys = Column(String(20), nullable=False)
    yshys = Column(String(20), nullable=False)
    sygh = Column(String(20), nullable=False)
    io_jkcf = Column(CHAR(1), nullable=False)
    bz = Column(Text, nullable=False)
    tjzt = Column(String(10), nullable=False)

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh"),
            'xm': str2(getattr(self, "xm")),
            'xb': str2(getattr(self, "xb")),
            'nl': '%s 岁' %str(getattr(self, "nl")),
            'sfzh': getattr(self, "sfzh"),
            'sjhm': getattr(self, "sjhm"),
            'depart': str2(getattr(self, "depart")),
            'dwmc': str2(getattr(self, "dwmc")),
            'djrq': getattr(self, "djrq"),
            'qdrq': getattr(self, "qdrq"),
            'zjrq': str2(getattr(self, "zjrq"))[0:10],
            'shrq': str2(getattr(self, "shrq"))[0:10],
            'zjys': str2(getattr(self, "zjxm")),
            'shys': str2(getattr(self, "shxm")),
            'yzjys': str2(getattr(self, "yzjxm")),
            'yshys': str2(getattr(self, "yshxm")),
            'tjzt': getattr(self, "tjzt")
        }

    @property
    def get_bgjl(self):
        return {
            'tjbh':getattr(self, "tjbh"),
            'bgzt': '1',
            'djrq': getattr(self, "djrq"),
            'djgh': getattr(self, "djgh"),
            'djxm': str2(getattr(self, "djxm")),
            'qdrq': getattr(self, "qdrq"),
            'zjrq': getattr(self, "zjrq"),
            'zjgh': getattr(self, "zjys"),
            'zjxm': str2(getattr(self, "zjxm")),
            'shrq': getattr(self, "shrq"),
            'shgh': getattr(self, "shrq"),
            'shxm': str2(getattr(self, "shys"))
        }

    @property
    def pdf_dict(self):
        sjhm = getattr(self, "sjhm", '')
        if not sjhm:
            sjhm ='&nbsp;'
        else:
            sjhm = sjhm
            # if len(sjhm)>=11:
            #     sjhm =  sjhm[0:3]+'-'+sjhm[3:7]+'-'+sjhm[-4:]
            # else:
            #     sjhm = sjhm
        return {
                "tjbh": getattr(self, "tjbh", ''),
                "xm": str2(getattr(self, "xm", '')),
                "xb": str2(getattr(self, "xb", '')),
                "nl": '%s 岁' %str(getattr(self, "nl", '')),
                "xmdw": str2(getattr(self, "xmdw", '')),
                "sfzh": getattr(self, "sfzh", ''),
                "sjhm": sjhm,
                "depart": str2(getattr(self, "depart", '')),
                "dwmc": self.get_dwmc,
                "qdrq": str(getattr(self, "qdrq", ''))[0:10],
                "djrq": str(getattr(self, "djrq", '')),
                'zjys': getattr(self, "zjys"),
                'shys': getattr(self, "shys"),
                'syys': getattr(self, "sygh")
                }

    @property
    def get_dwmc(self):
        if str2(getattr(self, "bz")):
            return str2(getattr(self, "bz"))
        else:
            if str2(getattr(self, "depart")):
                return "%s(%s)" %(str2(getattr(self, "dwmc", '')),str2(getattr(self, "depart")))
            else:
                return str2(getattr(self, "dwmc", ''))

class MT_TJ_PHOTO(BaseModel):

    __tablename__ = 'TJ_PHOTO'

    tjbh = Column(VARCHAR(16), primary_key=True)
    picture = Column(BLOB, nullable=False)


class MT_TJ_KSDM(BaseModel):

    __tablename__ = 'TJ_KSDM'

    ksbm = Column(CHAR(6), primary_key=True)
    ksmc = Column(VARCHAR(40), nullable=False)

class MT_TJ_XMDM(BaseModel):

    __tablename__ = 'TJ_XMDM'

    xmbh = Column(String(12, 'Chinese_PRC_CI_AS'), primary_key=True)
    xmmc = Column(String(60, 'Chinese_PRC_CI_AS'))
    xmdw = Column(String(20, 'Chinese_PRC_CI_AS'))
    XSSX = Column(Integer)
    XB = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    DJ = Column(Numeric(8, 2))
    SZLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    MRJG = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    CKLB = Column(String(10, 'Chinese_PRC_CI_AS'))
    CKSX = Column(Float(53))
    CKXX = Column(Float(53))
    CKZF = Column(String(20, 'Chinese_PRC_CI_AS'))
    PGTS = Column(String(20, 'Chinese_PRC_CI_AS'))
    PDTS = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZXZ = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZDZ = Column(String(20, 'Chinese_PRC_CI_AS'))
    SFTX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    TXMC = Column(String(256, 'Chinese_PRC_CI_AS'))
    LBBM = Column(CHAR(6, 'Chinese_PRC_CI_AS'), index=True)
    PYJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    WBJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    ZDYM = Column(String(50, 'Chinese_PRC_CI_AS'))
    sfzh = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    FLAG = Column(CHAR(1, 'Chinese_PRC_CI_AS'), server_default=text("('0')"))
    BZ = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZHXGR = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZHXGRQ = Column(DateTime)
    LISBH = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZYDH = Column(String(3, 'Chinese_PRC_CI_AS'))
    TSZY = Column(String(200, 'Chinese_PRC_CI_AS'))
    ZYSX = Column(Numeric(4, 0))
    XSHS = Column(Integer, server_default=text("((1))"))
    BJXH = Column(Numeric(8, 0))
    ZDXJ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    HISBH = Column(CHAR(100, 'Chinese_PRC_CI_AS'))
    XMLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    CDCDM = Column(String(50, 'Chinese_PRC_CI_AS'))
    CDCBZ = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SCJCJG = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFCF = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    xstp = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    sycd = Column(String(2, 'Chinese_PRC_CI_AS'))
    Alias = Column(String(20, 'Chinese_PRC_CI_AS'))
    IsMicrobe = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    SFSF = Column(CHAR(1, 'Chinese_PRC_CI_AS'), server_default=text("('0')"))
    XMBH_DZ = Column(String(10, 'Chinese_PRC_CI_AS'))
    ZY_FLAG = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    ZYTS3 = Column(String(100, 'Chinese_PRC_CI_AS'))
    PACSMC = Column(String(50, 'Chinese_PRC_CI_AS'))
    PACSBWBH = Column(String(50, 'Chinese_PRC_CI_AS'))
    PACSBWMC = Column(String(100, 'Chinese_PRC_CI_AS'))
    PACSJCLX = Column(String(20, 'Chinese_PRC_CI_AS'))
    NEWLISBH = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZYTS4 = Column(String(100, 'Chinese_PRC_CI_AS'))
    LCYY = Column(String(500, 'Chinese_PRC_CI_AS'))
    ZYTS5 = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZYTS6 = Column(String(100, 'Chinese_PRC_CI_AS'))
    ZYTS7 = Column(String(100, 'Chinese_PRC_CI_AS'))
    hisdxxh = Column(Numeric(5, 0))
    ZNPD_FLAG = Column(Numeric(1, 0), server_default=text("((0))"))
    BDX = Column(Numeric(5, 0))
    TYPE = Column(String(10, 'Chinese_PRC_CI_AS'))
    XMXE = Column(Integer, server_default=text("((10000))"))
    EDHS = Column(Integer, server_default=text("((1))"))
    XMLB = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    WXLBBM = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    BGCJZQ = Column(Integer, server_default=text("((1))"))
    YSTCBL = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    ZDXJBJ = Column(Integer)
    SFJC = Column(CHAR(1, 'Chinese_PRC_CI_AS'), server_default=text("('1')"))
    BBLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    JSRTCBL = Column(CHAR(6, 'Chinese_PRC_CI_AS'))
    CYFCX = Column(Integer, server_default=text("((0))"))
    JPSL = Column(Integer)

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}


def get_item_state_sql(tjbh):
    return '''
            SELECT 
                (CASE 
                    WHEN qzjs ='1' THEN '已拒检'
                    WHEN jsbz ='1' THEN '已小结'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='0' THEN '核实'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='1' THEN '已回写'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='2' THEN '已登记'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='3' THEN '已检查'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='4' THEN '已抽血'
                    WHEN qzjs IS NULL AND jsbz <>'1' AND ZXPB='5' THEN '已留样'
                    ELSE '未定义' END
                ) AS STATE,
                XMBH,
                XMMC,
                (SELECT KSMC FROM TJ_KSDM WHERE KSBM=TJ_TJJLMXB.KSBM) AS KSMC,
                substring(convert(char,JCRQ,120),1,10) AS JCRQ,
                (SELECT YGXM FROM TJ_YGDM WHERE YGGH=TJ_TJJLMXB.JCYS) AS JCYS,
                substring(convert(char,shrq,120),1,10) AS SHRQ,
                (SELECT YGXM FROM TJ_YGDM WHERE YGGH=TJ_TJJLMXB.shys) AS SHYS,
                TMBH1,(CASE WHEN KSBM IN ('0020','0024') THEN 1 ELSE 0 END ) AS btn_name
            FROM TJ_TJJLMXB 
                WHERE TJBH='%s' AND SFZH='1' 
                AND XMBH NOT IN (SELECT XMBH FROM TJ_KSKZXM  WHERE KSBM='0028')
            ORDER BY qzjs DESC,jsbz,ZXPB DESC,KSBM,ZHBH,XSSX;
    ''' % tjbh
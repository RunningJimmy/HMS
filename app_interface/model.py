from utils.bmodel import *

# 工作总结
class MT_TJ_WorkSummary(BaseModel):

    __tablename__ = 'TJ_WorkSummary'

    WID = Column(Integer, primary_key=True, autoincrement=True)
    editime = Column(DateTime, nullable=False)
    editor = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)               # 编辑人
    state = Column(CHAR(1), nullable=False, server_default=text("('0')"))          # 总结状态
    xjqk = Column(TEXT, nullable=True)          # 巡检情况
    jyfs = Column(TEXT, nullable=True)          # 举一反三
    bzzj = Column(TEXT, nullable=True)          # 本周总结
    xzjh = Column(TEXT, nullable=True)          # 下周计划
    zsk = Column(TEXT, nullable=True)           # 知识库维护
    jsqk = Column(TEXT, nullable=True)          # 晋升情况
    score = Column(Integer, nullable=True)      # 评分
    sjpy = Column(TEXT, nullable=True)          # 上级评语
    sjxm = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)          # 上级姓名
    pysj = Column(DateTime, nullable=False)     # 上级评语

    def to_dict(self):
        tmp = {}
        for col_obj in self.__table__.columns:
            if col_obj.name == 'state':
                tmp[col_obj.name] = {'0':'提交','1':'审阅'}.get(getattr(self, col_obj.name, '0'),'提交')
            elif col_obj.name == 'score':
                if not getattr(self, col_obj.name, 0):
                    tmp[col_obj.name] = '0'
                else:
                    tmp[col_obj.name] = str(getattr(self, col_obj.name, None))
            else:
                tmp[col_obj.name] = str2(getattr(self, col_obj.name, None))

        return tmp
        # return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

# 值班问题记录
class MT_TJ_OverTime(BaseModel):

    __tablename__ = 'TJ_OverTime'

    OID = Column(Integer, primary_key=True, autoincrement=True)
    ODate = Column(Date, nullable=False)
    recorder = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)
    content = Column(TEXT, nullable=False)
    sftx = Column(CHAR(1), nullable=False, server_default=text("('0')"))
    wtgz = Column(CHAR(1), nullable=False, server_default=text("('0')"))

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

# 供应商
class MT_TJ_Supplier(BaseModel):

    __tablename__ = 'TJ_Supplier'

    SID = Column(Integer, primary_key=True, autoincrement=True)
    Ename = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=False)
    Product = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=False)
    Contactor = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=True)
    ContactWay = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=True)
    BZ = Column(TEXT, nullable=True)
    Doc = Column(BLOB, nullable=True)

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}


# 固定资产
class MT_TJ_ASSET(BaseModel):

    __tablename__ = 'TJ_ASSET'

    aid = Column(Integer, primary_key=True, autoincrement=True)
    ename = Column(VARCHAR(30), nullable=False)
    etype = Column(VARCHAR(20), nullable=False)
    earea= Column(VARCHAR(20), nullable=False)
    use_date = Column(Date, nullable=True)
    use_id = Column(VARCHAR(30), nullable=True)
    use_place = Column(VARCHAR(30), nullable=True)
    eip = Column(VARCHAR(15), nullable=True)
    ehost = Column(VARCHAR(30), nullable=True)
    eport = Column(VARCHAR(10), nullable=True)
    bz = Column(VARCHAR(200), nullable=True)
    sfbf = Column(CHAR(1), nullable=False, server_default=text("('0')"))

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

    # def to_dict(self):
    #     return {
    #             'aid': str(getattr(self, "aid")),
    #             "ename": str2(getattr(self, "ename", '')),
    #             "etype": str2(getattr(self, "etype", '')),
    #             "earea": str2(getattr(self, "earea", '')),
    #             "use_date": str(getattr(self, "use_date", '')),
    #             "use_id": str(getattr(self, "use_id", '')),
    #             "use_place": str2(getattr(self, "use_place", '')),
    #             "eip": str(getattr(self, "eip", '')),
    #             "ehost": str2(getattr(self, "ehost", '')),
    #             "eport": str2(getattr(self, "eport", '')),
    #             "bz": str2(getattr(self, "bz", '')),
    #             "sfbf": getattr(self, "sfbf", '')
    #     }


# 需求管理
class MT_TJ_XQGL(BaseModel):

    __tablename__ = 'TJ_XQGL'

    vstate = {
        None:'已作废',
        '0': '待提交',
        '1': '已提交',
        '2': '已审核' ,
        '3': '已开发' ,
        '4': '已跟踪',
        '5': '已验收'
    }

    DID = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(CHAR(1), nullable=False)              # 需求状态
    dname = Column(VARCHAR(50), nullable=True)          # 需求名称
    submiter = Column(VARCHAR(10), nullable=True)       # 提交人
    submitime = Column(DateTime, nullable=True)         # 提交时间
    expect_date = Column(VARCHAR(10), nullable=True)    # 期望日期
    question = Column(TEXT, nullable=True)              # 问题描述
    demand = Column(TEXT, nullable=True)                # 需求描述
    system = Column(VARCHAR(20), nullable=False)        # 系统名称
    module = Column(VARCHAR(20), nullable=False)        # 模块名称
    level = Column(VARCHAR(20), nullable=False)         # 紧急程度
    dtype = Column(VARCHAR(20), nullable=False)         # 需求类型
    shxm = Column(VARCHAR(10), nullable=False)          # 审核姓名
    shsj = Column(DateTime, nullable=False)             # 审核时间
    shnr = Column(TEXT, nullable=False)                 # 需求评估内容，收益价值
    spxm = Column(VARCHAR(10), nullable=False)          # 审批姓名
    spsj = Column(DateTime, nullable=False)             # 审批时间
    kfxm = Column(VARCHAR(10), nullable=False)          # 开发姓名
    kfsj = Column(DateTime, nullable=False)             # 开发时间
    jjfa = Column(TEXT, nullable=False)                 # 解决方案
    gzxm = Column(VARCHAR(10), nullable=False)          # 跟踪姓名
    gzsj = Column(DateTime, nullable=False)             # 跟踪时间
    syqk = Column(TEXT, nullable=False)                 # 使用情况
    ysxm = Column(VARCHAR(10), nullable=False)          # 验收姓名
    yssj = Column(DateTime, nullable=False)             # 验收时间
    yspj = Column(TEXT, nullable=False)
    zfxm = Column(VARCHAR(10), nullable=False)          # 作废姓名
    zfsj = Column(DateTime, nullable=False)             # 作废时间
    zfyy = Column(TEXT, nullable=False)                 # 作废原因
    zdy_pj1 = Column(Integer, nullable=False)           # 自定义评价1
    zdy_pj2 = Column(Integer, nullable=False)           # 自定义评价2
    zdy_pj3 = Column(Integer, nullable=False)           # 自定义评价3
    zdy_pj4 = Column(Integer, nullable=False)           # 自定义评价4
    zdy_pj5 = Column(Integer, nullable=False)           # 自定义评价5
    zdy_pj6 = Column(Integer, nullable=False)           # 自定义评价6

    @property
    def to_dict(self):
        tmp = {}
        for col_obj in self.__table__.columns:
            if col_obj.name == 'state':
                tmp[col_obj.name] = self.vstate.get(getattr(self, col_obj.name))
            elif col_obj.type==INTEGER:
                tmp[col_obj.name] = str(getattr(self, col_obj.name))
            elif col_obj.type==DATETIME:
                tmp[col_obj.name] = str(getattr(self, col_obj.name))[0:19]
            else:
                tmp[col_obj.name] = str2(getattr(self, col_obj.name))

        return tmp
        # return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}

# 电话记录 实际应该同步 TJ_CZJLB 此表为过渡
class MT_TJ_DHGTJLB(BaseModel):

    __tablename__ = 'TJ_DHGTJLB'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16), nullable=False)       # 体检编号
    jllx = Column(Integer, nullable=True)           # 记录类型
    jlnr = Column(DateTime, nullable=True)          # 记录内容
    jlr = Column(String(16), nullable=False)        # 记录人
    jlsj = Column(String(16), nullable=False)       # 记录时间

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh", ''),
            'jllx': self.jllx_v,
            'jlsj': str(getattr(self, "jlsj", ''))[0:19],
            'jlr':str2(getattr(self, "jlr", '')),
            'jlnr': str2(getattr(self, "jlnr", ''))
        }


    @property
    def jllx_v(self):
        if getattr(self, "jllx", '')== '1':
            return '项目追踪'
        elif getattr(self, "jllx", '')== '2':
            return '阳性沟通'
        elif getattr(self, "jllx", '')== '3':
            return '检后回访'
        elif getattr(self, "jllx", '')== '4':
            return '慢病回访'
        else:
            return ''

class MV_RIS2HIS_ALL(BaseModel):

    __tablename__ = 'V_RIS2HIS_ALL'

    CBLKH = Column(VARCHAR(20), primary_key=True)        # 体检编号
    CNAME = Column(VARCHAR(20),nullable=False)
    CSEX = Column(VARCHAR(20),nullable=False)
    CAGE = Column(Integer, nullable=False)
    CBGZT = Column(VARCHAR(20), nullable=False)         # 报告状态
    CJCZT = Column(VARCHAR(20), nullable=False)         # 检查状态
    CBZ = Column(VARCHAR(50), nullable=False)

class MT_TJ_SMS_POST(BaseModel):

    __tablename__ = 'TJ_SMS_POST'

    tjbh = Column(String(16), primary_key=True)       # 体检编号
    sendtime = Column(DateTime, nullable=False)       # 发送时间
    context = Column(Text, nullable=False)            # 短信内容
    state = Column(String(20), nullable=False)        # 状态
    sender = Column(String(20), nullable=False)       # 发送者
    xm = Column(String(20), nullable=False)           # 姓名
    sjhm = Column(String(20), nullable=False)         # 手机号码
    xb = Column(String(20), nullable=False)           # 性别

    @property
    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh", ''),
            'sendtime': str(getattr(self, "sendtime", ''))[0:19],
            'context':str2(getattr(self, "context", ''))
        }


def get_inspect_result_sql():
    return '''
     SELECT 
        SYSTYPE,CMODALITY,CBZ AS XMMC,CACCNO,CBLKH,CNAME,CSEX,CAGE,
        CBGZT,RIS_BG_CSHYSXM AS SHYS,RIS_BG_DSHSJ AS SHSJ,
        RIS_BG_DBGSJ AS BGSJ,RIS_BG_CBGYSXM AS BGYS,CJCZT,
        DCHECKDATE,DDJSJ,IID,IJCH,RIS_BG_CBGSJ_HL7 AS XMJG,RIS_BG_CBGZD AS XMZD,
        RIS_BG_CBGYS,RIS_BG_CSHYS,HISORDER_IID,CBRLX,CROOM
     FROM V_RIS2HIS_ALL WHERE CBLKH = '%s'
    '''

class MV_ReportMicroView(BaseModel):

    __tablename__ = 'ReportMicroView'

    PatNo = Column(String(16), primary_key=True)        # 体检编号
    ItemNo = Column(String(20), primary_key=True)       # 条码号
    ReceiveDate = Column(String(10), primary_key=True)  # 项目编号
    SectionNo = Column(String(10), nullable=False)      # 项目名称
    Technician = Column(String(16), nullable=False)  # 项目结果
    gdbj = Column(String(10), nullable=False)  # 项目标识
    ckfw = Column(String(50), nullable=False)  # 项目参考范围

# VI_TJ_RESULT 检验结果表
class MV_VI_TJ_RESULT(BaseModel):

    __tablename__ = 'VI_TJ_RESULT'

    tjbh = Column(String(16), primary_key=True)         # 体检编号
    tmh = Column(String(20), primary_key=True)          # 条码号
    xmxh = Column(String(10), primary_key=True)         # 项目编号
    xmmc = Column(String(50), nullable=False)           # 项目名称
    xmjg = Column(String(250), nullable=False)          # 项目结果
    gdbj = Column(String(10), nullable=False)           # 项目标识
    ckfw = Column(String(50), nullable=False)           # 项目参考范围
    xmdw = Column(String(50), nullable=False)           # 项目单位
    jyys = Column(String(16), nullable=False)           # 检验医生
    jyrq = Column(DateTime, nullable=False)             # 检验日期
    shys = Column(String(16), nullable=False)           # 审核医生
    bgrq = Column(DateTime, nullable=False)             # 审核日期

    @property
    def to_dict(self):
        return {
            'tjbh': getattr(self, "tjbh", ''),
            'xmbh': getattr(self, "xmxh", ''),
            'xmjg': str2(getattr(self, "xmjg", '')),
            'ycts': str2(getattr(self, "gdbj", '')),
            'ckfw': str2(getattr(self, "ckfw", '')),
            'xmdw': str2(getattr(self, "xmdw", '')),
            'jcys': getattr(self, "jyys", ''),
            'jcrq': getattr(self, "jyrq", ''),
            'shys': getattr(self, "shys", ''),
            'shrq': getattr(self, "bgrq", '')
        }

# LIS项目对照表
def get_lis_match_pes_sql():
    return '''
      SELECT 
		TJ_XMDM.NEWLISBH, 
		TJ_XMDM.XMBH   
       FROM TJ_XMDM,   
             TJ_XMLB  
       WHERE ( TJ_XMDM.LBBM = TJ_XMLB.LBBM ) AND  
                NEWLISBH IS NOT NULL AND
             ( ( TJ_XMLB.XMLX = '2' ) and (flag =0 ) ) 
    '''


def get_equip_sql(tjbh):
    return '''
    SELECT 
        a.TJBH,
        (CASE 
            WHEN a.qzjs='1' THEN '已拒检'
            WHEN (a.qzjs<>'1' OR a.qzjs IS NULL) AND a.jsbz='1' THEN '已小结'
            WHEN (a.qzjs<>'1' OR a.qzjs IS NULL) AND a.jsbz<>'1' AND a.zxpb='3'  THEN '已检查'
            ELSE '核实' END
        ) AS XMZT,
        b.EQUIP_NAME AS EQUIP,
        (CASE 
            WHEN b.OPERATE_TIME IS NOT NULL THEN b.OPERATE_TIME
            ELSE a.JCRQ  END 
        ) AS JCRQ,
        (CASE 
            WHEN b.OPERATOR2 IS NOT NULL THEN b.OPERATOR2
            ELSE (SELECT YGXM FROM TJ_YGDM where yggh=a.JCYS ) END 
        ) AS JCYS,
        (CASE 
            WHEN a.ZHBH IN ('0806','501576') THEN JCRQ 
            ELSE '' END
        ) AS SHRQ,
        (CASE 
            WHEN a.ZHBH IN ('0806','501576') THEN (SELECT YGXM FROM TJ_YGDM where yggh=a.JCYS ) 
            ELSE '' END
        ) AS SHYS,
        ( CASE
            WHEN a.zhbh ='501576' THEN a.JG
          WHEN a.zhbh ='0310' THEN b.EQUIP_JG1
          ELSE '' END
        ) AS XMJG,
        ( CASE
            WHEN a.zhbh ='501576' THEN a.ZD
          WHEN a.zhbh ='0310' THEN b.EQUIP_JG2
            WHEN a.zhbh ='0806' THEN a.JG
          ELSE '' END
        ) AS XMZD,
        b.FILE_PATH AS FILENAME
         
    FROM 
    
    (SELECT * FROM TJ_TJJLMXB WHERE TJBH ='%s' AND ZHBH IN ('0806','5402','501576','1000074','0310') AND SFZH='0') AS a
    
    INNER JOIN (SELECT * FROM TJ_EQUIP WHERE TJBH ='%s' ) AS b
    
    ON a.TJBH=b.TJBH AND a.ZHBH=b.XMBH
    
    ''' %(tjbh,tjbh)


from utils.bmodel import *

class MT_TJ_XQGL(BaseModel):

    __tablename__ = 'TJ_XQGL'

    vstate = {
        '0':'已提交',
        '1':'已审核',
        '2':'已审批' ,
        '3':'开发中' ,
        '4':'已验收'
    }

    DID = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(CHAR(1), nullable=True)          # 需求状态
    dname = Column(VARCHAR(50), nullable=True)      # 需求名称
    submiter = Column(VARCHAR(10), nullable=True)      #
    submit_time = Column(DateTime, nullable=True)
    expect_date = Column(VARCHAR(10), nullable=True)
    question = Column(TEXT, nullable=True)
    demand = Column(TEXT, nullable=True)
    system = Column(VARCHAR(20), nullable=False)
    module = Column(VARCHAR(20), nullable=False)
    level = Column(VARCHAR(20), nullable=False)
    shxm = Column(VARCHAR(10), nullable=False)
    shsj = Column(DateTime, nullable=False)
    spxm = Column(VARCHAR(10), nullable=False)
    spsj = Column(DateTime, nullable=False)
    kfxm = Column(VARCHAR(10), nullable=False)
    kfsj = Column(DateTime, nullable=False)
    jjfa = Column(VARCHAR(200), nullable=False)
    gzxm = Column(VARCHAR(10), nullable=False)
    gzsj = Column(DateTime, nullable=False)
    ysxm = Column(VARCHAR(10), nullable=False)
    yssj = Column(DateTime, nullable=False)
    yspj = Column(TEXT, nullable=False)

    @property
    def to_dict(self):
        return {
            'did': str(getattr(self, "DID")),
            "state":self.vstate[getattr(self, "state", '0')],
            'dname': str2(getattr(self, "dname", '')),
            'submiter': str2(getattr(self, "submiter", '')),
            'submit_time': str2(getattr(self, "submit_time", ''))[0:19],
            'system': str2(getattr(self, "system", '')),
            'module': str2(getattr(self, "module", '')),
            'level': str2(getattr(self, "level", '')),
            'shxm': str2(getattr(self, "shxm", '')),
            'shsj': str2(getattr(self, "shsj", ''))[0:19],
            'spxm': str2(getattr(self, "shxm", '')),
            'spsj': str2(getattr(self, "shsj", ''))[0:19],
            'kfxm': str2(getattr(self, "shxm", '')),
            'kfsj': str2(getattr(self, "shsj", ''))[0:19],
            'gzxm': str2(getattr(self, "shxm", '')),
            'gzsj': str2(getattr(self, "shsj", ''))[0:19],
            'ysxm': str2(getattr(self, "shxm", '')),
            'yssj': str2(getattr(self, "shsj", ''))[0:19]
        }

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


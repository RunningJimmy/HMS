from utils.bmodel import *

# 报告查看禁止
class MT_TJ_Forbidden(BaseModel):

    __tablename__ = 'TJ_Forbidden'

    fid = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16),nullable=True,unique=True)
    operator = Column(String(16),nullable=True)
    operatime = Column(DateTime,nullable=True)

# 慢病记录表 宽表
class MT_MB_YSKH(BaseModel):

    __tablename__ = 'MB_YSKH'

    mbid = Column(Integer, primary_key=True, autoincrement=True)
    tjbh = Column(String(16),nullable=True,unique=True)
    xm = Column(String(10),nullable=True)
    xb = Column(String(5),nullable=False)
    nl = Column(Integer, nullable=False)
    sjhm = Column(String(20),nullable=False)
    sfzh = Column(String(20), nullable=False)
    addr = Column(String(100),nullable=False)
    dwbh = Column(String(5), nullable=False)
    dwmc = Column(String(200), nullable=False)
    ysje = Column(FLOAT, nullable=False)
    djrq = Column(String(10), nullable=False)
    qdrq = Column(String(10), nullable=False)
    tjrq = Column(String(10), nullable=False)
    zjrq = Column(String(10), nullable=False)
    shrq = Column(String(10), nullable=False)
    zjys = Column(String(10), nullable=False)
    shys = Column(String(10), nullable=False)
    is_gxy = Column(CHAR(1), nullable=True,default='0')
    is_gxz = Column(CHAR(1), nullable=True,default='0')
    is_gns = Column(CHAR(1), nullable=True,default='0')
    is_gxt = Column(CHAR(1), nullable=True,default='0')
    is_jzx = Column(CHAR(1), nullable=True,default='0')
    glu = Column(FLOAT, nullable=False)         # 血糖
    is_yc_glu = Column(CHAR(1), nullable=True, default='0')
    glu2 = Column(FLOAT, nullable=False)        # 二小时血糖
    is_yc_glu2 = Column(CHAR(1), nullable=True, default='0')
    hbalc = Column(FLOAT, nullable=False)       # 糖化血红蛋白
    is_yc_hbalc = Column(CHAR(1), nullable=True, default='0')
    ua = Column(FLOAT, nullable=False)          # 尿酸
    is_yc_ua = Column(CHAR(1), nullable=True, default='0')
    tch = Column(FLOAT, nullable=False)         # 总胆固醇
    is_yc_tch = Column(CHAR(1), nullable=True, default='0')
    tg = Column(FLOAT, nullable=False)          # 甘油三酯
    is_yc_tg = Column(CHAR(1), nullable=True, default='0')
    hdl = Column(FLOAT, nullable=False)         # 高密度脂蛋白
    is_yc_hdl = Column(CHAR(1), nullable=True, default='0')
    ldl = Column(FLOAT, nullable=False)         # 低密度脂蛋白
    is_yc_ldl = Column(CHAR(1), nullable=True, default='0')
    hbp = Column(FLOAT, nullable=False)         # 高血压
    is_yc_hbp = Column(CHAR(1), nullable=True, default='0')
    lbp = Column(FLOAT, nullable=False)         # 低血压
    is_yc_lbp = Column(CHAR(1), nullable=True, default='0')
    jzxcs = Column(Text, nullable=False)        # 甲状腺彩超
    is_hf = Column(CHAR(1), nullable=True, default='0') # 是否回访

    @property
    def to_dict(self):
        return {
            "tjbh": getattr(self, "tjbh", ''),
            "xm": getattr(self, "xm", ''),
            "xb": getattr(self, "xb", ''),
            "nl": '%s 岁' % str(getattr(self, "nl", '')),
            "sfzh": getattr(self, "sfzh", ''),
            "sjhm": getattr(self, "sjhm", ''),
            "dwmc": getattr(self, "dwmc", ''),
            "ysje": str(getattr(self, "ysje", '')),
            "is_gxy": getattr(self, "is_gxy", ''),
            "is_gxz": getattr(self, "is_gxz", ''),
            "is_gxt": getattr(self, "is_gxt", ''),
            "is_gns": getattr(self, "is_gns", ''),
            "is_jzx": getattr(self, "is_jzx", ''),
            "glu": getattr(self, "glu", ''),
            "is_yc_glu": int(getattr(self, "is_yc_glu", '')),
            "glu2": getattr(self, "glu2", ''),
            "is_yc_glu2": int(getattr(self, "is_yc_glu2", '')),
            "hbalc": getattr(self, "hbalc", ''),
            "is_yc_hbalc": int(getattr(self, "is_yc_hbalc", '')),
            "ua": getattr(self, "ua", ''),
            "is_yc_ua": int(getattr(self, "is_yc_ua", '')),
            "tch": getattr(self, "tch", ''),
            "is_yc_tch": int(getattr(self, "is_yc_tch", '')),
            "tg": getattr(self, "tg", ''),
            "is_yc_tg": int(getattr(self, "is_yc_tg", '')),
            "hdl": getattr(self, "hdl", ''),
            "is_yc_hdl": int(getattr(self, "is_yc_hdl", '')),
            "ldl": getattr(self, "ldl", ''),
            "is_yc_ldl": int(getattr(self, "is_yc_ldl", '')),
            "hbp": getattr(self, "hbp", ''),
            "is_yc_hbp": int(getattr(self, "is_yc_hbp", '')),
            "lbp": getattr(self, "lbp", ''),
            "is_yc_lbp": int(getattr(self, "is_yc_lbp", ''))
        }

def get_mbgl_sql():
    return '''
    SELECT 
    tjbh,xm,xb,CAST(nl AS VARCHAR) AS nl,sfzh,sjhm,dwmc,CAST(ysje AS VARCHAR) AS ysje,is_gxy,is_gxz,is_gxt,is_gns,is_jzx,glu,is_yc_glu,glu2,is_yc_glu2,hbalc,is_yc_hbalc,ua,
    is_yc_ua,tch,is_yc_tch,tg,is_yc_tg,hdl,is_yc_hdl,ldl,is_yc_ldl,hbp,is_yc_hbp,lbp,is_yc_lbp
    FROM MB_YSKH WHERE 
    '''

def get_base_where(where_str):
    return '''
    WITH 
        T1 AS (
        SELECT 
        (CASE sumover 
            WHEN '0' THEN '未总检'
            WHEN '9' THEN '待审核'
            WHEN '1' THEN '已审核'
        ELSE '' END) AS TJZT,	
        TJBH,XM,XB,NL,TJ_TJDAB.SJHM,SFZH,QDRQ,TJ_TJDJB.DWBH,ywy,YSJE,JY FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH 
         AND %s AND QD='1' AND (del <> '1' or del is null)
        
    ''' %where_str

# 获取心内科
def get_xnk_sql():
    return '''
            SELECT 
            T1.TJZT,
            T1.TJBH,
            T1.XM,
            (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
            T1.NL,
            T1.SJHM,
            T1.sfzh,
            T1.ysje,
            substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
            (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
            (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
            (CASE TJ_TJJLMXB.XMBH 
                WHEN '280091' THEN '螺旋CT' 
                WHEN '050057' THEN '颈部彩超' 
                WHEN '540018' THEN '动脉硬化' 
                ELSE TJ_TJJLMXB.XMMC  END
             ) AS XMMC,
            (CASE WHEN XMBH='540018' THEN TJ_TJJLMXB.JG ELSE TJ_TJJLMXB.ZD END) AS XMZD,
            (CASE WHEN XMBH='540018' THEN '' ELSE TJ_TJJLMXB.JG END) AS XMJG
            FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 
            AND TJ_TJJLMXB.XMBH IN ('280091','050057','050072','540018') AND TJ_TJJLMXB.SFZH='0' 
            ORDER BY TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ
    '''

# 获取肝病科
def get_gbk_sql():
    return '''
    SELECT T1.TJZT,T1.TJBH,
        T1.XM,
        (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
        T1.nl,
        T1.sjhm,
        T1.sfzh,
        T1.ysje,
        substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
        (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
        (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
         TJ_TJJLMXB.XMMC,
         (CASE WHEN TJ_TJJLMXB.ZD IS NULL THEN TJ_TJJLMXB.CKFW ELSE TJ_TJJLMXB.ZD END) AS XMZD,
        TJ_TJJLMXB.JG AS XMJG
        FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 
        AND TJ_TJJLMXB.ZHBH IN ('1075','1074','1063','1076','1124','1125','4512','1127','4504','4505','4501','4502','4503','4548','1098','501258','500658','500660','500818','370321') 
        AND TJ_TJJLMXB.SFZH='0' AND TJ_TJJLMXB.YCBZ='1' AND TJ_TJJLMXB.qzjs IS NULL
        ORDER BY T1.TJBH,TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ
    '''

# 获取妇科SQL
def get_fk_sql():
    return '''
        SELECT T1.TJZT,T1.TJBH,
        T1.XM,
        (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
        T1.nl,
        T1.sjhm,
        T1.sfzh,
        T1.ysje,
        substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
        (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
        (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
         TJ_TJJLMXB.XMMC,
         (CASE WHEN TJ_TJJLMXB.ZD IS NULL THEN TJ_TJJLMXB.CKFW ELSE TJ_TJJLMXB.ZD END) AS XMZD,
        TJ_TJJLMXB.JG AS XMJG
        FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 
        AND TJ_TJJLMXB.XMBH IN (SELECT XMBH FROM TJ_ZHMX WHERE ZHBH IN ('4585','4527','4529','1914','1910','1930','1933','1909','501699','501780') )
        AND TJ_TJJLMXB.SFZH='0' AND TJ_TJJLMXB.YCBZ='1' AND TJ_TJJLMXB.qzjs IS NULL
        ORDER BY T1.TJBH,TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ  
    '''

# 获取心胸外科
def get_xxwk_sql():
    return '''
        SELECT T1.TJZT,T1.TJBH,
        T1.XM,
        (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
        T1.nl,
        T1.sjhm,
        T1.sfzh,
        T1.ysje,
        substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
        (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
        (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
         TJ_TJJLMXB.XMMC,
         (CASE WHEN TJ_TJJLMXB.ZD IS NULL THEN TJ_TJJLMXB.CKFW ELSE TJ_TJJLMXB.ZD END) AS XMZD,
        TJ_TJJLMXB.JG AS XMJG
        FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 

        AND TJ_TJJLMXB.XMBH IN ('280008','280018','370313','370314','370315','370316','370317','370318','370319','140048')

        AND TJ_TJJLMXB.SFZH='0' AND TJ_TJJLMXB.YCBZ='1' AND TJ_TJJLMXB.qzjs IS NULL

        ORDER BY T1.TJBH,TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ  
    '''

# 获取消化内科
def get_xhnk_sql():
    return '''
        SELECT T1.TJZT,T1.TJBH,
        T1.XM,
        (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
        T1.nl,
        T1.sjhm,
        T1.sfzh,
        T1.ysje,
        substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
        (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
        (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
         TJ_TJJLMXB.XMMC,
         (CASE WHEN TJ_TJJLMXB.ZD IS NULL THEN TJ_TJJLMXB.CKFW ELSE TJ_TJJLMXB.ZD END) AS XMZD,
        TJ_TJJLMXB.JG AS XMJG
        FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 

        AND TJ_TJJLMXB.XMBH IN ('500001','500002','370269','370270','370271','190017','190021','270008','270010','500012','500013')

        AND TJ_TJJLMXB.SFZH='0' AND TJ_TJJLMXB.YCBZ='1' AND TJ_TJJLMXB.qzjs IS NULL

        ORDER BY T1.TJBH,TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ  
    '''

# 获取泌尿科SQL
def get_mnk_sql():
    return '''
        SELECT T1.TJZT,T1.TJBH,
        T1.XM,
        (CASE T1.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END ) AS XB,
        T1.nl,
        T1.sjhm,
        T1.sfzh,
        T1.ysje,
        substring(convert(char,T1.QDRQ,120),1,10) as TJRQ,
        (select MC from TJ_DWDMB where DWBH=T1.DWBH) as DWMC,
        (select ygxm from tj_ygdm where yggh=T1.ywy ) as YWY,
         TJ_TJJLMXB.XMMC,
         (CASE WHEN TJ_TJJLMXB.ZD IS NULL THEN TJ_TJJLMXB.CKFW ELSE TJ_TJJLMXB.ZD END) AS XMZD,
        TJ_TJJLMXB.JG AS XMJG,
        T1.JY,
        TJ_TJJLMXB.XMBH
        FROM T1 INNER JOIN TJ_TJJLMXB ON T1.TJBH=TJ_TJJLMXB.TJBH 
        
        AND TJ_TJJLMXB.XMBH IN ('050060','050063','280029','280001','140049','120058')
        
        AND TJ_TJJLMXB.SFZH='0' AND TJ_TJJLMXB.YCBZ='1' AND TJ_TJJLMXB.qzjs IS NULL
        
        ORDER BY T1.TJBH,TJ_TJJLMXB.XMBH,T1.DWBH,T1.QDRQ  
    '''
# 获取泌尿科清洗后的结果
def get_clean_result(results):
    # 条件
    yxs = ['前列腺增生', '肾囊肿', '肾结石', '输尿管结石', '肾积水', '肾肿瘤', '肾上腺占位', '肾上腺肿瘤', '肾上腺增粗',
           '肾上腺增厚', '膀胱肿瘤', '膀胱占位', '膀胱沟疝', '睾丸鞘膜积液']
    # PSA >6
    # 红细胞(RBC) > 15

    datas = []
    for result in results:
        # result = ['tjzt','tjbh', 'xm', 'xb', 'nl', 'sjhm', 'sfzh','ysje','qdrq','dwmc','ywy','xmmc','xmjg','xmzd','jy','xmbh']
        if select(result,yxs):
            new_result = list(result)
            new_result.pop(-1)
            new_result.pop(-1)
            datas.append(new_result)

    return datas


# 前列腺彩超及CT类项目
def select_1(zd,jy,bscz):
    '''
    :param zd: 项目诊断
    :param jy:  报告建议
    :param bscz:标识词组，异常
    :return:
    '''
    for yx in bscz:
        if yx in zd:
            return True
        elif yx in jy:
            return True
    return False

def select(result:list,ycct:list):
    if result[-1] == '140049':
        if float2(result[-3]) > 6:
            return True
    elif result[-1] in ['120058','130059']:
        if float2(result[-3]) >= 10:
            return True
    else:
        if select_1(str2(result[-4]), str2(result[-2]),ycct):
            return True

    return False

def float2(result):
    if not result:
        return 0
    else:
        try:
            return float(result)
        except Exception as e:
            print(e)
            return 0
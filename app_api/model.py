from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class MT_TJ_ShortUrl(db.Model):

    __tablename__ = 'TJ_Short_Url'

    SUID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tjbh = db.Column(db.String(16, 'Chinese_PRC_CI_AS'), nullable=False)
    url_long = db.Column(db.String(200, 'Chinese_PRC_CI_AS'), nullable=False)
    url_short = db.Column(db.String(200, 'Chinese_PRC_CI_AS'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

# MT 表示 表 MV 表示视图
class MT_TJ_FILE_ACTIVE(db.Model):

    __tablename__ = "TJ_FILE_ACTIVE"

    rid = db.Column(db.BigInteger, primary_key=True)
    tjbh = db.Column(db.String(16))
    dwbh = db.Column(db.CHAR(5))
    ryear = db.Column(db.CHAR(4))
    rmonth = db.Column(db.CHAR(7))
    rday = db.Column(db.CHAR(10))
    localfile = db.Column(db.String(250))
    ftpfile = db.Column(db.String(100))
    filename = db.Column(db.String(20))
    filetype = db.Column(db.CHAR(2))
    filetypename = db.Column(db.String(20))
    filesize = db.Column(db.Float)
    filemtime = db.Column(db.BigInteger)
    createtime = db.Column(db.DateTime)


# 自动更新表
class MT_TJ_UPDATE(db.Model):

    __tablename__ = "TJ_UPDATE"

    upid = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Float)
    ufile = db.Column(db.Text)
    describe = db.Column(db.Text)
    uptime = db.Column(db.DateTime)
    platform = db.Column(db.CHAR(1))

class MT_TJ_BGGL(db.Model):

    __tablename__ = 'TJ_BGGL'

    tjbh = db.Column(db.String(16), primary_key=True)                         # 体检编号
    bgzt = db.Column(db.CHAR(1), nullable=True)                               # 报告状态 默认：追踪(0) 审核完成待审阅(1) 审阅完成待打印(2) 打印完成待整理(3)
    djrq = db.Column(db.DateTime, nullable=True)                              # 登记日期
    djgh = db.Column(db.String(16), nullable=False)                           # 登记工号
    djxm = db.Column(db.String(16), nullable=False)                           # 登记姓名
    qdrq = db.Column(db.DateTime, nullable=True)                              # 签到日期
    qdgh = db.Column(db.String(16), nullable=False)                           # 签到工号
    qdxm = db.Column(db.String(16), nullable=False)                           # 签到姓名
    sdrq = db.Column(db.DateTime, nullable=False)                             # 收单日期
    sdgh = db.Column(db.String(16), nullable=False)                           # 收单工号
    sdxm = db.Column(db.String(16), nullable=False)                           # 收单姓名
    zzrq = db.Column(db.DateTime, nullable=False,)                            # 追踪日期
    zzgh = db.Column(db.String(16), nullable=False)                           # 追踪工号
    zzxm = db.Column(db.String(16), nullable=False)                           # 追踪姓名
    zzbz = db.Column(db.Text, nullable=False)                                 # 追踪备注    记录电话等沟通信息，强制接收等信息
    zjrq = db.Column(db.DateTime, nullable=False)                             # 总检日期
    zjgh = db.Column(db.String(16), nullable=False)                           # 总检工号
    zjxm = db.Column(db.String(16), nullable=False)                           # 总检姓名
    zjbz = db.Column(db.Text, nullable=False)                                 # 总检备注
    shrq = db.Column(db.DateTime, nullable=False)                             # 审核日期
    shgh = db.Column(db.String(16), nullable=False)                           # 审核工号
    shxm = db.Column(db.String(16), nullable=False)                           # 审核姓名
    shbz = db.Column(db.Text, nullable=False)                                 # 审核备注    记录退回原因
    syrq = db.Column(db.DateTime, nullable=False)                             # 审阅日期
    sygh = db.Column(db.String(16), nullable=False)                           # 审阅工号
    syxm = db.Column(db.String(16), nullable=False)                           # 审阅姓名
    sybz = db.Column(db.Text, nullable=False)                                 # 审阅备注    记录退回原因
    dyrq = db.Column(db.DateTime, nullable=False)                             # 打印日期
    dygh = db.Column(db.String(16), nullable=False)                           # 打印工号
    dyxm = db.Column(db.String(16), nullable=False)                           # 打印姓名
    dyfs = db.Column(db.CHAR(1), nullable=True, default='0')                  # 打印方式 默认 0  自助打印 1
    dycs = db.Column(db.Integer, nullable=True, default=0)                    # 打印次数 默认 0
    zlrq = db.Column(db.DateTime, nullable=False)                             # 整理日期
    zlgh = db.Column(db.String(16), nullable=False)                           # 整理工号
    zlxm = db.Column(db.String(16), nullable=False)                           # 整理姓名
    zlhm = db.Column(db.String(16), nullable=False)                           # 整理货号
    lqrq = db.Column(db.DateTime, nullable=False)                             # 领取日期
    lqgh = db.Column(db.String(16), nullable=False)                           # 领取工号
    lqxm = db.Column(db.String(16), nullable=False)                           # 领取姓名
    lqbz = db.Column(db.Text, nullable=False)                                 # 领取备注    记录领取信息
    bgym = db.Column(db.Integer, nullable=True, default=0)                    # 报告页码，默认0页
    bglj = db.Column(db.String(250), nullable=False)                          # 报告路径 只存储对应PDF、HTML根路径
    bgms = db.Column(db.CHAR(1), nullable=False,default='0')                  # 报告模式 默认HTML 1 PDF


def get_report_progress_sum_sql(dwbh):
    return '''
            WITH 
                T1 AS (
                SELECT TJZT,TJBH,del,QD,SUMOVER,dybj FROM TJ_TJDJB WHERE DWBH ='%s'
                ),
                T2 AS (
                SELECT BGZT,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
                ),
                T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN 'tjlq'
                        WHEN BGZT ='4' THEN 'tjzl'
                        WHEN BGZT ='3' OR dybj='1' THEN 'tjdy'
                        WHEN BGZT ='2' THEN 'tjsy'
                        WHEN BGZT ='0' THEN 'tjzz'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN 'tjsh'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN 'tjzj'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN 'tjqd' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN 'tjdj'
                        WHEN TJZT ='0' OR del='1' THEN 'tjqx'
                        ELSE '' END
                    ) AS TJZT,T1.TJBH FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT TJZT,COUNT(TJBH) FROM T3 GROUP BY TJZT

    ''' % dwbh

def get_report_progress_sum2_sql(dwbh,tstart,tend):
    return '''
            WITH 
                T1 AS (
                SELECT TJZT,TJBH,del,QD,SUMOVER,dybj FROM TJ_TJDJB WHERE DWBH ='%s' 
                AND  (del <> '1' or del is null) and QD='1' and (QDRQ>='%s' and QDRQ<'%s')
                ),
                T2 AS (
                SELECT BGZT,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
                ),
                T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN 'tjlq'
                        WHEN BGZT ='4' THEN 'tjzl'
                        WHEN BGZT ='3' OR dybj='1' THEN 'tjdy'
                        WHEN BGZT ='2' THEN 'tjsy'
                        WHEN BGZT ='0' THEN 'tjzz'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN 'tjsh'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN 'tjzj'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN 'tjqd' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN 'tjdj'
                        WHEN TJZT ='0' OR del='1' THEN 'tjqx'
                        ELSE '' END
                    ) AS TJZT,T1.TJBH FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT TJZT,COUNT(TJBH) FROM T3 GROUP BY TJZT

    ''' % (dwbh,tstart,tend)

def get_report_progress_sql(bgzt, dwbh, where_tjzt):
    return '''
            WITH 
            T1 AS (
                SELECT TJZT,TJBH,XM,XB,NL,TJ_TJDAB.SFZH,TJ_TJDAB.SJHM,depart,TJ_TJDJB.DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,del,QD,SUMOVER,dybj,jy  FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH =TJ_TJDAB.DABH AND TJ_TJDJB.DWBH ='%s'
            ),
            T2 AS (
                SELECT BGZT,SYRQ,DYRQ,ZLRQ,LQRQ,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
            ),
            T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN 'tjlq'
                        WHEN BGZT ='4' THEN 'tjzl'
                        WHEN BGZT ='3' OR dybj='1' THEN 'tjdy'
                        WHEN BGZT ='2' THEN 'tjsy'
                        WHEN BGZT ='0' THEN 'tjzz'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN 'tjsh'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN 'tjzj'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN 'tjqd' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN 'tjdj'
                        WHEN TJZT ='0' OR del='1' THEN 'tjqx'
                        ELSE '' END
                    ) AS TJZT2,
                    T1.TJBH,XM,XB,NL,DWBH,SFZH,SJHM,depart,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,SYRQ,DYRQ,ZLRQ,LQRQ,jy FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT
                '%s',TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,NL,SFZH,SJHM,
                substring(convert(char,QDRQ,120),1,10) AS QDRQ,jy,YSJE,depart,
                substring(convert(char,DJRQ,120),1,10) AS DJRQ,
                substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
                substring(convert(char,SHRQ,120),1,10) AS SHRQ,
                substring(convert(char,SYRQ,120),1,10) AS SYRQ,
                (case 
                WHEN BGRQ IS NULL THEN substring(convert(char,DYRQ,120),1,10)
                ELSE substring(convert(char,BGRQ,120),1,10) END )
                AS DYRQ,
                substring(convert(char,ZLRQ,120),1,10) AS ZLRQ,
                substring(convert(char,LQRQ,120),1,10) AS LQRQ,
            (select MC from TJ_DWDMB where DWBH=T3.DWBH) AS DWMC

            FROM T3 %s

    ''' % (dwbh, bgzt,where_tjzt)

def get_report_progress2_sql(bgzt, dwbh, tjzt,tstart,tend):
    return '''
            WITH 
            T1 AS (
                SELECT TJZT,TJBH,XM,XB,NL,TJ_TJDAB.SFZH,TJ_TJDAB.SJHM,depart,TJ_TJDJB.DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,del,QD,SUMOVER,dybj,jy  FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH =TJ_TJDAB.DABH AND TJ_TJDJB.DWBH ='%s'
                AND  (del <> '1' or del is null) and QD='1' and (QDRQ>='%s' and QDRQ<'%s')
            ),
            T2 AS (
                SELECT BGZT,SYRQ,DYRQ,ZLRQ,LQRQ,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
            ),
            T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN 'tjlq'
                        WHEN BGZT ='4' THEN 'tjzl'
                        WHEN BGZT ='3' OR dybj='1' THEN 'tjdy'
                        WHEN BGZT ='2' THEN 'tjsy'
                        WHEN BGZT ='0' THEN 'tjzz'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN 'tjsh'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN 'tjzj'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN 'tjqd' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN 'tjdj'
                        WHEN TJZT ='0' OR del='1' THEN 'tjqx'
                        ELSE '' END
                    ) AS TJZT2,
                    T1.TJBH,XM,XB,NL,SFZH,SJHM,depart,DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,SYRQ,DYRQ,ZLRQ,LQRQ,jy FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT
                '%s',TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,NL,SFZH,SJHM,
                substring(convert(char,QDRQ,120),1,10) AS QDRQ,jy,YSJE,depart,
                substring(convert(char,DJRQ,120),1,10) AS DJRQ,
                substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
                substring(convert(char,SHRQ,120),1,10) AS SHRQ,
                substring(convert(char,SYRQ,120),1,10) AS SYRQ,
                (case 
                WHEN BGRQ IS NULL THEN substring(convert(char,DYRQ,120),1,10)
                ELSE substring(convert(char,BGRQ,120),1,10) END )
                AS DYRQ,
                substring(convert(char,ZLRQ,120),1,10) AS ZLRQ,
                substring(convert(char,LQRQ,120),1,10) AS LQRQ,
            (select MC from TJ_DWDMB where DWBH=T3.DWBH) AS DWMC

            FROM T3 %s

    ''' % (dwbh,tstart,tend, bgzt, tjzt)

def get_report_progress_sql2(dwbh):
    return '''
        WITH 
            T1 AS (
                SELECT TJZT,TJBH,XM,XB,NL,TJ_TJDJB.DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,del,QD,SUMOVER,dybj FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH =TJ_TJDAB.DABH AND TJ_TJDJB.DWBH ='%s'
            ),
            T2 AS (
                SELECT BGZT,SYRQ,DYRQ,ZLRQ,LQRQ,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
            ),
            T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN 'tjlq'
                        WHEN BGZT ='4' THEN 'tjzl'
                        WHEN BGZT ='3' OR dybj='1' THEN 'tjdy'
                        WHEN BGZT ='2' THEN 'tjsy'
                        WHEN BGZT ='0' THEN 'tjzz'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN 'tjsh'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN 'tjzj'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN 'tjqd' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN 'tjdj'
                        WHEN TJZT ='0' OR del='1' THEN 'tjqx'
                        ELSE TJZT END
                    ) AS TJZT2,
                    T1.TJBH,XM,XB,NL,DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,SYRQ,SYXM,DYRQ,ZLRQ,LQRQ FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT
                TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,NL,YSJE,
                substring(convert(char,DJRQ,120),1,10) AS DJRQ,
                substring(convert(char,QDRQ,120),1,10) AS QDRQ,
                substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
                substring(convert(char,SHRQ,120),1,10) AS SHRQ,
                substring(convert(char,SYRQ,120),1,10) AS SYRQ,
                substring(convert(char,DYRQ,120),1,10) AS DYRQ,
                substring(convert(char,ZLRQ,120),1,10) AS ZLRQ,
                substring(convert(char,LQRQ,120),1,10) AS LQRQ,
            (select MC from TJ_DWDMB where DWBH=T3.DWBH) AS DWMC

            FROM T3

    ''' % dwbh

# 获取个人体检进度
def get_user_progress_sql(where):
    return '''
            WITH 
            T1 AS (
                SELECT TJZT,TJBH,XM,XB,NL,TJ_TJDAB.SFZH,TJ_TJDAB.SJHM,depart,TJ_TJDJB.DWBH,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,del,QD,SUMOVER,dybj,jy  FROM TJ_TJDJB INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH =TJ_TJDAB.DABH 
               %s
            ),
            T2 AS (
                SELECT BGZT,SYRQ,DYRQ,ZLRQ,LQRQ,TJBH FROM TJ_BGGL WHERE TJBH IN (SELECT TJBH FROM T1)
            ),
            T3 AS (
                SELECT 
                    (CASE 
                        WHEN BGZT ='5' THEN '已领取'
                        WHEN BGZT ='4' THEN '已整理'
                        WHEN BGZT ='3' OR dybj='1' THEN '已打印'
                        WHEN BGZT ='2' THEN '已审阅'
                        WHEN BGZT ='0' THEN '追踪中'
                        WHEN TJZT ='7' OR (SUMOVER='1' AND (del IS NULL OR del='')) THEN '已审核'
                        WHEN TJZT ='6' OR (SUMOVER='9' AND (del IS NULL OR del='')) THEN '已总检'
                        WHEN TJZT IN ('3','4') OR (QD='1' AND (del IS NULL OR del='')) THEN '已签到' 
                        WHEN TJZT IN ('1','2') OR ((QD IS NULL OR QD='') AND (del IS NULL OR del=''))  THEN '已登记'
                        WHEN TJZT ='0' OR del='1' THEN '已取消'
                        ELSE '' END
                    ) AS TJZT2,
                    T1.TJBH,XM,XB,NL,DWBH,SFZH,SJHM,depart,YSJE,DJRQ,QDRQ,ZJRQ,SHRQ,BGRQ,SYRQ,DYRQ,ZLRQ,LQRQ,jy FROM T1 LEFT JOIN T2 ON T1.TJBH=T2.TJBH 
                )

            SELECT
                TJZT2,TJBH,XM,(CASE XB WHEN '1' THEN '男' ELSE '女' END) AS XB,NL,SFZH,SJHM,
                substring(convert(char,QDRQ,120),1,10) AS QDRQ,jy,YSJE,depart,
                substring(convert(char,DJRQ,120),1,10) AS DJRQ,
                substring(convert(char,ZJRQ,120),1,10) AS ZJRQ,
                substring(convert(char,SHRQ,120),1,10) AS SHRQ,
                substring(convert(char,SYRQ,120),1,10) AS SYRQ,
                (case 
                WHEN BGRQ IS NULL THEN substring(convert(char,DYRQ,120),1,10)
                ELSE substring(convert(char,BGRQ,120),1,10) END )
                AS DYRQ,
                substring(convert(char,ZLRQ,120),1,10) AS ZLRQ,
                substring(convert(char,LQRQ,120),1,10) AS LQRQ,
            (select MC from TJ_DWDMB where DWBH=T3.DWBH) AS DWMC

            FROM T3 

    ''' %where
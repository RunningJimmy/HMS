from utils.bmodel import *
from datetime import datetime
import time

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

def cur_time():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(int(time.time())))

def cur_date(count=0):
    interval = 86400
    return time.strftime("%Y-%m-%d", time.localtime(int(time.time())+count*interval))

def cur_date2():
    date = time.strftime("%Y%m%d", time.localtime(int(time.time())))
    return date[2:]

class MV_CX_ALL(BaseModel):

    __tablename__ = 'V_CX_ALL'

    tjbh = Column(VARCHAR(20), primary_key=True)
    xm = Column(VARCHAR(20),nullable=False)
    xb = Column(VARCHAR(20),nullable=False)
    nl = Column(Integer, nullable=False)
    tmbh = Column(VARCHAR(20), nullable=False)
    xmhz = Column(VARCHAR(250), nullable=False)
    sjhm = Column(VARCHAR(20), nullable=False)
    sfzh = Column(VARCHAR(20), nullable=False)
    depart = Column(VARCHAR(50), nullable=False)
    dwmc = Column(VARCHAR(100), nullable=False)
    djrq = Column(VARCHAR(20), nullable=False)
    qdrq = Column(VARCHAR(20), nullable=False)

    def to_dict(self):
        return {
            'tjbh':getattr(self, "tjbh"),
            'xm': str2(getattr(self, "xm")),
            'xb': str2(getattr(self, "xb")),
            'nl': '%s 岁' %str(getattr(self, "nl")),
            'tmbh': getattr(self, "tmbh"),
            'xmhz': getattr(self, "xmhz"),
            'sfzh': getattr(self, "sfzh"),
            'sjhm': getattr(self, "sjhm"),
            'depart': str2(getattr(self, "depart")),
            'dwmc': getattr(self, "dwmc"),
            'djrq': getattr(self, "djrq"),
            'qdrq': getattr(self, "qdrq")
        }


def get_tjbh_sql(tmbh):
    sql = '''
    SELECT TJBH FROM TJ_TJJLMXB WHERE TMBH1='%s' GROUP BY TJBH
    ''' %tmbh
    return sql

# 获取采血+采样
def get_tmxx_sql(tjbh):
    sql='''
    WITH 
        T1 AS (
            SELECT TJBH,XMMC,(CASE WHEN XMBH IN ('1931','5010','1926','1000320','1000321') THEN TJBH+XMBH ELSE TMBH1 END) AS TMBH 
            FROM TJ_TJJLMXB WHERE TJBH='%s' AND SFZH='1' 
            AND (
                       (XMBH IN (SELECT XMBH FROM TJ_XMDM WHERE LBBM IN (SELECT LBBM FROM TJ_XMLB WHERE XMLX='2' )) AND TMBH1 IS NOT NULL) 
                    OR (XMBH IN ('1931','5010','1926','1000320','1000321'))
                 )
        ),
        T2 AS (
            SELECT T1.TJBH,T1.TMBH,(SELECT XMMC+'  ' FROM T1 AS C WHERE C.TJBH = T1.TJBH AND C.TMBH = T1.TMBH  FOR XML PATH('')  ) AS XMHZ from T1 
            GROUP BY T1.TJBH,T1.TMBH
        ),
        T3 AS (
                SELECT TJBH,MXBH AS TMBH FROM TJ_CZJLB WHERE JLLX IN ('0010','0011') GROUP BY TJBH,MXBH
        )

    SELECT T2.TJBH,T2.TMBH,T2.XMHZ,(SELECT 1 FROM T3 WHERE T3.TJBH = T2.TJBH AND T3.TMBH=T2.TMBH ) AS ISCX,
     (SELECT (CASE WHEN (qzjs is null or qzjs='') THEN 0 ELSE 1 END) as qzjs FROM TJ_TJJLMXB WHERE TJ_TJJLMXB.TJBH = T2.TJBH AND TJ_TJJLMXB.XMMC=T2.XMHZ AND TJ_TJJLMXB.SFZH = '1') AS SFJJ
     FROM T2 WHERE TJBH='%s';
    ''' %(tjbh,tjbh)

    return sql

# 获取采样的
def get_tmxx2_sql(tjbh):
    sql='''
    WITH 
        T1 AS (
            SELECT TJBH,XMMC,(CASE WHEN XMBH IN ('1931','5010','1926') THEN TJBH+XMBH ELSE TMBH1 END) AS TMBH 
            FROM TJ_TJJLMXB WHERE TJBH='%s' AND SFZH='1' 
            AND (
                       (XMBH IN (SELECT XMBH FROM TJ_XMDM WHERE LBBM IN (SELECT LBBM FROM TJ_XMLB WHERE XMLX='2' )) AND TMBH1 IS NOT NULL) 
                    OR (XMBH IN ('1931','5010','1926'))
                 )
        ),
        T2 AS (
            SELECT T1.TJBH,T1.TMBH,(SELECT XMMC+'  ' FROM T1 AS C WHERE C.TJBH = T1.TJBH AND C.TMBH = T1.TMBH  FOR XML PATH('')  ) AS XMHZ from T1 
            GROUP BY T1.TJBH,T1.TMBH
        ),
        T3 AS (
                SELECT TJBH,MXBH AS TMBH FROM TJ_CZJLB WHERE JLLX='0011' GROUP BY TJBH,MXBH
        )

    SELECT T2.TJBH,T2.TMBH,T2.XMHZ,(SELECT 1 FROM T3 WHERE T3.TJBH = T2.TJBH AND T3.TMBH=T2.TMBH ) AS ISCX,
     (SELECT qzjs FROM TJ_TJJLMXB WHERE TJ_TJJLMXB.TJBH = T2.TJBH AND TJ_TJJLMXB.XMMC=T2.XMHZ AND TJ_TJJLMXB.SFZH = '1') AS SFJJ
     FROM T2 WHERE TJBH='%s';
    ''' %(tjbh,tjbh)

    return sql

# 检查样本类型
def get_yblx_sql():
    sql= '''
        SELECT (SELECT XMMC FROM TJ_XMDM WHERE XMBH = aa.XMBH) as XMMC,rtrim(bb.YBLX) as YBLX FROM TJ_SFTJB AS aa
    
        INNER JOIN 
        
        (SELECT SFBH,SFMC,YBLX,(SELECT DMMC FROM GY_DMZD WHERE DMLB='1196' AND DMSB>0 AND DMSB=TJ_SFXMB.YBLX) AS YBMC FROM TJ_SFXMB WHERE YBLX IS NOT NULL) AS bb
        
        ON aa.SFBH=bb.SFBH
        
    '''
    return sql

# 样本试管名称
def get_tmsg_sql():
    sql = '''
    SELECT 
        XMBH,
        (SELECT XMMC FROM TJ_XMDM WHERE XMBH=TJ_SFTJB.XMBH) AS XMMC, 
        (SELECT SFMC FROM TJ_SFXMB WHERE SFBH = TJ_SFTJB.SFBH) AS SGMC  
    FROM TJ_SFTJB
    '''
    return sql

# 拒检
def get_xmjj_sql(tjbh,tmbh,login_id,login_name,login_area):
    sql='''
    UPDATE TJ_TJJLMXB SET ZXPB='1',jsbz='1',qzjs='1',JCRQ='%s',JCYS='%s' WHERE TJBH='%s' AND TMBH1='%s';
    INSERT INTO TJ_CZJLB(jllx,jlmc,tjbh,mxbh,CZGH,CZXM,CZQY,CZSJ)values('0012','拒检','%s','%s','%s','%s','%s','%s');
    ''' \
        %(cur_datetime(),login_id,tjbh,tmbh,tjbh,tmbh,login_id,login_name,login_area,cur_datetime())

    return sql

# 样本交接 条码数量汇总
def get_handover_sql(t_start,t_end,area,some_where):
    return '''
        SELECT '%s' AS QSSJ,'%s' AS JSSJ,CZQY,CAST(BZ AS VARCHAR) AS SGYS,count(*) as SGSL,

        JJXM,JJSJ,JSXM,JSSJ
    
        FROM TJ_CZJLB 
        
        WHERE CZSJ BETWEEN '%s' AND '%s'
        
        AND JLLX IN ('0010','0011')  
        
        AND CZQY LIKE '%s%%'
        
        %s
        
        GROUP BY CZQY,CAST(BZ AS VARCHAR),JJXM,JJSJ,JSXM,JSSJ
        
        ORDER BY CZQY,count(*) DESC ;
        
    ''' %(t_start,t_end,t_start,t_end,area,some_where)


# 样本交接 条码数量汇总  明州的时候 汇总
def get_handover2_sql(t_start, t_end, area, some_where):
    return '''
        SELECT '%s' AS QSSJ,'%s' AS JSSJ,LEFT(CZQY,2) as CZQY,CAST(BZ AS VARCHAR) AS SGYS,count(*) as SGSL,

        JJXM,JJSJ,JSXM,JSSJ

        FROM TJ_CZJLB 

        WHERE CZSJ BETWEEN '%s' AND '%s'

        AND JLLX IN ('0010','0011')  

        AND CZQY LIKE '%s%%'
        
        %s

        GROUP BY LEFT(CZQY,2),CAST(BZ AS VARCHAR),JJXM,JJSJ,JSXM,JSSJ

        ORDER BY count(*) DESC ;

    ''' % (t_start, t_end, t_start, t_end, area,some_where)


# 获取当前留样信息，初始化用
def get_urine_init_sql(area):
    return '''
    SELECT 
        '已留样' AS state,
        TJ_TJDAB.XM,
        (CASE TJ_TJDAB.XB WHEN '1' THEN '男' WHEN '2' THEN '女' ELSE '' END) AS XB,
        TJ_TJDJB.NL,
        C.MXBH,
        TJ_TJDJB.TJBH,
        C.JLNR 
    FROM TJ_TJDJB 
        INNER JOIN TJ_TJDAB ON TJ_TJDJB.DABH=TJ_TJDAB.DABH AND (TJ_TJDJB.del <> '1' or TJ_TJDJB.del is null) and TJ_TJDJB.QD='1'
        INNER JOIN (SELECT TJBH,MXBH,JLNR FROM TJ_CZJLB  WHERE CZSJ>=substring(convert(char,GETDATE(),120),1,10) AND JLLX='0011' AND CZQY='%s') C
        
        ON TJ_TJDJB.TJBH=C.TJBH 
    ''' %area
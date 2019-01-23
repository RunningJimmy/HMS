from result.model import *
from utils import sms_api
from utils.dbconn import get_tjxt_session
from string import Template

def post_sms(sms_content_template,tjbh,sjhm):
    url = "http://tjbg.nbmzyy.com:5005/api/report/down/pdf/%s" %tjbh
    #print(Template(sms_content_template).safe_substitute({'url': url}),sjhm)
    sms_api(sjhm, Template(sms_content_template).safe_substitute({'url': url}))


if __name__ == "__main__":
    sql = '''SELECT * FROM  TJ_Short_Url WHERE create_time>='2019-01-19 05:52:22.877' AND tjbh NOT IN ('149520594','149520592') ; '''
    session = get_tjxt_session('10.8.200.201', 'tjxt', 'bsuser', 'admin2389')
    result = session.query(MT_TJ_SMSTemplate2.CONTENT).filter(MT_TJ_SMSTemplate2.TNAME == '报告领取',MT_TJ_SMSTemplate2.YXBZ == '1').limit(1).scalar()
    sms_content_template = str2(result)
    # print(sms_content_template)
    results = session.execute(sql).fetchall()
    for result in results:
        sjhm_obj = session.query(MV_RYXX).filter(MV_RYXX.tjbh == result[1]).scalar()
        if sjhm_obj:
            post_sms(sms_content_template,result[1],sjhm_obj.sjhm)
        # print(result)

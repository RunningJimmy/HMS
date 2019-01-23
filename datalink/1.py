from datalink.model import *
from utils.dbconn import get_cxk_session



if __name__=="__main__":
    engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
    session = sessionmaker(bind=engine)()
    pacs_session = get_cxk_session()
    results = pacs_session.execute("select tjbh,xmbh,jcys,jcrq,jg from TJ_TJJLMXB WHERE tjbh='180070021' ").fetchall()
    for result in results:
        if result[4]==None:
            jg = None
        else:
            jg = result[4]
        session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh==result[0],MT_TJ_TJJLMXB.xmbh==result[1]).update({
            MT_TJ_TJJLMXB.jcys:result[2],
            MT_TJ_TJJLMXB.jcrq: result[3],
            MT_TJ_TJJLMXB.jg: jg,
        })

    session.commit()


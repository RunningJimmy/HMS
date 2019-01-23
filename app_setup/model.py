from utils.bmodel import *

class MT_Permissions(BaseModel):

    __tablename__ = 'sys_permissions'

    pid = Column(INTEGER, primary_key=True, nullable=False)
    pname = Column(VARCHAR(20), nullable=False)
    pcontent = Column(Text, nullable=False)
    mtime = Column(DateTime, nullable=False)
    muser = Column(VARCHAR(20), nullable=False)


class MT_TJ_DWFZR(BaseModel):

    __tablename__ = 'TJ_DWFZR'

    yhid = Column(VARCHAR(20), primary_key=True, nullable=False)
    yhmc = Column(VARCHAR(20), nullable=False)
    yhmm = Column(VARCHAR(20), nullable=False)
    yxbz = Column(CHAR(1), nullable=False)
    bz = Column(VARCHAR(250), nullable=True)

    def to_dict(self):
        return {
            'yhid': getattr(self, "yhid"),
            'yhmc': str2(getattr(self, "yhmc")),
            'yhmm': getattr(self, "yhmm"),
            'yxbz': getattr(self, "yxbz"),
            'bz': str2(getattr(self, "bz"))
        }

class MT_TJ_DWFZRSQ(BaseModel):

    __tablename__ = 'TJ_DWFZRSQ'

    yhid = Column(VARCHAR(16), primary_key=True, nullable=False)
    dwbh = Column(VARCHAR(10), primary_key=True, nullable=False)


class MT_XMLB(BaseModel):
    __tablename__ = 'TJ_XMLB'

    LBBM = Column(CHAR(6, 'Chinese_PRC_CI_AS'), primary_key=True)
    LBMC = Column(String(60, 'Chinese_PRC_CI_AS'))
    XMLX = Column(CHAR(1, 'Chinese_PRC_CI_AS'))
    PYJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    WBJM = Column(String(50, 'Chinese_PRC_CI_AS'))
    ZDYM = Column(String(50, 'Chinese_PRC_CI_AS'))
    XSSX = Column(Integer)
    ZHXGR = Column(String(20, 'Chinese_PRC_CI_AS'))
    ZHXGRQ = Column(DateTime)

    def to_dict(self):
        return {col.name: str2(getattr(self, col.name, None)) for col in self.__table__.columns}
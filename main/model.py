from utils.bmodel import *

#用户登录权限表
class MT_TJ_USER(BaseModel):

    __tablename__ = 'SS_OPERATE_USER'

    xtsb = Column(Integer, primary_key=True)
    yhdm = Column(VARCHAR(20),primary_key=True)
    yhzm = Column(VARCHAR(20),nullable=False)
    yhmc = Column(VARCHAR(20), nullable=False)
    yhkl = Column(VARCHAR(50), nullable=False)
    yhzt = Column(Integer, nullable=False)


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

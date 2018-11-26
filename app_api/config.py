from flask import Flask
from flask_cors import CORS
from utils import gol
import logging,os
from logging.handlers import TimedRotatingFileHandler


def create_app():
    # 基础配置  # 修改静态文件夹的目录
    app = Flask(__name__,static_folder='', static_url_path='')
    # 跨域访问
    # CORS(app, supports_credentials=True,resources=r'/*')
    # app = Flask(__name__,static_url_path='/app_reportserver/')
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pymssql://bsuser:admin2389@10.8.200.201/tjxt"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
    # app.config["SQLALCHEMY_ECHO"] =False
    # app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True
    # app.config['UPLOAD_FOLDER'] = 'D:/tmp/'

    app.config["SQLALCHEMY_DATABASE_URI"] = gol.get_value("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = gol.get_value("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config["SQLALCHEMY_ECHO"] = gol.get_value("SQLALCHEMY_ECHO")
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = gol.get_value("SQLALCHEMY_COMMIT_ON_TEARDOWN")
    app.config['UPLOAD_FOLDER_PHOTO'] = gol.get_value("SQLALCHEMY_UPLOAD_FOLDER_PHOTO")
    app.config['UPLOAD_FOLDER_EQUIP'] = gol.get_value("SQLALCHEMY_UPLOAD_FOLDER_EQUIP")
    app.config['UPLOAD_FOLDER_REPORT'] = gol.get_value("SQLALCHEMY_UPLOAD_FOLDER_REPORT")
    app.config['UPLOAD_FOLDER_UPDATE'] = gol.get_value("SQLALCHEMY_UPLOAD_FOLDER_UPDATE")
    app.config['UPLOAD_FOLDER_TMP'] = gol.get_value("SQLALCHEMY_UPLOAD_FOLDER_TMP")

    # 日志配置
    # handler = TimedRotatingFileHandler(filename='api_server.log',when='d',interval=1,backupCount=10)
    # formatter = logging.Formatter('[%(asctime)s-%(levelname)s] - %(message)s')
    # handler.setLevel(logging.INFO)
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)

    return app


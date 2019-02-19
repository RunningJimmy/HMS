from flask import send_file,make_response,request,jsonify,abort,url_for,render_template,send_from_directory
from app_api.utils import cur_datetime
from app_api.exception import *
from app_api.model import *
import zeep,json,base64,os,ujson,time,urllib.parse,requests
import mimetypes,subprocess
from utils import gol,str2
from app_api.dbconn import *
import win32api,shutil
import win32print
from pyecharts import Bar
from collections import OrderedDict

'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMSServer
@file: report.py
@time: 2019-1-11 13:54
@desc: 报告API
'''


# 报告视图
def init_report_views(app,db,print_queue=None,report_queue=None):

    # 检验类报告
    @app.route('/api/lis/report/create/<string:tjbh>', methods=['POST'])
    def report_lis_create(tjbh):
        print(' %s：客户端(%s)：检验类报告生成请求！参数 tjbh：%s'  % (cur_datetime(), request.remote_addr, tjbh))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        mes_obj = {'tjbh': tjbh, 'action': 'lis'}
        if report_queue:
            report_queue.put(mes_obj)
        else:
            abort(404)

        return jsonify({'code': 1, 'mes': '检验类报告生成', 'data': ''})

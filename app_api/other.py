from flask import jsonify,request,json,abort,render_template
from app_api.model import *
import requests,time
from pyecharts import Bar
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMSServer
@file: other.py
@time: 2019-1-10 13:25
@desc: 外网API，请求中转
'''

# 初始化视图
def init_other_views(app,db,forward_request_address):

    # 转发请求(中转到外网)
    @app.route('/api/forward', methods=['POST'])
    def forward_request():
        request_args, request_data = request.args.to_dict(), request.data,
        action = request_args['action']
        if action=='url':
            forward_request_url = forward_request_address + '/api/other/short_url'
        else:
            forward_request_url = None
        request_args.pop('action')
        response = requests.post(forward_request_url, params=request_args, data=request_data)
        if response.status_code == 200:
            return response.text
        else:
            return jsonify({'code': 0, 'message': '%s' %str(response.status_code), 'data': ''})

    # 长网址转换为短网址
    @app.route('/api/other/short_url', methods=['POST'])
    def get_short_url():
        request_args,url_long = request.args,json.loads(str(request.data,'utf-8'))
        url = "http://suo.im/api.php"
        print(' %s：客户端(%s)：链接地址转换请求：参数 %s' % (cur_datetime(), request.remote_addr, url_long['url']))
        response = requests.get(url, params=url_long)
        # 保存数据
        try:
            obj = MT_TJ_ShortUrl()
            obj.tjbh = request_args['tjbh']
            obj.url_long = url_long['url']
            obj.url_short = response.text
            db.session.add(obj)
            db.session.commit()
            return jsonify({'code': 1, 'message': '', 'data': response.text})
        except Exception as e:
            return jsonify({'code': 0, 'message':'错误：%s'%e, 'data': ''})

    # 图片 => 文字 百度API
    @app.route('/api/other/pic2txt/', methods=['POST'])
    def pic2txt():
        file_obj = request.files['file']
        print(' %s：客户端(%s)：OCR服务请求：%s' % (cur_datetime(), request.remote_addr,file_obj.filename))
        url = "http://10.7.200.127:10006/api/pic2txt/"
        try:
            response = requests.post(url, files=request.files)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(' %s：客户端(%s)：OCR服务请求失败，错误信息：%s' % (cur_datetime(), request.remote_addr, e))
            abort(404)

    # 展示图表
    @app.route('/api/chart/show/', methods=['POST'])
    def show_chart():
        request_args, request_data = request.args.to_dict(), json.loads(str(request.data,'utf-8'))
        print(request_args, request_data)
        titles = request_data['bar_titles']
        datas = request_data['bar_datas']
        bar = Bar()
        if isinstance(datas,list):
            for index,data in enumerate(datas):
                build_chart(bar,titles[index],data)
        elif isinstance(datas, dict):
            build_chart(bar, titles, datas)

        ret_html = render_template('pyecharts.html',
                                   myechart=bar.render_embed(),
                                   mytitle=u"明州体检",
                                   host='/static',
                                   script_list=bar.get_js_dependencies())
        return ret_html

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

# 构建图
def build_chart(bar:Bar, title:str, datas:dict):
    axis_x = [key for key in datas.keys()]
    axis_y = list(datas.values())
    # 通用配置项都在add()中进行配置 具体见官网 http://pyecharts.org/#/
    bar.add(title, axis_x, axis_y, is_more_utils=True, xaxis_rotate=90)
    return bar
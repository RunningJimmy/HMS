from flask import jsonify,request,json,abort,render_template,send_file
from app_api.model import *
import requests,time,os
from utils import str2
from pyecharts import Bar,Pie,Gauge
from pyecharts_javascripthon.api import TRANSLATOR

# '''
# @author: zhufd
# @license: (C) Copyright 明州体检
# @contact: 13736093855
# @software: HMSServer
# @file: other.py
# @time: 2019-1-10 13:25
# @desc: 外网API，请求中转
# '''

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

    # 自适应
    @app.route('/api/chart/create/<string:chart_type>/<int:height>', methods=['POST'])
    def create_chart(chart_type,height):
        datas = json.loads(str(request.data,'utf-8'))
        title = datas.get('title')
        datas = datas.get('datas')
        if chart_type == 'bar':
            chart = build_chart_bar(title,datas)
        elif chart_type == 'pie':
            chart = build_chart_pie(title, datas)
        elif chart_type == 'guage':
            chart = build_chart_gauge(title,datas)
        else:
            chart = None
            abort(404)
        javascript_snippet = TRANSLATOR.translate(chart.options)
        html = render_template(
            'pyecharts2.html',
            chart_id=chart.chart_id,
            my_title=u"明州体检",
            host='/static',
            renderer=chart.renderer,
            my_width="100%",
            my_height=height,
            custom_function=javascript_snippet.function_snippet,
            options=javascript_snippet.option_snippet,
            script_list=chart.get_js_dependencies()
        )
        tmp_path = app.config['UPLOAD_FOLDER_TMP']
        tmp_filename = os.path.join(tmp_path, "%s_%s_%s.html" %(title,chart_type,cur_timep()))
        with open(tmp_filename,"w",encoding="UTF-8") as f:
            f.write(html)
        return jsonify({'code': 1, 'mes': '创建图表成功', 'data': os.path.basename(tmp_filename)})

    @app.route('/api/chart/show/<string:filename>', methods=['GET'])
    def show_chart(filename):
        tmp_path = app.config['UPLOAD_FOLDER_TMP']
        file_name = os.path.join(tmp_path,filename)
        if os.path.exists(file_name):
            return send_file(file_name)
        else:
            abort(404)

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

def cur_timep():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))

def get_datas(session,title,tstart,tend):
    pass

# 构建图
def build_chart_bar(title:str, datas:dict):
    axis_x = [str2(key) for key in datas.keys()]
    axis_y = list(datas.values())
    chart = Bar()
    # 通用配置项都在add()中进行配置 具体见官网 http://pyecharts.org/#/
    chart.add(title, axis_x, axis_y, is_more_utils=True, xaxis_rotate=90)
    return chart

# 构建饼图
def build_chart_pie(title:str,datas:dict):
    axis_x = [str2(key) for key in datas.keys()]
    axis_y = list(datas.values())
    chart = Pie(title,title_pos ='center')
    chart.add(
            '',axis_x,axis_y,           #''：图例名（不使用图例）
            radius = [25,55],           #环形内外圆的半径
            is_label_show = True,       #是否显示标签
            label_text_color = None,    #标签颜色
            legend_orient = 'vertical', #图例垂直
            legend_pos = 'left',
            is_more_utils=False
            )
    return chart

# 构建仪表盘，用于展示百分率的
def build_chart_gauge(title1:str,data:float):
    print()
    chart = Gauge()
    chart.add(title1,'',data)
    return chart
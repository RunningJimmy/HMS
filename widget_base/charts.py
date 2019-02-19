'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: charts.py
@time: 2019-2-15 16:16
@version：0.1
@desc: 图表，尝试WEB：pyecharts；客户端渲染：matplotlib、PyQtCharts
'''
from pyecharts import Bar,Pie,Gauge
from utils import str2

class Charts(object):

    def __init__(self,chart_type='Bar'):
        self.bar_obj = Bar()

    def add_chart(self,title:str,axis_x:list,axis_y:list,**kwargs):
        '''
        :param title: 标题
        :param axis_x: X轴 标签
        :param axis_y: Y轴 数据
        :return:
        '''
        self.bar_obj.add(title, axis_x, axis_y, is_more_utils=True, xaxis_rotate=90,**kwargs)

# 构建饼图
def build_chart_pie(filename,title,datas):
    axis_x = [str2(key) for key in datas.keys()]
    axis_y = list(datas.values())
    pie = Pie(title,width=400,height=200,title_pos = 'center')
    pie.add(
            '',axis_x,axis_y,           #''：图例名（不使用图例）
            radius = [25,55],           #环形内外圆的半径
            is_label_show = True,       #是否显示标签
            label_text_color = None,    #标签颜色
            legend_orient = 'vertical', #图例垂直
            legend_pos = 'left',
            is_more_utils=False
            )
    pie.render(filename)

# 构建仪表盘，用于展示百分率的
def build_chart_gauge(filename,title1:str,title2:str,data:float):
    pie = Gauge(width=400,height=200)
    pie.add(title1,title2,data)
    pie.render(filename)
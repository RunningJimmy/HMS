'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: operate_setup.py
@time: 2019-1-15 15:02
@desc:操作记录表
'''
from widgets.cwidget import *
from widgets import CRUDWidget
from .model import *

class OperateSetup(CRUDWidget):

    def __init__(self,parent=None):
        super(OperateSetup,self).__init__(parent)
        table_operate_cols = OrderedDict([
            ('czbh', "操作编号"),
            ('czdzd', "操作名称"),
            ('JSGS', "绩效系数"),
            ('YXBJ', "有效标记"),
            ('czdzd', "操作名称"),
            ('BZ', "备注"),
        ])
        table_operate = OperateTableWidget(table_operate_cols)
        self.setTable(table_operate_cols,table_operate,'操作记录')
        self.setTableModel(MT_TJ_CZJLWHB)
        #  初始化界面
        super(OperateSetup, self).initUI()
        # 绑定信号槽
        super(OperateSetup, self).initSignal()
        # 初始化数据
        self.on_btn_query_click()

class OperateTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(OperateTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                # if col_name=='':
                item = QTableWidgetItem(str(row_data[col_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        # self.setColumnWidth(0, 40)
        # self.setColumnWidth(1, 120)
        # self.setColumnWidth(2, 70)
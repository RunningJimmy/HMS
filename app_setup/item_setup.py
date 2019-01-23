'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: item_setup.py
@time: 2019-1-12 17:21
@desc: 项目维护
'''
from widgets.cwidget import *
from widgets import CRUDWidget
from .model import *


# 项目类型设置
class ItemTypeSetup(CRUDWidget):

    item_clicked = pyqtSignal(str)
    # 传递类别编码，唯一

    def __init__(self, parent=None):
        super(ItemTypeSetup, self).__init__(parent)
        table_item_type_cols = OrderedDict([
            ('LBBM', "编号"),
            ('LBMC', "类别名称"),
            ('XMLX', "项目类型")
        ])
        table_item_type = ItemTypeTableWidget(table_item_type_cols)
        self.setModelExtend({'XMLX':OrderedDict([('检查','1'),('检验','2'),('功能','3')])} )
        self.setTable(table_item_type_cols,table_item_type,'项目类别')
        self.setTableModel(MT_XMLB)
        #  初始化界面
        super(ItemTypeSetup, self).initUI()
        # 绑定信号槽
        super(ItemTypeSetup, self).initSignal()
        # 初始化数据
        self.on_btn_query_click()

    def on_table_item_click(self,QTableWidgetItem):
        self.item_clicked.emit(self.table.getItemValueOfKey(QTableWidgetItem.row(),'LBBM'))

# 项目设置：子项、组合项目
class ItemSetup(CRUDWidget):

    def __init__(self, parent=None):
        super(ItemSetup, self).__init__(parent)
        table_item_cols = OrderedDict([
            ('xmbh', "项目编号"),
            ('xmmc', "项目名称"),
            ('xmdw', "项目单位"),
            ('DJ', "项目单价"),
            ('CKSX', "参考上限"),
            ('CKXX', "参考下限"),
            # ('mrjg', "默认结果")
        ])
        table_item = ItemTableWidget(table_item_cols)
        self.setTable(table_item_cols,table_item,'项目明细')
        self.setTableModel(MT_TJ_XMDM)
        #  初始化界面
        super(ItemSetup, self).initUI()
        self.btn_citem = QPushButton('增加组合')
        self.add_btn(0,self.btn_citem)
        # 绑定信号槽
        super(ItemSetup, self).initSignal()
        # 初始化数据
        self.on_btn_query_click()

    # 表格数据刷新
    def on_table_refresh(self,lbbm:str):
        results = self.session.query(MT_TJ_XMDM).filter(MT_TJ_XMDM.LBBM==lbbm).order_by(MT_TJ_XMDM.XSHS,MT_TJ_XMDM.XSSX).all()
        self.table.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('项目明细(%s)' % self.table.rowCount())


# 项目、组合项目维护
class CItemWidget(QSplitter):

    def __init__(self,parent=None):
        super(CItemWidget,self).__init__(parent)

        # self.setWindowTitle('')
        # self.setWindowIcon(Icon(title))
        self.setOrientation(Qt.Horizontal)
        self.setChildrenCollapsible(True)
        #############添加控件########
        self.left_widget = ItemTypeSetup()
        self.right_widget = ItemSetup()
        self.addWidget(self.left_widget)
        self.addWidget(self.right_widget)
        #############布局#############
        self.setStretchFactor(0, 1)   #第一个参数代表控件序号，第二个参数0表示不可伸缩，非0可伸缩
        self.setStretchFactor(1, 3)
        # 联系信号槽
        self.left_widget.item_clicked.connect(self.right_widget.on_table_refresh)

class ItemTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(ItemTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                # 组合项目加粗
                if row_data.get('sfzh',None)=='1':
                    item.setFont(QFont("宋体",10,QFont.Bold))
                if col_index==1:
                    item.setTextAlignment(Qt.AlignLeft| Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 150)


class ItemTypeTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(ItemTypeTableWidget, self).__init__(heads, parent)
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

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 70)
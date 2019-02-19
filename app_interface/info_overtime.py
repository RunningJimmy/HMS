'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: info_supplier.py
@time: 2019-1-10 7:57
@desc: 加班信息
'''

from widgets.cwidget import *
from widgets import CRUD_UI
from .model import *

# 供应商联系表
class InfoOverTime(Widget):

    def __init__(self,parent=None):
        super(InfoOverTime,self).__init__(parent)
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()
        self.on_btn_search_click()

    def initSignal(self):
        self.table_overtime.doubleClicked.connect(self.on_table_overtime_dclick)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        # self.btn_delete.clicked.connect(self.on_btn_delete_click)
        self.btn_drop.clicked.connect(self.on_btn_drop_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('检索条件')
        # gp_top.setLayout(lt_top)
        ######
        lt_middle = HBoxLayout()
        self.gp_middle = GroupBox('值班(0)')
        self.table_overtime_cols = OrderedDict([
            ('OID', "ID"),
            ('ODate', "日期"),
            ('recorder', "值班人"),
            ('content', "值班交接"),
            ('content', "已调休？")
        ])
        self.table_overtime = OverTimeTableWidget(self.table_overtime_cols)
        lt_middle.addWidget(self.table_overtime)
        self.gp_middle.setLayout(lt_middle)
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_insert = QPushButton('新增')
        self.btn_update = QPushButton('修改')
        self.btn_drop = QPushButton('删除')
        lt_bottom.addStretch()
        lt_bottom.addWidget(self.btn_insert)
        lt_bottom.addWidget(self.btn_update)
        # lt_bottom.addWidget(self.btn_drop)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击修改
    def on_table_overtime_dclick(self,QModelIndex):
        self.on_btn_update_click()

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_OverTime).all()
        self.table_overtime.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('值班(%s)' %self.table_overtime.rowCount())

    # 增加
    def on_btn_insert_click(self):
        ui = CRUD_UI(self.table_overtime_cols,MT_TJ_OverTime,parent=self)
        ui.handle.emit({})
        ui.exec_()
        self.on_btn_search_click()

    # 修改
    def on_btn_update_click(self):
        if self.table_overtime.currentRow()==-1:
            mes_about(self,"请选择需要修改的数据！")
            return
        ui = CRUD_UI(self.table_overtime_cols, MT_TJ_OverTime, parent=self)
        ui.handle.emit(self.table_overtime.selectRow2Dict())
        ui.exec_()
        self.on_btn_search_click()

    # 删除
    def on_btn_drop_click(self):
        button = mes_warn(self, '您确认删除吗？')
        if button == QMessageBox.Yes:
            try:
                self.session.query(MT_TJ_OverTime).filter_by(**self.table_overtime.selectRow2Dict()).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self,"删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"删除失败，信息：%s" %e)

        self.on_btn_search_click()

class OverTimeTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(OverTimeTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                if col_index==len(heads)-1:
                    item.setTextAlignment(Qt.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignCenter)

                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.horizontalHeader().setStretchLastSection(True)
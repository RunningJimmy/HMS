'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: sms_template_setup.py
@time: 2019-1-10 16:57
@desc: 
'''
from widgets.cwidget import *
from widgets import CRUD_UI
from .model import *

# 短信模板设置
class SmsTemplateSetup(Widget):

    def __init__(self,parent=None):
        super(SmsTemplateSetup,self).__init__(parent)
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()
        self.on_btn_search_click()

    def initSignal(self):
        self.table_sms_template.doubleClicked.connect(self.on_table_sms_template_dclick)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        self.btn_test.clicked.connect(self.on_btn_test_click)
        self.btn_drop.clicked.connect(self.on_btn_drop_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('检索条件')
        # gp_top.setLayout(lt_top)
        ######
        lt_middle = QHBoxLayout()
        self.gp_middle = QGroupBox('短信模板(0)')
        self.table_sms_template_cols = OrderedDict([
            ('TID', "ID"),
            ('TNAME', "模板名称"),
            ('TXB', "性别"),
            ('YXBZ', "是否有效"),
            ('CONTENT', "模板内容"),
            ('BZ', "备注")

        ])
        # 扩展控件，用 QComboBox
        self.widget_extend = {'TXB':OrderedDict([('所有',None),('男','1'),('女','0')])}
        self.table_sms_template = SmsTemplateTableWidget(self.table_sms_template_cols)
        lt_middle.addWidget(self.table_sms_template)
        self.gp_middle.setLayout(lt_middle)
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_insert = QPushButton('新增')
        self.btn_update = QPushButton('修改')
        self.btn_drop = QPushButton('删除')
        self.btn_test = QPushButton('测试')
        lt_bottom.addStretch()
        lt_bottom.addWidget(self.btn_insert)
        lt_bottom.addWidget(self.btn_update)
        lt_bottom.addWidget(self.btn_drop)
        lt_bottom.addWidget(self.btn_test)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击修改
    def on_table_sms_template_dclick(self,QModelIndex):
        self.on_btn_update_click()

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_SMSTemplate2).all()
        self.table_sms_template.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('短信模板(%s)' %self.table_sms_template.rowCount())

    # 增加
    def on_btn_insert_click(self):
        if self.login_id!='BSSA':
            mes_about(self,"您不是管理员，无权操作！")
            return
        ui = CRUD_UI(self.table_sms_template_cols,MT_TJ_SMSTemplate2,self.widget_extend,self)
        ui.handle.emit({})
        ui.exec_()
        self.on_btn_search_click()

    # 修改
    def on_btn_update_click(self):
        if self.login_id!='BSSA':
            mes_about(self,"您不是管理员，无权操作！")
            return
        if self.table_sms_template.currentRow()==-1:
            mes_about(self,"请选择需要修改的数据！")
            return
        ui = CRUD_UI(self.table_sms_template_cols, MT_TJ_SMSTemplate2,self.widget_extend, self)
        ui.handle.emit(self.table_sms_template.selectRow2Dict())
        ui.exec_()
        self.on_btn_search_click()

    # 删除
    def on_btn_drop_click(self):
        if self.login_id!='BSSA':
            mes_about(self,"您不是管理员，无权操作！")
            return
        button = mes_warn(self, '您确认删除吗？')
        if button == QMessageBox.Yes:
            try:
                self.session.query(MT_TJ_SMSTemplate2).filter_by(**self.table_sms_template.selectRow2Dict('TID')).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self,"删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"删除失败，信息：%s" %e)


    # 短信测试
    def on_btn_test_click(self):
        pass


class SmsTemplateTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(SmsTemplateTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                if col_index>=len(self.heads)-2:
                    item.setTextAlignment(Qt.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 60)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setStretchLastSection(True)
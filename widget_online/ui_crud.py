'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: ui_crud.py
@time: 2019-2-20 13:37
@version：0.1
@desc: 
'''
from .common import *

# 增删改查窗口
class CRUDWidget(Widget):

    def __init__(self, parent=None):
        super(CRUDWidget, self).__init__(parent)
        self.extend_map = None

    # 设置表格
    def setTable(self, table_cols: dict,table: QTableWidget,table_title):
        '''
        :param table_cols: 表格列
        :param table_title: 表格标题
        :param table: 表格
        :return:
        '''
        self.table_cols = table_cols
        self.table_title = table_title
        self.table = table

    # 设置表格模型
    def setTableModel(self, model):
        '''
        :param model: BaseModel
        :return:
        '''
        self.model = model

    # 设置模型扩展，用于增删改查
    def setModelExtend(self, extend_map:dict):
        '''
        :param model: BaseModel
        :return:
        '''
        self.extend_map = extend_map

    # 绑定信号槽
    def initSignal(self):
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        self.btn_delete.clicked.connect(self.on_btn_delete_click)
        self.table.itemClicked.connect(self.on_table_item_click)
        self.table.itemDoubleClicked.connect(self.on_table_item_dclick)

    # 初始化 通用界面
    def initUI(self):
        lt_main = QVBoxLayout()
        # 筛选布局
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('筛选')
        self.le_search = QLineEdit()
        lt_top.addWidget(QLabel(''))
        lt_top.addWidget(self.le_search)
        gp_top.setLayout(lt_top)
        # 数据展示布局
        lt_middle = QHBoxLayout()
        lt_middle.setContentsMargins(0,10,0,0)
        self.gp_middle = QGroupBox()
        self.gp_middle.setFlat(True)
        self.gp_middle.setFont(QFont("宋体",10))
        lt_middle.addWidget(self.table)
        self.gp_middle.setLayout(lt_middle)
        # 功能区布局
        self.lt_bottom = QHBoxLayout()
        self.btn_insert = QPushButton("增加")
        self.btn_update = QPushButton("修改")
        self.btn_delete = QPushButton("删除")
        self.lt_bottom.addStretch()
        self.lt_bottom.insertWidget(1,self.btn_insert)
        self.lt_bottom.insertWidget(2,self.btn_update)
        self.lt_bottom.insertWidget(3,self.btn_delete)
        self.lt_bottom.addStretch()
        # 主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addLayout(self.lt_bottom)
        self.setLayout(lt_main)

    # 功能区增加按钮
    def add_btn(self,position:int,button:QPushButton):
        self.lt_bottom.insertWidget(position,button)

    # 单击
    def on_table_item_click(self,QTableWidgetItem):
        pass

    # 双击
    def on_table_item_dclick(self,QTableWidgetItem):
        pass

    # 查询
    def on_btn_query_click(self,**kwargs):
        if kwargs:
            results = self.session.query(self.model).filter_by(**kwargs).all()
        else:
            results = self.session.query(self.model).all()

        self.table.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('%s(%s)' %(self.table_title,self.table.rowCount()))

    # 增加
    def on_btn_insert_click(self):
        ui = CRUD_UI(self.table_cols, self.model, map_extend=self.extend_map, parent=self)
        ui.handle.emit({})
        ui.exec_()
        # self.on_btn_query_click()

    # 修改
    def on_btn_update_click(self):
        if self.table.currentRow() == -1:
            mes_about(self, "请选择需要修改的数据！")
            return
        ui = CRUD_UI(self.table_cols, self.model, map_extend=self.extend_map, parent=self)
        ui.handle.emit(self.table.selectRow2Dict())
        ui.exec_()
        # self.on_btn_query_click()

    # 删除
    def on_btn_delete_click(self):
        button = mes_warn(self, '您确认删除吗？')
        if button == QMessageBox.Yes:
            try:
                self.session.query(self.model).filter_by(**self.table.selectRow2Keys()).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self, "删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self, "删除失败，信息：%s" % e)

        # self.on_btn_query_click()

# 自动生成窗口界面，插入和更新功能
class CRUD_UI(Dialog):

    handle = pyqtSignal(dict)
    # 一行数据，字典，key-value,字典为空，则判断为插入动作，否则为更新动作

    def __init__(self,map:dict,model:object,map_extend=None,parent=None):
        '''
        :param map: 数据字典：OrderedDict([('yhid', "用户账户"),......,('bz', "备注信息")])
        :param model: 数据模型：BaseModel
        :param map_extend: 数据模型：扩展控件,用于生成非常规控件
        :param parent: 父窗口
        '''
        super(CRUD_UI,self).__init__(parent)
        self.data_map = map
        self.db_model = model
        self.map_extend = map_extend if map_extend else {}
        # 绑定列与控件
        self.data_widget_map = {}
        self.initDynamicUI()
        self.handle.connect(self.initData)
        self.btn_cancle.clicked.connect(self.close)
        self.btn_handle.clicked.connect(self.on_btn_handle_click)
        # 动作：插入/跟新
        self.handle_type = None

    # 增删改
    def on_btn_handle_click(self):
        if not self.handle_type:
            return
        sql_model_obj = SqlModelHandle(self.db_model, self.session, self.data_widget_map)
        state, mes = sql_model_obj.handle(self.handle_type)
        if state:
            mes_about(self,"保存成功！")
            self.close()
        else:
            mes_about(self,"保存失败，信息：%s" %mes)

    # 初始化界面
    def initDynamicUI(self):
        self.setMinimumWidth(400)
        lt_main = QFormLayout()
        lt_main.setVerticalSpacing(10)
        lt_main.setLabelAlignment(Qt.AlignRight)
        for col_name,col_mark in self.data_map.items():
            widget_obj = self.map_extend.get(col_name,None)
            if widget_obj:
                # widget = DynamicComboBox(values)
                widget = widget_obj()
            else:
                pytype,pylength,isnull,iskey,isauto = pyobj(self.db_model,col_name)
                if pytype:
                    widget = create_widget(pytype,pylength,isnull,iskey,isauto)
            # 绑定列与控件
            self.data_widget_map[col_name] = widget
            # 窗口添加控件
            lt_main.addRow(QLabel("%s：" %col_mark), widget)

        lt_btn = QHBoxLayout()
        self.btn_handle = QPushButton("保存")
        self.btn_cancle = QPushButton("取消")
        lt_btn.addStretch()
        lt_btn.addWidget(self.btn_handle)
        lt_btn.addSpacing(20)
        lt_btn.addWidget(self.btn_cancle)
        lt_btn.addStretch()
        lt_main.addRow(QLabel())
        lt_main.addRow(lt_btn)
        self.setLayout(lt_main)

    # 初始化数据
    def initData(self,data:dict):
        if data:
            self.handle_type = "update"
            title = "编辑"
        else:
            self.handle_type = "insert"
            title = "新增"
        # 设置数据
        self.setData(data)
        self.setWindowTitle(title)

    # 设置数据
    def setData(self,data:dict):
        for key,value in data.items():
            widget = self.data_widget_map.get(key,None)
            if widget:
                widget_set_value(widget,value)
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: hms(健康管理系统)
@file: info_asset.py
@time: 2019-1-4 14:09
@desc:设备资产管理：电脑/打印机/读卡器/路由器/服务器等
'''

from widgets.cwidget import *
from .model import *

# 设备资产
class InfoEquipAsset(Widget):

    def __init__(self,parent=None):
        super(InfoEquipAsset,self).__init__(parent)
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()

    def initSignal(self):
        self.table_asset.doubleClicked.connect(self.on_table_asset_dclick)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        self.btn_delete.clicked.connect(self.on_btn_delete_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('检索条件')
        # 设备类型
        self.cb_equip = QComboBox()
        self.cb_equip.addItems(['台式机','笔记本','一体机','平板','显示小屏','显示大屏','打印机','路由器','服务器','读卡器'])
        # 设备区域
        self.cb_area = QComboBox()
        self.cb_area.addItems(['明州体检','江东体检','医务室'])
        lt_top.addWidget(QLabel("资产类型："))
        lt_top.addWidget(self.cb_equip)
        lt_top.addSpacing(10)
        lt_top.addWidget(QLabel("院区："))
        lt_top.addWidget(self.cb_area)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        ######
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('资产(0)')
        self.table_asset_cols = OrderedDict([
            ('aid', ""),
            ('ename', "厂商"),
            ('etype', "类型"),
            ('earea', "场所"),
            ('use_date', "资产日期"),
            ('use_id', "资产编号"),
            ('use_place', "资产位置"),
            ('eip', "IP地址"),
            ('ehost', "主机名"),
            ('eport', "端口号"),
            ('bz', "备注"),
            ('sfbf', "是否报废")
        ])
        self.table_asset = AssetTableWidget(self.table_asset_cols)
        lt_middle.addWidget(self.table_asset)
        gp_middle.setLayout(lt_middle)
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_insert = QPushButton('新增')
        self.btn_update = QPushButton('修改')
        self.btn_delete = QPushButton('报废')
        lt_bottom.addStretch()
        lt_bottom.addWidget(self.btn_insert)
        lt_bottom.addWidget(self.btn_update)
        lt_bottom.addWidget(self.btn_delete)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击修改
    def on_table_asset_dclick(self,QModelIndex):
        self.on_btn_update_click()

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_ASSET).all()
        self.table_asset.load([result.to_dict() for result in results])
        self.gp_middle_left.setTitle('用户(%s)' %self.table_asset.rowCount())

    # 增加
    def on_btn_insert_click(self):
        ui = AssetHandleDialog(self)
        ui.handle.emit({})
        ui.exec_()
        self.on_btn_search_click()

    # 修改
    def on_btn_update_click(self):
        if self.table_asset.currentRow()==-1:
            mes_about(self,"请选择需要修改的数据！")
            return
        ui = AssetHandleDialog(self)
        ui.handle.emit(self.table_asset.selectRow2Dict())
        ui.exec_()
        self.on_btn_search_click()

    # 删除
    def on_btn_delete_click(self):
        if self.table_dwmc.count()>0:
            mes_about(self,"请先清空该用户的授权单位信息！")
            return
        button = mes_warn(self, '您确认删除此用户吗？')
        if button == QMessageBox.Yes:
            try:
                self.session.query(MT_TJ_ASSET).filter_by(**self.table_asset.selectRow2Dict()).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self,"删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"删除失败，信息：%s" %e)

#
class AssetHandleDialog(Dialog):
    # 模型数据，根据是否为空判断是INSERT还是UPDATE
    handle = pyqtSignal(dict)

    def __init__(self,parent=None):
        super(AssetHandleDialog,self).__init__(parent)
        self.initUI()
        self.setDataWidgetMapper()
        self.handle.connect(self.initData)
        self.btn_cancle.clicked.connect(self.close)
        self.btn_handle.clicked.connect(self.on_btn_handle_click)
        self.handle_type = None

    # 设置控件与模型进行映射
    def setDataWidgetMapper(self):
        self.data_widget_map = {
            ('aid', ""),
            ('ename', "厂商"),
            ('etype', "类型"),
            ('earea', "院区"),
            ('use_date', "资产日期"),
            ('use_id', "资产编号"),
            ('use_place', "资产位置"),
            ('eip', "IP地址"),
            ('ehost', "主机名"),
            ('eport', "端口号"),
            ('bz', "备注"),
            ('sfbf', "是否报废")
        }
        self.sql_model_obj = SqlModelHandle(MT_TJ_ASSET,self.session,self.data_widget_map)

    # 增删改
    def on_btn_handle_click(self):
        if not self.handle_type:
            return
        state, mes = self.sql_model_obj.handle(self.handle_type)
        if state:
            mes_about(self,"保存成功！")
            self.close()
        else:
            mes_about(self,"保存失败，信息：%s" %mes)

    # 初始化界面
    def initUI(self):
        lt_main = QFormLayout()
        self.le_ename = QLineEdit()
        self.le_etype = QLineEdit()
        self.le_earea = QLineEdit()
        self.use_date = QDateEdit(QDate.currentDate())
        self.use_date.setCalendarPopup(True)
        self.use_date.setDisplayFormat("yyyy-MM-dd")
        self.le_use_id = QLineEdit()
        self.le_use_place = QLineEdit()
        self.le_eip = QLineEdit()
        self.le_ehost = QLineEdit()
        self.le_eport = QLineEdit()
        self.pt_bz = QPlainTextEdit()
        lt_btn = QHBoxLayout()
        self.btn_handle = QPushButton("保存")
        self.btn_cancle = QPushButton("取消")
        lt_btn.addStretch()
        lt_btn.addWidget(self.btn_handle)
        lt_btn.addWidget(self.btn_cancle)
        lt_btn.addStretch()
        # 添加布局
        lt_main.addRow("账户：",self.le_user_id)
        lt_main.addRow("名称：", self.le_user_name)
        lt_main.addRow("密码：", self.le_user_pwd)
        lt_main.addRow(self.cb_active,QLabel("有效"))
        lt_main.addRow("备注：", self.pt_bz)
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

class AssetTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(AssetTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)




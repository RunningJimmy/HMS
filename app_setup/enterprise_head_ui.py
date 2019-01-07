'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: hms(健康管理系统)
@file: enterprise_head_ui.py
@time: 2019-1-2 9:09
@desc:企业负责人增删改查，主要用于招工电子报告下载用
'''
from widgets.cwidget import *
from app_setup.model import *

# 招工电子报告后台设置，人员和单位
class EnterpriseHeadUI(CenterWidget):

    status = False

    def __init__(self,parent=None):
        super(EnterpriseHeadUI,self).__init__(parent)
        self.setWindowTitle('招工电子报告下载->权限设置')
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()
        # 初始化数据
        dwmc_bh = OrderedDict()
        dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            dwmc_bh[result.dwbh] = str2(result.mc)
            dwmc_py[result.pyjm.lower()] = str2(result.mc)
        self.le_dwmc_search.setBhs(dwmc_bh)
        self.le_dwmc_search.setPys(dwmc_py)
        # 初始化用户
        self.on_btn_search_click()
        self.cur_yhid = None

    def initSignal(self):
        self.table_dwmc.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_dwmc.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.table_user.doubleClicked.connect(self.on_table_user_dclick)
        self.table_user.itemClicked.connect(self.on_table_user_click)
        self.btn_search.clicked.connect(self.on_btn_search_click)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        self.btn_delete.clicked.connect(self.on_btn_delete_click)
        self.le_dwmc_search.added.connect(self.on_table_dwmc_add)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        # 上 左
        lt_top_left = QHBoxLayout()
        gp_top_left = QGroupBox('检索用户')
        self.le_user_search = QLineEdit()
        self.btn_search = QPushButton("查询")
        lt_top_left.addWidget(self.le_user_search)
        lt_top_left.addWidget(self.btn_search)
        lt_top_left.addStretch()
        gp_top_left.setLayout(lt_top_left)
        # 上 右
        lt_top_right = QHBoxLayout()
        gp_top_right = QGroupBox('检索单位')
        self.le_dwmc_search = TUint({},{})
        lt_top_right.addWidget(self.le_dwmc_search)
        lt_top_right.addStretch()
        gp_top_right.setLayout(lt_top_right)
        # 添加上布局
        lt_top.addWidget(gp_top_left)
        lt_top.addWidget(gp_top_right)
        #######################################
        lt_middle = QHBoxLayout()
        lt_middle_left = QHBoxLayout()
        lt_middle_right = QHBoxLayout()
        self.gp_middle_left = QGroupBox('用户(0)')
        self.gp_middle_right = QGroupBox('授权单位(0)')
        self.table_user_cols = OrderedDict([
            ('yhid', "用户账户"),
            ('yhmc', "用户名称"),
            ('yhmm', "用户密码"),
            ('yxbz', "是否有效"),
            ('bz', "备注信息")
        ])
        self.table_user = UserTableWidget(self.table_user_cols)
        self.table_dwmc = QListWidget()
        lt_middle_left.addWidget(self.table_user)
        lt_middle_right.addWidget(self.table_dwmc)
        self.gp_middle_left.setLayout(lt_middle_left)
        self.gp_middle_right.setLayout(lt_middle_right)
        lt_middle.addWidget(self.gp_middle_left)
        lt_middle.addWidget(self.gp_middle_right)
        lt_bottom = QHBoxLayout()
        lt_bottom_left = QHBoxLayout()
        gp_bottom_left = QGroupBox()
        self.btn_insert = QPushButton('新增')
        self.btn_update = QPushButton('修改')
        self.btn_delete = QPushButton('删除')
        lt_bottom_left.addStretch()
        lt_bottom_left.addWidget(self.btn_insert)
        lt_bottom_left.addWidget(self.btn_update)
        lt_bottom_left.addWidget(self.btn_delete)
        lt_bottom_left.addStretch()
        gp_bottom_left.setLayout(lt_bottom_left)
        lt_bottom.addWidget(gp_bottom_left)
        lt_bottom.addStretch()
        # 添加主布局
        lt_main.addLayout(lt_top)
        lt_main.addLayout(lt_middle)
        lt_main.addLayout(lt_bottom)
        self.setLayout(lt_main)

    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_dwmc.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

            menu = QMenu()
            item_drop = menu.addAction(Icon("删除"), "删除")
            action = menu.exec_(self.table_dwmc.mapToGlobal(pos))
            # 获取变量
            item = self.table_dwmc.currentItem()
            # 删除
            if action == item_drop:
                button = mes_warn(self, '您确认取消当前用户下载该单位电子报告的授权吗？')
                if button == QMessageBox.Yes:
                    result = self.session.query(MT_TJ_DW).filter(MT_TJ_DW.mc == item.text()).scalar()
                    self.session.query(MT_TJ_DWFZRSQ).filter(MT_TJ_DWFZRSQ.yhid == self.cur_yhid,MT_TJ_DWFZRSQ.dwbh==result.dwbh).delete()
                    try:
                        self.session.commit()
                        # 更新UI
                        self.table_dwmc.takeItem(self.table_dwmc.currentRow())
                        mes_about(self,"删除成功！")

                    except Exception as e:
                        self.session.rollback()
                        mes_about(self,"删除失败，信息：%s" %e)

    # 双击修改
    def on_table_user_dclick(self,QModelIndex):
        self.on_btn_update_click()
        # ui = UserHandleDialog(self)
        # ui.handle.emit(self.table_user.selectRow2Dict())
        # ui.exec_()
        # self.on_btn_search_click()

    # 单行选择
    def on_table_user_click(self):
        self.cur_yhid = self.table_user.getCurItemValueOfKey('yhid')
        results = self.session.query(MT_TJ_DW).\
            filter(MT_TJ_DW.dwbh == MT_TJ_DWFZRSQ.dwbh).\
            filter(MT_TJ_DWFZRSQ.yhid == self.cur_yhid ).all()
        self.table_dwmc.clear()
        self.table_dwmc.addItems([str2(result.mc) for result in results])
        self.gp_middle_right.setTitle('授权单位(%s)' %self.table_dwmc.count())

    # 添加元素
    def on_table_dwmc_add(self,dwmc:str,dwbh:str):
        if self.table_user.currentRow()==-1:
            mes_about(self,"请选择要添加的用户")
            return
        # 更新数据库
        obj = MT_TJ_DWFZRSQ()
        obj.yhid = self.cur_yhid
        obj.dwbh = dwbh
        self.session.add(obj)
        try:
            self.session.commit()
            # 更新UI
            self.table_dwmc.addItem(dwmc)
        except Exception as e:
            self.session.rollback()
        self.le_dwmc_search.setText('')

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_DWFZR).all()
        self.table_user.load([result.to_dict() for result in results])
        self.gp_middle_left.setTitle('用户(%s)' %self.table_user.rowCount())

    # 增加
    def on_btn_insert_click(self):
        ui = UserHandleDialog(self)
        ui.handle.emit({})
        ui.exec_()
        self.on_btn_search_click()

    # 修改
    def on_btn_update_click(self):
        if self.table_user.currentRow()==-1:
            mes_about(self,"请选择需要修改的数据！")
            return
        ui = UserHandleDialog(self)
        ui.handle.emit(self.table_user.selectRow2Dict())
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
                self.session.query(MT_TJ_DWFZR).filter_by(**self.table_user.selectRow2Dict()).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self,"删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"删除失败，信息：%s" %e)

#
class UserHandleDialog(Dialog):

    handle = pyqtSignal(dict)
    # '''
    # :param: 模型数据，根据是否为空判断是INSERT还是UPDATE
    # '''

    def __init__(self,parent=None):
        super(UserHandleDialog,self).__init__(parent)
        self.initUI()
        self.setDataWidgetMapper()
        self.handle.connect(self.initData)
        self.btn_cancle.clicked.connect(self.close)
        self.btn_handle.clicked.connect(self.on_btn_handle_click)
        self.handle_type = None

    # 设置控件与模型进行映射
    def setDataWidgetMapper(self):
        self.data_widget_map = {
            'yhid':self.le_user_id,
            'yhmc': self.le_user_name,
            'yhmm': self.le_user_pwd,
            'yxbz': self.cb_active,
            'bz': self.pt_bz,
        }
        self.sql_model_obj = SqlModelHandle(MT_TJ_DWFZR,self.session,self.data_widget_map)

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
        self.le_user_id = QLineEdit()
        self.le_user_name = QLineEdit()
        self.le_user_pwd = QLineEdit()
        self.cb_active = QCheckBox()
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


class UserTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(UserTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = EnterpriseHeadUI()
    ui.show()
    app.exec_()
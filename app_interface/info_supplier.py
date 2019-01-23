'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: info_supplier.py
@time: 2019-1-10 7:57
@desc: 供应商联系表
'''
from widgets.cwidget import *
from widgets import CRUD_UI
from .model import *

# 供应商联系表
class InfoSupplier(Widget):

    def __init__(self,parent=None):
        super(InfoSupplier,self).__init__(parent)
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()
        self.on_btn_search_click()

    def initSignal(self):
        self.table_supplier.doubleClicked.connect(self.on_table_supplier_dclick)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)
        self.btn_update.clicked.connect(self.on_btn_update_click)
        # self.btn_delete.clicked.connect(self.on_btn_delete_click)
        self.btn_drop.clicked.connect(self.on_btn_drop_click)
        self.table_supplier.itemClicked.connect(self.on_table_supplier_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('检索条件')
        # gp_top.setLayout(lt_top)
        ######
        lt_middle = HBoxLayout()
        self.gp_middle = GroupBox('供应商(0)')
        self.table_supplier_cols = OrderedDict([
            ('SID', "ID"),
            ('Ename', "公司名"),
            ('Product', "产品"),
            ('Contactor', "联系人"),
            ('ContactWay', "联系方式"),
            ('Doc', "接口文档"),
            ('BZ', "备注"),
        ])
        self.table_supplier = SupplierTableWidget(self.table_supplier_cols)
        lt_middle.addWidget(self.table_supplier)
        self.gp_middle.setLayout(lt_middle)
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_insert = QPushButton('新增')
        self.btn_update = QPushButton('修改')
        self.btn_drop = QPushButton('删除')
        lt_bottom.addStretch()
        lt_bottom.addWidget(self.btn_insert)
        lt_bottom.addWidget(self.btn_update)
        lt_bottom.addWidget(self.btn_drop)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击修改
    def on_table_supplier_dclick(self,QModelIndex):
        self.on_btn_update_click()

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_Supplier).all()
        self.table_supplier.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('供应商(%s)' %self.table_supplier.rowCount())

    # 增加
    def on_btn_insert_click(self):
        ui = CRUD_UI(self.table_supplier_cols,MT_TJ_Supplier,parent=self)
        ui.handle.emit({})
        ui.exec_()
        self.on_btn_search_click()

    # 修改
    def on_btn_update_click(self):
        if self.table_supplier.currentRow()==-1:
            mes_about(self,"请选择需要修改的数据！")
            return
        ui = CRUD_UI(self.table_supplier_cols, MT_TJ_Supplier, parent=self)
        ui.handle.emit(self.table_supplier.selectRow2Dict())
        ui.exec_()
        self.on_btn_search_click()

    # 删除
    def on_btn_drop_click(self):
        button = mes_warn(self, '您确认删除吗？')
        if button == QMessageBox.Yes:
            try:
                self.session.query(MT_TJ_Supplier).filter_by(**self.table_supplier.selectRow2Dict('SID')).delete()
                self.session.commit()
                self.on_btn_search_click()
                mes_about(self,"删除成功！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"删除失败，信息：%s" %e)

        self.on_btn_search_click()

    # 单击
    def on_table_supplier_click(self,QTableWidgetItem):
        if QTableWidgetItem.text()=='下载':
            fileName, _ = QFileDialog.getSaveFileName(self, "保存文件", desktop(), "Excel 2007 Files (*.zip)",
                                                      options=QFileDialog.DontUseNativeDialog)
            if fileName:
                result = self.session.query(MT_TJ_Supplier).filter(MT_TJ_Supplier.SID==self.table_supplier.getItemValueOfKey(QTableWidgetItem.row(),'SID')).scalar()
                with open("%s.zip" %fileName,"wb") as f:
                    f.write(result.Doc)

                mes_about(self,"下载成功！")


class SupplierTableWidget(TableWidget):

    def __init__(self, heads, parent=None):
        super(SupplierTableWidget, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                if col_index== len(self.heads)-1:
                    item.setTextAlignment(Qt.AlignLeft)

                elif col_index==len(self.heads)-2:
                    if row_data[col_name]:
                        item = QTableWidgetItem('下载')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)


        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 70)
        # self.resizeColumnToContents(len(self.heads)-1)
        self.horizontalHeader().setStretchLastSection(True)
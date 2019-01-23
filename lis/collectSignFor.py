from widgets.cwidget import *
from lis.model import *
from utils.api import api_file_down

# 签收界面
class CollectSignFor_UI(Widget):

    def __init__(self):
        super(CollectSignFor_UI,self).__init__()
        self.initUI()

    # 初始化界面
    def initUI(self):
        lt_main = QVBoxLayout()                    # 主布局
        lt_top = QHBoxLayout()                     # 上布局
        lt_bottom = HBoxLayout()                  # 下布局
        self.gp_bottom = GroupBox('签收数量(0)')
        ############ 上布局 ########################
        self.lb_serialno = QSerialNo()
        lt_top.addWidget(self.lb_serialno)
        lt_top.addStretch()
        ############ 下布局 ########################
        self.collect_cols = OrderedDict([
                                ("ck", ""),
                                ("zt", '状态'),
                                ("jllx", "类型"),
                                ("tjbh", "体检编号"),
                                ("tmbh", "条码号"),
                                ("czxm", "采集人员"),
                                ("czsj", "采集时间"),
                                ("czqy", "采集区域"),
                                ("jjxm", "交接护士"),
                                ("jjsj", "交接时间"),
                                ("sjfs", "封盘条码"),
                                ("jsxm", "签收人员"),
                                ("jssj", "签收时间"),
                                ("tmxm", "条码项目")
                            ])
        self.table_signfor = CollectSignForTable(self.collect_cols)
        # 设置列宽
        self.table_signfor.setColumnWidth(0, 40)
        self.table_signfor.setColumnWidth(5, 150)
        lt_bottom.addWidget(self.table_signfor)
        self.gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addLayout(lt_top)
        lt_main.addWidget(self.gp_bottom)
        self.setLayout(lt_main)

class CollectSignFor(CollectSignFor_UI):

    def __init__(self):

        super(CollectSignFor,self).__init__()
        self.initParas()
        self.lb_serialno.returnPressed.connect(self.on_lb_serialno_press)
        self.table_signfor.itemClicked.connect(self.on_table_signfor_show)
        # 查看采血图片 UI
        self.pic_ui = None

    def initParas(self):
        if self.get_gol_para('api_file_down'):
            self.show_url = self.get_gol_para('api_file_down')
        else:
            self.show_url = 'http://10.8.200.201:4000/app_api/file/down/%s/%s'

    # 查询
    def on_lb_serialno_press(self):
        results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.sjfs==self.lb_serialno.text()).all()
        self.table_signfor.load([result.to_dict for result in results])
        self.gp_bottom.setTitle('签收数量(%s)' %self.table_signfor.rowCount())
        button = mes_warn(self, '当前数量：%s 您确定签收吗？' %self.table_signfor.rowCount())
        if button == QMessageBox.Yes:
            result = self.session.query(distinct(MT_TJ_CZJLB.jsxm)).filter(MT_TJ_CZJLB.sjfs == self.lb_serialno.text()).scalar()
            if result:
                pass
            else:
                operate_time = cur_datetime()
                try:
                    self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.sjfs == self.lb_serialno.text()).update({
                        MT_TJ_CZJLB.jssj: operate_time,
                        MT_TJ_CZJLB.jsxm: self.login_name,
                    })
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    mes_about(self,"签收失败，错误信息：%s" %e)
                    return
            results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.sjfs == self.lb_serialno.text()).all()
            self.table_signfor.load([result.to_dict for result in results])
            self.lb_serialno.setText('')
        # mes_about(self, '共检索出 %s 条数据！' % self.table_signfor.rowCount())

    # 设置文本 和查看 照片
    def on_table_signfor_show(self,QTableWidgetItem):
        btn_name = QTableWidgetItem.text()
        if btn_name=='查看':
            url = self.show_url %(self.table_signfor.getItemValueOfKey(QTableWidgetItem.row(),'tjbh'),'000001')
            data = api_file_down(url)
            if data:
                if not self.pic_ui:
                    self.pic_ui = PicDialog()
                self.pic_ui.setData(data)
                self.pic_ui.show()
            else:
                mes_about(self,'该人未拍照！')

# 抽血历史采集筛选列表
class CollectSignForTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectSignForTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):

        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                data = row_data.get(col_name,'')
                if col_name=='ck':
                    item = QTableWidgetItem('查看')
                    font = QFont()
                    font.setBold(True)
                    font.setWeight(75)
                    item.setFont(font)
                    item.setBackground(QColor(218,218,218))
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
                    item.setTextAlignment(Qt.AlignCenter)
                elif col_index==len(heads)-1:
                    item = QTableWidgetItem(data)
                else:
                    item = QTableWidgetItem(data)
                    item.setTextAlignment(Qt.AlignCenter)


                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 40)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 80)
        self.setColumnWidth(5, 70)
        self.horizontalHeader().setStretchLastSection(True)
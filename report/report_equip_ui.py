from widgets.cwidget import *
from widgets.utils import CefWidget

class ReportEquipUI(Widget):

    def __init__(self,parent=None):
        super(ReportEquipUI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_left = QVBoxLayout()
        self.btn_query = ToolButton(Icon('query'), '查询')
        self.gp_where_search = BaseCondiSearchGroup(1)
        self.gp_where_search.setNoChoice()
        # 报告状态
        self.cb_report_state = ReportStateGroup()
        self.cb_report_state.addStates(['所有','未审核','已审核'])
        self.cb_equip_type = EquipTypeLayout()
        self.cb_equip_type.set_equip_type(EquipName.get(str(gol.get_value('equip_type','00')).zfill(2)))
        self.cb_user = UserGroup('检查医生：')
        self.cb_user.addUsers(['所有',self.login_name])
        # 区域
        self.cb_area = AreaGroup()
        self.gp_where_search.addItem(self.cb_area, 0, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_report_state, 1, 3, 1, 2)
        self.gp_where_search.addItem(self.cb_user, 0, 5, 1, 2)
        self.gp_where_search.addItem(self.cb_equip_type, 1, 5, 1, 2)
        # 按钮
        self.gp_where_search.addWidget(self.btn_query, 0, 7, 2, 2)
        self.gp_quick_search = QuickSearchGroup()
        self.gp_quick_search.setLabelDisable('sfzh')
        self.gp_quick_search.setLabelDisable('sjhm')
        self.table_report_equip_cols = OrderedDict([
            ('xmzt', '状态'),
            ('cname', '设备名称'),
            ('tjbh', '体检编号'),
            ('xm', '姓名'),
            ('xb', '性别'),
            ('nl', '年龄'),
            ('tjqy', '体检区域'),
            ('bgrq', '报告日期'),
            ('bgys', '报告医生'),
            ('jcrq','检查日期'),
            ('jcys','检查医生'),
            ('jcqy', '检查房间'),
            ('dwmc', '单位名称'),
            ('xmzd', '项目诊断'),
            ('fpath', '文件路径')
        ])
        # 待审阅列表
        self.table_report_equip = ReportEquipTable(self.table_report_equip_cols)
        self.gp_table = QGroupBox('检查列表（0）')
        lt_table = QHBoxLayout()
        lt_table.addWidget(self.table_report_equip)
        self.gp_table.setLayout(lt_table)
        # 审阅信息
        self.gp_review_user = ReportEquipUser()
        # 添加布局
        lt_left.addWidget(self.gp_where_search,1)
        lt_left.addWidget(self.gp_quick_search,1)
        lt_left.addWidget(self.gp_table,7)
        lt_left.addWidget(self.gp_review_user,1)

        ####################右侧布局#####################
        # self.wv_report_equip = WebView()
        self.wv_report_equip = CefWidget(self)
        lt_right = QHBoxLayout()
        lt_right.addWidget(self.wv_report_equip)
        self.gp_right = QGroupBox('报告预览')
        self.gp_right.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0,128,0);''')
        self.gp_right.setLayout(lt_right)
        lt_main.addLayout(lt_left,1)
        lt_main.addWidget(self.gp_right,2)

        self.setLayout(lt_main)

class ReportEquipUser(QGroupBox):

    # 自定义 信号，封装对外使用
    btnClick = pyqtSignal(bool,str)  # 审核/取消状态  结果内容
    btnSet = pyqtSignal()
    dataChanged = pyqtSignal(str,str,str,str,str,str)

    def __init__(self):
        super(ReportEquipUser,self).__init__()
        self.initUI()
        self.btn_audit.clicked.connect(self.on_btn_audit_click)
        self.btn_describe.clicked.connect(self.btnSet)
        self.dataChanged.connect(self.setData)

    def initUI(self):
        self.setTitle('审核信息')
        lt_main = QGridLayout()
        self.lb_jcys = AuditLabel()
        self.lb_jcrq = AuditLabel()
        self.lb_bgys = AuditLabel()
        self.lb_bgrq = AuditLabel()
        self.lb_xmzd = QPlainTextEdit()
        self.lb_xmzd.setStyleSheet('''font: 75 12pt '微软雅黑';height:20px;''')
        self.btn_audit = ToolButton(Icon('样本签收'),'取消审核')
        self.btn_describe = ToolButton(Icon('临床检查'), '常用结论')
        ###################基本信息  第一行##################################
        lt_main.addWidget(QLabel('检查：'), 0, 0, 1, 1)
        lt_main.addWidget(self.lb_jcys, 0, 1, 1, 1)
        lt_main.addWidget(QLabel('时间：'), 1, 0, 1, 1)
        lt_main.addWidget(self.lb_jcrq, 1, 1, 1, 1)
        lt_main.addWidget(QLabel('报告：'), 0, 2, 1, 1)
        lt_main.addWidget(self.lb_bgys, 0, 3, 1, 1)
        lt_main.addWidget(QLabel('时间：'), 1, 2, 1, 1)
        lt_main.addWidget(self.lb_bgrq, 1, 3, 1, 1)
        # 按钮
        lt_main.addWidget(self.btn_audit, 0, 9, 2, 2)
        lt_main.addWidget(self.btn_describe, 0, 11, 2, 2)
        ###################基本信息  第二行##################################
        # lt_main.addWidget(QLabel('审阅备注：'), 0, 2, 2, 2)
        lt_main.addWidget(self.lb_xmzd, 0, 4, 2, 5)

        lt_main.setHorizontalSpacing(5)            #设置水平间距
        lt_main.setVerticalSpacing(5)              #设置垂直间距
        lt_main.setContentsMargins(5, 5, 5, 5)  #设置外间距
        lt_main.setColumnStretch(6, 1)             #设置列宽，添加空白项的
        self.setLayout(lt_main)
        # 状态标签
        self.lb_audit_bz = StateLable(self)
        self.lb_audit_bz.show()

    # 清空数据
    def clearData(self):
        self.lb_jcys.setText('')
        self.lb_jcrq.setText('')
        self.lb_bgys.setText('')
        self.lb_bgrq.setText('')
        self.lb_xmzd.setPlainText('')
        self.lb_audit_bz.show2(False)

    # 设置数据
    def setData(self,xmzt,jcys,jcrq,bgys,bgrq,xmzd):
        self.clearData()
        if xmzt=='已小结':
            self.lb_audit_bz.show2()
            self.btn_audit.setText('取消审核')
            self.lb_xmzd.setDisabled(True)
        else:
            self.lb_audit_bz.show2(False)
            self.btn_audit.setText('完成审核')
            self.lb_xmzd.setDisabled(False)

        self.lb_jcys.setText(jcys)
        self.lb_jcrq.setText(jcrq)
        self.lb_bgys.setText(bgys)
        self.lb_bgrq.setText(bgrq)
        self.lb_xmzd.setPlainText(xmzd)

    # 状态变更
    def statechange(self,bgys='',bgrq=''):
        # 从完成审阅 -> 取消审阅
        if '完成审核' in self.btn_audit.text():
            self.btn_audit.setText('取消审核')
            self.lb_audit_bz.show2()
        else:
            self.btn_audit.setText('完成审核')
            self.lb_audit_bz.show2(False)
        # 刷新
        self.lb_bgrq.setText(bgrq)
        self.lb_bgys.setText(bgys)

    # 获取审阅备注信息
    def get_sybz(self):
        return self.lb_xmzd.toPlainText()

    def set_describe(self,describe:str):
        if self.lb_xmzd.isEnabled():
            self.lb_xmzd.setPlainText(describe)

    # 按钮点击
    def on_btn_audit_click(self):
        if '完成审核' in self.btn_audit.text():
            if not self.lb_xmzd.toPlainText():
                mes_about(self, '请输入项目诊断意见！')
                return
            shzt = True
            self.btnClick.emit(shzt, self.lb_xmzd.toPlainText())
        else:
            text, ok = QInputDialog.getText(self, '明州体检', '请输入取消审核原因：', QLineEdit.Normal, '')
            if ok and text:
                shzt = False
                self.btnClick.emit(shzt,text)

class AuditLabel(QLabel):

    def __init__(self,p_str=None,parent=None):
        super(AuditLabel,self).__init__(p_str,parent)
        self.setStyleSheet('''border: 1px solid;font: 75 12pt \"微软雅黑\";''')
        self.setMinimumWidth(80)

class StateLable(QLabel):

    def __init__(self,parent):
        super(StateLable,self).__init__(parent)
        self.setMinimumSize(200,200)
        self.setGeometry(200,-60,100,100)
        self.setStyleSheet('''font: 75 28pt "微软雅黑";color: rgb(255, 0, 0);''')
        self.setAttribute(Qt.WA_TranslucentBackground)                               #背景透明
        self.data = open(file_ico('已审核.png'),'rb').read()

    def show2(self,flag = True):
        if flag:
            p = QPixmap()
            p.loadFromData(self.data)
            self.setPixmap(p)
        else:
            self.clear()


# 设备信息
EquipName={
    '01':'电测听',
    '02':'人体成分(投放)',
    '03':'人体成分',
    '04':'骨密度',
    '05':'超声骨密度',
    '06':'动脉硬化',
    '07':'大便隐血',
    '08':'心电图',
    '11':'肺功能',
    '12':'胸部正位'
}

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ReportEquipUI()
    ui.show()
    app.exec_()
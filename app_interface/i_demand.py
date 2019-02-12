from widgets.cwidget import *
from widgets.richText import RichTextWidget
from utils import cur_date,cur_datetime
from .model import *

# 需求管理
# 1、提交：提交人、提交时间、提交内容、期望完成时间
# 2、审核：审核人：需求管理员、指定审批人员、开发人员、跟踪人员、系统及模块
# --取消此节点  3、审批：审批人（业务领导）、审批时间、评估价值、紧急程度、保争拒弃
# 4、开发：开发人、解决方案、评估周期
# 5、跟踪：跟踪人、使用情况
# 6、验收评价：确认人、交付物（签字）
class DemandManger(Widget):

    status = False

    def __init__(self,parent=None):
        super(DemandManger,self).__init__(parent)
        self.initUI()
        # 添加信号槽
        self.table_demand.itemClicked.connect(self.on_table_demand_click)
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_xqtj.clicked.connect(self.on_btn_xqtj_click)
        self.btn_xqsh.clicked.connect(self.on_btn_xqsh_click)
        self.btn_xqsp.clicked.connect(self.on_btn_xqsp_click)
        self.btn_kfqr.clicked.connect(self.on_btn_kfqr_click)
        self.btn_csgz.clicked.connect(self.on_btn_csgz_click)
        self.btn_yspj.clicked.connect(self.on_btn_yspj_click)
        # 特殊变量
        self.cur_id = None
        self.cur_state = None
        self.cur_name = None

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_main_left = QVBoxLayout()
        lt_main_right = QVBoxLayout()
        # 左上布局
        lt_left_top = QHBoxLayout()
        gp_left_top = QGroupBox('条件检索')
        self.state = OrderedDict([
            ('所有',None),
            ('已提交','0'),
            ('已审核','1'),
            ('开发中','2'),
            ('跟踪','3'),
            ('已验收','4')
        ])
        self.cb_state = QComboBox()
        self.cb_state.addItems(list(self.state.keys()))
        self.de_start = QDateEdit(QDate.currentDate())
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        self.btn_query = QPushButton(Icon('query'), '查询')
        self.btn_print = QPushButton(Icon('print'), '打印')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_left_top.addWidget(QLabel('需求状态：'))
        lt_left_top.addWidget(self.cb_state)
        lt_left_top.addWidget(QLabel('时间：'))
        lt_left_top.addWidget(self.de_start)
        lt_left_top.addWidget(QLabel('-'))
        lt_left_top.addWidget(self.de_end)
        lt_left_top.addWidget(Line())
        lt_left_top.addWidget(self.btn_query)
        lt_left_top.addWidget(self.btn_print)
        lt_left_top.addWidget(self.btn_export)
        lt_left_top.addStretch()
        gp_left_top.setLayout(lt_left_top)
        # 左中布局
        lt_left_middle = HBoxLayout()
        self.gp_left_middle = GroupBox('需求列表(0)')
        self.table_demand_cols = OrderedDict([('state', '状态'),
                                              ('dname', '需求名称'),
                                              ('submiter', '需求人'),
                                              ('submit_time', '提交时间'),
                                              ('shxm', '审核人'),
                                              ('shsj', '审核时间'),
                                              ('spxm', '审批人'),
                                              ('spsj', '审批时间'),
                                              ('kfxm', '开发人'),
                                              ('kfsj', '开发时间'),
                                              ('gzxm', '跟踪人'),
                                              ('gzsj', '跟踪时间'),
                                              ('ysxm', '验收人'),
                                              ('yssj', '验收时间'),
                                              ('did', '需求ID')
                                            ])
        self.table_demand = DemandTable(self.table_demand_cols)
        lt_left_middle.addWidget(self.table_demand)
        self.gp_left_middle.setLayout(lt_left_middle)
        #############################################################
        lt_btns = QHBoxLayout()
        gp_btns = QGroupBox()
        self.btn_xqtj = QPushButton(Icon('submit'), '需求提交')
        self.btn_xqsh = QPushButton(Icon('submit'), '需求审核')
        # self.btn_xqsp = QPushButton(Icon('submit'), '需求审批')
        self.btn_kfqr = QPushButton(Icon('submit'), '确认开发')
        self.btn_csgz = QPushButton(Icon('submit'), '测试跟踪')
        self.btn_yspj = QPushButton(Icon('评价'), '验收评价')
        #添加布局
        lt_btns.addWidget(self.btn_xqtj)
        lt_btns.addWidget(self.btn_xqsh)
        lt_btns.addWidget(self.btn_xqsp)
        lt_btns.addWidget(self.btn_kfqr)
        lt_btns.addWidget(self.btn_csgz)
        lt_btns.addWidget(self.btn_yspj)
        gp_btns.setLayout(lt_btns)
        # 添加左布局
        lt_main_left.addWidget(gp_left_top)
        lt_main_left.addWidget(self.gp_left_middle)
        lt_main_left.addWidget(gp_btns)
        ### 右布局 ###############################################
        lb_demand_name = QLabel('IT需求申请单')
        lb_demand_name.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_name)
        lt_1.addStretch()
        #############################################
        lt_2 = QGridLayout()
        self.cb_system = QComboBox()
        self.cb_system_modle = QComboBox()
        lt_main_right.addLayout(lt_1)
        # 添加主布局
        # lt_main.addWidget(gp_left_top)
        lt_main.addLayout(lt_main_left)
        lt_main.addLayout(lt_main_right)
        self.setLayout(lt_main)

    #单击表格
    def on_table_demand_click(self,QTableWidgetItem):
        row = QTableWidgetItem.row()
        self.cur_id = self.table_demand.getItemValueOfKey(row,'did')
        self.cur_name = self.table_demand.getItemValueOfKey(row, 'dname')
        self.cur_state = self.table_demand.getItemValueOfKey(row, 'state')

    # 查询
    def on_btn_query_click(self):
        tstart,tend = self.de_start.text(),self.de_end.text()
        vstate = self.state[self.cb_state.currentText()]
        if not vstate:
            results = self.session.query(MT_TJ_XQGL).filter(
                MT_TJ_XQGL.submit_time>=tstart,
                MT_TJ_XQGL.submit_time<tend
            ).all()
        else:
            results = self.session.query(MT_TJ_XQGL).filter(
                MT_TJ_XQGL.state==vstate,
                MT_TJ_XQGL.submit_time>=tstart,
                MT_TJ_XQGL.submit_time<tend
            ).all()
        self.table_demand.load([result.to_dict for result in results])
        self.gp_left_middle.setTitle('需求列表(%s)' %self.table_demand.rowCount())
        mes_about(self,"检索出%s条数据！" %self.table_demand.rowCount())

    # 导出功能
    def on_btn_export_click(self):
        self.table_demand.export()

    # 提交需求
    def on_btn_xqtj_click(self):
        demand_submit_dialog = DemandSubmitDialog(self)
        demand_submit_dialog.exec_()

    # 审核需求
    def on_btn_xqsh_click(self):
        demand_audit_dialog = DemandAuditDialog(self)
        demand_audit_dialog.title_changed.emit(self.cur_name)
        demand_audit_dialog.exec_()

    #审批需求
    def on_btn_xqsp_click(self):
        if self.cur_state=='已提交':
            mes_about(self,"需求管理员(张兆丰)审核完成后，方可处理！")
        elif self.cur_state=='已审核':
            button = mes_warn(self, "您确定审批本需求？")
            if button != QMessageBox.Yes:
                return
            try:
                self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID==self.cur_id).update({
                    MT_TJ_XQGL.state:'2'
                })
                self.session.commit()
            except Exception as  e:
                self.session.rollback()
                mes_about(self,"执行数据库操作发生错误，错误信息：%s" %e)
        else:
            mes_about(self,"当前需求已被审批过，请勿重复处理！")
        # demand_approval_dialog = DemandApprovalDialog(self)
        # demand_approval_dialog.exec_()

    # 开发确认
    def on_btn_kfqr_click(self):
        demand_develop_dialog = DemandDevelopDialog(self)
        demand_develop_dialog.title_changed.emit(self.cur_name)
        demand_develop_dialog.exec_()

    # 测试跟踪
    def on_btn_csgz_click(self):
        demand_track_dialog = DemandTrackDialog(self)
        demand_track_dialog.title_changed.emit(self.cur_name)
        demand_track_dialog.exec_()

    # 验收评价
    def on_btn_yspj_click(self):
        demand_evaluate_dialog = DemandEvaluateDialog(self)
        demand_evaluate_dialog.title_changed.emit(self.cur_name)
        demand_evaluate_dialog.exec_()

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(DemandManger, self).closeEvent(*args, **kwargs)


class DemandTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(DemandTable, self).__init__(heads, parent)

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(self.heads.keys()):
                data=row_data[col_name]
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 50)
        self.setColumnWidth(5, 70)
        self.setColumnWidth(6, 50)
        self.setColumnWidth(7, 70)
        self.setColumnWidth(8, 50)
        self.setColumnWidth(9, 70)
        self.setColumnWidth(10, 50)
        self.setColumnWidth(11, 70)
        self.setColumnWidth(12, 50)
        self.setColumnWidth(13, 70)

# 需求提交对话框
class DemandSubmitDialog(Dialog):

    def __init__(self,parent=None):
        super(DemandSubmitDialog,self).__init__(parent)
        self.setWindowTitle('需求提交')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('需求名称')
        lt_top2 = QHBoxLayout()
        gp_top2 = QGroupBox()
        self.lb_demand_title = QLabel('IT需求申请单 - 提交')
        self.lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(self.lb_demand_title)
        lt_1.addStretch()
        # 期望时间
        self.le_expected_time = QDateEdit(QDate.currentDate().addMonths(1))
        self.le_expected_time.setCalendarPopup(True)
        self.le_expected_time.setDisplayFormat("yyyy-MM-dd")
        self.le_demand_title = QLineEdit()
        self.le_demand_title.setMinimumWidth(150)
        self.le_demand_title.setPlaceholderText("尽量简短有内涵")
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb==1224,MT_GY_DMZD.dmsb>0).all()
        self.cb_system = QComboBox()
        self.cb_system.addItems([str2(result.srdm) for result in results])
        #### 模块 可编辑
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1225, MT_GY_DMZD.dmsb > 0).all()
        self.cb_module = QComboBox()
        self.cb_module.addItems([str2(result.srdm) for result in results])
        self.cb_module.setEditable(True)
        #### 紧急程度
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1228, MT_GY_DMZD.dmsb > 0).all()
        self.cb_level = QComboBox()
        self.cb_level.addItems([str2(result.srdm) for result in results])
        self.cb_level.setEditable(True)
        lt_top.addWidget(QLabel('需求名称：'))
        lt_top.addWidget(self.le_demand_title)
        gp_top.setLayout(lt_top)
        lt_top2.addWidget(QLabel('系统：'))
        lt_top2.addWidget(self.cb_system)
        lt_top2.addSpacing(15)
        lt_top2.addWidget(QLabel('模块：'))
        lt_top2.addWidget(self.cb_module)
        lt_top2.addSpacing(15)
        lt_top2.addWidget(QLabel('期望时间：'))
        lt_top2.addWidget(self.le_expected_time)
        lt_top2.addSpacing(15)
        lt_top2.addWidget(QLabel('紧急程度：'))
        lt_top2.addWidget(self.cb_level)
        lt_top2.addSpacing(15)
        # lt_top.addWidget(QLabel('提交时间：%s' %cur_date()))
        # lt_top.addSpacing(15)
        # lt_top.addWidget(QLabel('提交人：%s' % self.login_name))
        lt_top2.addStretch()
        gp_top2.setLayout(lt_top2)
        ### 现状描述 ########################
        lt_question = HBoxLayout()
        gp_question = GroupBox('现状描述')
        self.rt_question_describe = RichTextWidget()
        self.rt_question_describe.setPlaceholderText("业务场景描述：含现状操作流程、描述、问题及痛点。")
        lt_question.addWidget(self.rt_question_describe)
        gp_question.setLayout(lt_question)
        ### 需求描述 #################
        lt_demand = HBoxLayout()
        gp_demand = GroupBox('需求描述')
        self.rt_demand_describe = RichTextWidget()
        self.rt_demand_describe.setPlaceholderText("1、期望达成的目的；\n2、系统需求描述（含功能需求、流程、逻辑及描述等）；")
        lt_demand.addWidget(self.rt_demand_describe)
        gp_demand.setLayout(lt_demand)

        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("提交",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        # 添加布局
        # lt_main.addLayout(lt_1)
        # lt_main.addSpacing(20)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_top2)
        lt_main.addWidget(gp_question)
        lt_main.addWidget(gp_demand)
        lt_main.addSpacing(20)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    # 提交数据库
    def on_btn_submit_click(self):
        if not self.le_demand_title.text():
            mes_about(self,"请输入需求名称！")
            return
        if not self.rt_question_describe.text():
            mes_about(self, "请输入现状描述！")
            return
        if not self.rt_demand_describe.text():
            mes_about(self, "请输入需求描述！")
            return
        button = mes_warn(self, "您确定提交本需求？")
        if button != QMessageBox.Yes:
            return
        # 数据对象
        data_obj = {
            'state':'0',
            'dname':self.le_demand_title.text(),
            'submiter':self.login_name,
            'submit_time': cur_datetime(),
            'expect_date':self.le_expected_time.text(),
            'question':self.rt_question_describe.text(),
            'demand': self.rt_demand_describe.text(),
            'system': self.cb_system.currentText(),
            'module': self.cb_module.currentText(),
            'level': self.cb_level.currentText(),
        }
        try:
            self.session.bulk_insert_mappings(MT_TJ_XQGL, [data_obj])
            self.session.commit()
            mes_about(self, "提交成功！")
            self.accept()
        except Exception as e:
            self.session.rollback()
            mes_about(self,'插入 TJ_XQGL 记录失败！错误代码：%s' %e)

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 需求审核对话框
class DemandAuditDialog(Dialog):

    title_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DemandAuditDialog, self).__init__(parent)
        self.setWindowTitle('需求审核')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)
        self.title_changed.connect(self.setTitle)

    def initUI(self):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求申请单 - 审核')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_title)
        lt_1.addStretch()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox()
        # 期望时间
        self.le_done_time = QDateEdit(QDate.currentDate().addMonths(1))
        self.le_done_time.setCalendarPopup(True)
        self.le_done_time.setDisplayFormat("yyyy-MM-dd")
        self.le_demand_title = QLineEdit()
        self.le_demand_title.setPlaceholderText("尽量简短有内涵")
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb==1224,MT_GY_DMZD.dmsb>0).all()
        self.cb_system = QComboBox()
        self.cb_system.addItems([str2(result.srdm) for result in results])
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1225, MT_GY_DMZD.dmsb > 0).all()
        self.cb_module = QComboBox()
        self.cb_module.addItems([str2(result.srdm) for result in results])
        self.cb_module.setEditable(True)
        self.cb_level = QComboBox()
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1228, MT_GY_DMZD.dmsb > 0).all()
        self.cb_level.addItems([str2(result.srdm) for result in results])
        self.cb_level.setEditable(True)
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1227, MT_GY_DMZD.dmsb > 0).all()
        self.cb_demand_type = QComboBox()
        self.cb_demand_type.addItems([str2(result.srdm) for result in results])
        self.cb_demand_type.setEditable(True)
        lt_top.addWidget(QLabel('需求名称：'))
        lt_top.addWidget(self.le_demand_title)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('系统：'))
        lt_top.addWidget(self.cb_system)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('模块：'))
        lt_top.addWidget(self.cb_module)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('完成时间：'))
        lt_top.addWidget(self.le_done_time)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('紧急程度：'))
        lt_top.addWidget(self.cb_level)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('需求类型：'))
        lt_top.addWidget(self.cb_demand_type)
        lt_top.addSpacing(15)
        lt_top.addWidget(QLabel('审核人：%s' % self.login_name))
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        ### 预期收益 ########################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('预期收益')
        self.rt_suggest = RichTextWidget()
        self.rt_suggest.setPlaceholderText("\n评估预期的收益和价值（须有量化的数据说明及相应的衡量标准）。")
        lt_middle.addWidget(self.rt_suggest)
        gp_middle.setLayout(lt_middle)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("提交", QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        # lt_main.addLayout(lt_1)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_top2)
        lt_main.addWidget(gp_middle)
        lt_main.addSpacing(20)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setTitle(self,p_str):
        self.setWindowTitle("%s：%s" %(self.windowTitle(),p_str))

    # 提交数据库
    def on_btn_submit_click(self):
        pass

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 需求审批对话框
class DemandApprovalDialog(Dialog):

    def __init__(self, parent=None):
        super(DemandApprovalDialog, self).__init__(parent)
        self.setWindowTitle('需求审批')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求申请单 - 审批')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_title)
        lt_1.addStretch()
        lt_top = QFormLayout()
        gp_top = QGroupBox('好评率')

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("提交", QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        lt_main.addLayout(lt_1)
        lt_main.addSpacing(20)
        lt_main.addWidget(gp_top)
        # lt_main.addWidget(gp_middle)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    # 提交数据库
    def on_btn_submit_click(self):
        pass

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 需求开发对话框
class DemandDevelopDialog(Dialog):

    title_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DemandDevelopDialog, self).__init__(parent)
        self.setWindowTitle('需求开发')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)
        self.title_changed.connect(self.setTitle)

    def initUI(self):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求申请单 - 开发')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_title)
        lt_1.addStretch()
        lt_top = QFormLayout()
        gp_top = QGroupBox('')
        ### 服务评价 ########################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('解决方案')
        self.rt_suggest = RichTextWidget()
        self.rt_suggest.setPlaceholderText("\n评估需求可行性及资源匹配情况。")
        lt_middle.addWidget(self.rt_suggest)
        gp_middle.setLayout(lt_middle)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("提交", QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        lt_main.addLayout(lt_1)
        lt_main.addSpacing(20)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addSpacing(20)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setTitle(self,p_str):
        self.setWindowTitle("%s：%s" %(self.windowTitle(),p_str))

    # 提交数据库
    def on_btn_submit_click(self):
        pass

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 需求测试跟踪对话框
class DemandTrackDialog(Dialog):

    title_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DemandTrackDialog, self).__init__(parent)
        self.setWindowTitle('需求跟踪')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)
        self.title_changed.connect(self.setTitle)

    def initUI(self):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求申请单 - 跟踪')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_title)
        lt_1.addStretch()
        lt_top = QFormLayout()
        gp_top = QGroupBox('')
        ### 使用情况说明 ########################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('使用情况')
        self.rt_suggest = RichTextWidget()
        self.rt_suggest.setPlaceholderText("描述功能下放后使用情况")
        lt_middle.addWidget(self.rt_suggest)
        gp_middle.setLayout(lt_middle)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("提交", QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        lt_main.addLayout(lt_1)
        lt_main.addSpacing(20)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addSpacing(20)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setTitle(self,p_str):
        self.setWindowTitle("%s：%s" %(self.windowTitle(),p_str))

    # 提交数据库
    def on_btn_submit_click(self):
        pass

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 需求评价对话框
class DemandEvaluateDialog(Dialog):

    title_changed = pyqtSignal(str)

    def __init__(self,parent=None):
        super(DemandEvaluateDialog,self).__init__(parent)
        self.setWindowTitle('需求评价')
        self.initUI()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)
        self.title_changed.connect(self.setTitle)

    def initUI(self):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求申请单 - 评价')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_1 = QHBoxLayout()
        lt_1.addStretch()
        lt_1.addWidget(lb_demand_title)
        lt_1.addStretch()
        lt_top = QFormLayout()
        gp_top = QGroupBox('好评率')
        btns1 = EvaluateButton(['20%', '40%', '60%', '80%', '100%'])
        btns2 = EvaluateButton(['延期1月', '延期2周', '延期1周', '按期完成', '提前完成'])
        btns3 = EvaluateButton(['1周', '4天', '3天', '2天', '1天内'])
        lt_top.addRow(QLabel("解决效果："), btns1)
        lt_top.addRow(QLabel("承诺超期："), btns2)
        lt_top.addRow(QLabel("响应时间："), btns3)
        gp_top.setLayout(lt_top)
        ### 服务评价 ########################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('意见箱')
        self.rt_suggest = RichTextWidget()
        self.rt_suggest.setPlaceholderText("业务场景描述：含现状操作流程、描述、问题及痛点。")
        lt_middle.addWidget(self.rt_suggest)
        gp_middle.setLayout(lt_middle)

        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("提交",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        lt_main.addLayout(lt_1)
        lt_main.addSpacing(20)
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setTitle(self,p_str):
        self.setWindowTitle("%s：%s" %(self.windowTitle(),p_str))

    # 提交数据库
    def on_btn_submit_click(self):
        pass

    # 取消提交数据库
    def on_btn_cancle_click(self):
        button = mes_warn(self, "您确定放弃编辑？")
        if button != QMessageBox.Yes:
            return
        else:
            self.reject()

# 评价组按钮
class EvaluateButton(QWidget):

    def __init__(self,datas:list):
        super(EvaluateButton,self).__init__()

        lt_main = QHBoxLayout()
        for i in range(5):
            btn = QRadioButton(str(datas[i]))
            if i+1 ==5:
                self.num = 5
                btn.setChecked(True)
            btn.clicked.connect(partial(self.on_btn_click,i+1))
            lt_main.addWidget(btn)

        self.setLayout(lt_main)

    def on_btn_click(self,p_int):
        self.num = p_int

    def get_num(self):
        return self.num

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = DemandManger()
    ui.showMaximized()
    app.exec_()
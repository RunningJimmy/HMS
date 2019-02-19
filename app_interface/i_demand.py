from widgets.cwidget import *
from widget_custom import widget_set_value,UserLabel,SettingWidget
from widget_base import CefWidget
from widgets.richText import RichTextWidget
from utils import cur_datetime,build_chart
from app_interface.model import *

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
        self.table_demand.doubleClicked.connect(self.on_table_demand_dclick)
        self.btn_demand.clicked.connect(self.on_btn_demand_click)
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_print.clicked.connect(self.on_btn_print_click)
        # 特殊变量
        self.cur_id = None
        self.cur_state = None
        self.cur_name = None
        self.on_btn_query_click()

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_main_left = VBoxLayout()
        gp_main_left = QGroupBox()
        lt_main_right = VBoxLayout()
        gp_main_right = QGroupBox()
        # 左上布局
        lt_left_top = QHBoxLayout()
        gp_left_top = QGroupBox('条件检索')
        self.vstate = OrderedDict([
            ('所有', ''),
            ('已作废',-1),
            ('待提交',0),
            ('已提交',1),
            ('已审核',2),
            ('已开发',3),
            ('已跟踪',4),
            ('已验收',5)
        ])
        self.cb_state = QComboBox()
        self.cb_state.addItems(list(self.vstate.keys()))
        self.de_start = QDateEdit(QDate.currentDate().addDays(-365))
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        self.btn_query = QPushButton(Icon('query'), '查询')
        lt_left_top.addWidget(QLabel('需求状态：'))
        lt_left_top.addWidget(self.cb_state)
        lt_left_top.addWidget(QLabel('时间：'))
        lt_left_top.addWidget(self.de_start)
        lt_left_top.addWidget(QLabel('-'))
        lt_left_top.addWidget(self.de_end)
        lt_left_top.addWidget(Line())
        lt_left_top.addWidget(self.btn_query)
        lt_left_top.addStretch()
        gp_left_top.setLayout(lt_left_top)
        # 左中布局
        lt_left_middle = HBoxLayout()
        self.gp_left_middle = GroupBox('需求列表(0)')
        self.table_demand_cols = OrderedDict([
            ('DID', 'ID'),
            ('state', '状态'),
            ('dname', '需求名称'),
            ('submiter', '需求人'),
            ('submitime', '提交时间'),
            ('system', '系统名称'),
            ('module', '模块名称'),
            ('level', '紧急程度'),
            ('dtype', '需求类型'),
            ('expect_date', '期望日期'),
            ('shxm', '审核人'),
            ('shsj', '审核时间'),
            ('kfxm', '开发人'),
            ('kfsj', '开发时间'),
            ('gzxm', '跟踪人'),
            ('gzsj', '跟踪时间'),
            ('ysxm', '验收人'),
            ('yssj', '验收时间'),
            ('zfxm', '作废人'),
            ('zfsj', '作废时间'),
            ('question', '当前现状'),
            ('demand', '需求描述'),
            ('shnr', '需求评估'),
            ('jjfa', '解决方案'),
            ('syqk', '使用情况'),
            ('yspj', '验收评价'),
            ('zfyy', '作废原因'),
            ('zdy_pj1', '解决效果'),
            ('zdy_pj2', '承诺时间'),
            ('zdy_pj3', '操作体验'),

            ])
        self.table_demand = DemandTable(self.table_demand_cols)
        lt_left_middle.addWidget(self.table_demand)
        self.gp_left_middle.setLayout(lt_left_middle)
        #############################################################
        lt_btns = QHBoxLayout()
        gp_btns = QGroupBox()
        self.btn_demand = QPushButton('新增需求')
        self.btn_print = QPushButton(Icon('print'), '打印')
        self.btn_export = QPushButton(Icon('导出'), '导出')
        lt_btns.addWidget(self.btn_demand)
        lt_btns.addWidget(self.btn_print)
        lt_btns.addWidget(self.btn_export)
        gp_btns.setLayout(lt_btns)
        # 添加左布局
        lt_main_left.addWidget(gp_left_top)
        lt_main_left.addWidget(self.gp_left_middle)
        lt_main_left.addWidget(gp_btns)
        ### 右布局 ###############################################
        lt_right_top = QHBoxLayout()
        self.browser_all = CefWidget()
        self.browser_all2 = CefWidget()
        lt_right_bottom = QHBoxLayout()
        self.browser_all3 = CefWidget()
        self.browser_all4 = CefWidget()
        self.gp_right_top = QGroupBox()
        self.gp_right_bottom = QGroupBox()
        lt_right_top.addWidget(self.browser_all)
        lt_right_top.addWidget(self.browser_all2)
        # self.gp_right_top.setLayout(lt_right_top)
        lt_right_bottom.addWidget(self.browser_all3)
        lt_right_bottom.addWidget(self.browser_all4)
        # self.gp_right_bottom.setLayout(lt_right_bottom)
        lt_main_right.addLayout(lt_right_top)
        lt_main_right.addLayout(lt_right_bottom)
        # 添加主布局.
        # gp_main_left.setLayout(lt_main_left)
        # gp_main_right.setLayout(lt_main_right)
        # self.addWidget(gp_main_left)
        # self.addWidget(gp_main_right)

        lt_main.addLayout(lt_main_left,1)
        lt_main.addLayout(lt_main_right,2)
        self.setLayout(lt_main)

    #单击表格
    def on_table_demand_click(self,QTableWidgetItem):
        row = QTableWidgetItem.row()
        self.cur_id = self.table_demand.getItemValueOfKey(row,'DID')
        self.cur_name = self.table_demand.getItemValueOfKey(row, 'dname')
        self.cur_state = self.table_demand.getItemValueOfKey(row, 'state')

    # 编辑需求进度
    def on_table_demand_dclick(self,modelIndex):
        state = self.vstate.get(self.table_demand.getItemValueOfKey(modelIndex.row(),'state'),-1)
        ui = DemandProgressManager(self)
        ui.signal_action.emit(state,self.table_demand.selectRow2Dict())
        ui.exec_()

    # 获取最新操作者
    def newestor(self,row):
        state = self.vstate.get(self.table_demand.getItemValueOfKey(row, 'state'), -1)
        if state==1:
            return self.table_demand.getItemValueOfKey(row, 'submiter')
        elif state==2:
            return self.table_demand.getItemValueOfKey(row, 'shxm')
        elif state==3:
            return self.table_demand.getItemValueOfKey(row, 'kfxm')
        elif state==4:
            return self.table_demand.getItemValueOfKey(row, 'gzxm')
        elif state==5:
            return self.table_demand.getItemValueOfKey(row, 'ysxm')
        else:
            return ''

    # 新增需求
    def on_btn_demand_click(self):
        ui = DemandProgressManager(self)
        ui.signal_action.emit(0,{})
        ui.exec_()

    # 查询
    def on_btn_query_click(self):
        tstart,tend = self.de_start.text(),self.de_end.text()
        vstate = str(self.vstate[self.cb_state.currentText()])
        if not vstate:
            results = self.session.query(MT_TJ_XQGL).filter(
                MT_TJ_XQGL.submitime>=tstart,
                MT_TJ_XQGL.submitime<tend
            ).all()
        else:
            results = self.session.query(MT_TJ_XQGL).filter(
                MT_TJ_XQGL.state==vstate,
                MT_TJ_XQGL.submitime>=tstart,
                MT_TJ_XQGL.submitime<tend
            ).all()
        self.table_demand.load([result.to_dict for result in results])
        self.gp_left_middle.setTitle('需求列表(%s)' %self.table_demand.rowCount())
        # mes_about(self,"检索出%s条数据！" %self.table_demand.rowCount())
        sql = '''
            SELECT 
                (CASE state
                    WHEN 1 THEN '已提交'
                    WHEN 2 THEN '已审核'
                    WHEN 3 THEN '已开发'
                    WHEN 4 THEN '使用跟踪'
                    WHEN 5 THEN '验收评价'
                    ELSE '已作废' END 
                ) AS state,COUNT(*) AS SL
                FROM TJ_XQGL GROUP BY state
            '''
        results = dict(self.session.execute(sql).fetchall())
        chart_1 = build_chart("需求进度", results, 'pie', 240)
        if chart_1:
            self.browser_all2.load(chart_1)
            self.browser_all4.load(chart_1)
        sql2 ='''
        
            WITH T1 AS (
                SELECT 
                    SUM(CASE state WHEN '5' THEN 1 ELSE 0 END) AS wcs,
                    SUM(CASE WHEN state='10' THEN 0 ELSE 1 END) AS zrs 
                FROM TJ_XQGL
            )
            
            SELECT ROUND(convert(float,(wcs/CAST(zrs AS decimal)))*100,1) as bfl FROM T1
        '''
        result = self.session.execute(sql2).fetchone()
        chart_2 = build_chart("需求完成率", result[0], 'guage', 240)
        if chart_2:
            self.browser_all.load(chart_2)

        chart_3 = build_chart("需求进度", results, 'bar', 240)
        if chart_3:
            self.browser_all3.load(chart_3)

    # 大于功能
    def on_btn_print_click(self):
        row = self.table_demand.currentRow()
        if row==-1:
            mes_about(self,"请选择要打印的需求！")
            return
        state = self.vstate.get(self.table_demand.getItemValueOfKey(row, 'state'), -1)
        if state!=5:
            mes_about(self,"当前需求还未完成验收评价，不允许打印！")
            return
        mes_about(self,"打印功能暂未开放！")

    # 导出功能
    def on_btn_export_click(self):
        self.table_demand.export()

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(DemandManger, self).closeEvent(*args, **kwargs)

class DemandTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(DemandTable, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

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
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 80)
        self.setColumnWidth(5, 80)
        self.setColumnWidth(6, 80)
        self.setColumnWidth(7, 70)
        self.setColumnWidth(8, 80)
        self.setColumnWidth(9, 70)
        self.setColumnWidth(10, 50)
        self.setColumnWidth(11, 70)
        self.setColumnWidth(12, 50)
        self.setColumnWidth(13, 70)

class DemandProgressManager(Dialog, SettingWidget):

    signal_action = pyqtSignal(int, dict)

    def __init__(self, parent=None):
        super(DemandProgressManager, self).__init__(parent)
        self.resize(880, 600)
        self.setWindowTitle("业务需求管理")
        self.setChildWidgets()
        self.signal_action.connect(self.setData)
        # 增加作废按钮
        self.btn_delete = self.buttonBox.addButton("作废",QDialogButtonBox.ActionRole)
        self.btn_delete.clicked.connect(self.on_btn_delete_click)
        # 当前需求状态，默认是待提交状态
        self.cur_demand_state = 0
        self.cur_demand_id = 0

    def setChildWidgets(self):
        widgets = OrderedDict([
            ('需求提交', DemandSubmitWidget),
            ('需求审核', DemandAuditWidget),
            ('需求开发', DemandDevelopWidget),
            ('使用跟踪', DemandTrackWidget),
            ('验收评价', DemandEvaluateWidget),
            ('需求作废',DemandDeleteWidget)
        ])
        for label, widget_obj in widgets.items():
            widget = widget_obj()
            self.addWidget(label, widget)

    # 打开初始化
    def setData(self, state, data):
        # 更新当前状态
        self.cur_demand_state = state
        # 作废按钮变灰色
        if self.cur_demand_state in [5,-1]:
            self.btn_delete.setDisabled(True)
            self.buttonBox.buttons()[0].setEnabled(False)
        self.cur_demand_id = int(data.get('DID', 0))
        for widget in self.widgets():
            if widget.self_state == state:
                self.setCurWidget(widget)
            widget.signal_init.emit(state, data)
            widget.signal_close.connect(self.close)

    #保存编辑
    def on_btn_submit_click(self):
        if self.login_id == 'BSSA':
            mes_about(self, "系统管理员无权操作！")
            return
        for widget in self.widgets():
            widget.signal_save.emit(self.cur_demand_state, self.cur_demand_id)

    # 关闭窗口
    def on_btn_cancle_click(self):
        button = mes_warn(self, "你退出当前窗口吗？")
        if button != QMessageBox.Yes:
            return
        self.close()

    # 作废需求
    def on_btn_delete_click(self):
        if self.cur_demand_state==None:
            return
        elif self.cur_demand_state==5:
            mes_about(self,"当前需求已经完成验收，不允许作废！")
            return
        else:
            button = mes_warn(self, "你确定作废当前需求？")
            if button != QMessageBox.Yes:
                return
            else:
                for widget in self.widgets():
                    widget.signal_delete.emit(self.cur_demand_state, self.cur_demand_id)


# 需求提交对话框
class DemandSubmitWidget(Widget):

    signal_init = pyqtSignal(int,dict)      # 初始化信号
    signal_save = pyqtSignal(int,int)       # 保存信号，需求状态
    signal_delete = pyqtSignal(int, int)  # 保存信号，需求状态
    signal_close = pyqtSignal()             # 关闭主窗口的信号

    def __init__(self,parent=None):
        super(DemandSubmitWidget,self).__init__(parent)
        self.initUI()
        self.initParas()
        # 绑定信号槽
        self.signal_init.connect(self.on_demand_init)
        self.signal_save.connect(self.on_btn_submit_click)

    def initParas(self):
        self.self_state = 1
        # 绑定数据设置对象
        self.data_set_obj = {
            'state': '1',
            'dname':self.le_demand_title,
            'submitime': self.lb_submitime,
            'submiter':self.lb_submiter,
            'expect_date':self.le_expected_time,
            'question':self.rt_question_describe,
            'demand': self.rt_demand_describe,
            'system': self.cb_system,
            'module': self.cb_module,
            'level': self.cb_level,
            'dtype': self.cb_demand_type,
            'shxm': self.lb_shxm,
            'shsj': self.lb_shsj,
            'kfxm': self.lb_kfxm,
            'kfsj': self.lb_kfsj,
            'gzxm': self.lb_gzxm,
            'gzsj': self.lb_gzsj,
            'ysxm': self.lb_ysxm,
            'yssj': self.lb_yssj,
            'zfxm': self.lb_zfxm,
            'zfsj': self.lb_zfsj,
        }

    def initUI(self):
        main_layout = QVBoxLayout()
        main_area = QScrollArea()
        lt_main = QVBoxLayout()
        lt_demand_title = QHBoxLayout()
        gp_demand_title = QGroupBox('需求名')
        lt_info = QHBoxLayout()
        gp_info = QGroupBox()
        lt_user= QGridLayout()
        gp_user = QGroupBox('需求处理记录')
        # ####
        lb_demand_title = QLabel('IT需求单 - 提交')
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_title = QHBoxLayout()
        lt_title.addStretch()
        lt_title.addWidget(lb_demand_title)
        lt_title.addStretch()
        #############需求名称##################################
        self.le_demand_title = QLineEdit()
        self.le_demand_title.setMinimumWidth(150)
        self.le_demand_title.setPlaceholderText("尽量简短有内涵")
        # lt_demand_title.addWidget(QLabel('需求名称：'))
        lt_demand_title.addWidget(self.le_demand_title)
        gp_demand_title.setLayout(lt_demand_title)
        #################################################
        #### 系统
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb==1224,MT_GY_DMZD.dmsb>0).all()
        self.cb_system = QComboBox()
        self.cb_system.addItems([str2(result.srdm) for result in results])
        #### 模块 可编辑
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1225, MT_GY_DMZD.dmsb > 0).all()
        self.cb_module = QComboBox()
        self.cb_module.addItems([str2(result.srdm) for result in results])
        self.cb_module.setEditable(True)
        # 期望时间
        self.le_expected_time = QDateEdit(QDate.currentDate().addMonths(1))
        self.le_expected_time.setCalendarPopup(True)
        self.le_expected_time.setDisplayFormat("yyyy-MM-dd")
        #### 紧急程度
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1228, MT_GY_DMZD.dmsb > 0).all()
        self.cb_level = QComboBox()
        self.cb_level.addItems([str2(result.srdm) for result in results])
        self.cb_level.setEditable(True)
        ##### 需求类型
        results = self.session.query(MT_GY_DMZD).filter(MT_GY_DMZD.dmlb == 1227, MT_GY_DMZD.dmsb > 0).all()
        self.cb_demand_type = QComboBox()
        self.cb_demand_type.addItems([str2(result.srdm) for result in results])
        self.cb_demand_type.setEditable(True)
        #### 添加布局
        lt_info.addWidget(QLabel('系统：'))
        lt_info.addWidget(self.cb_system)
        lt_info.addSpacing(10)
        lt_info.addWidget(QLabel('模块：'))
        lt_info.addWidget(self.cb_module)
        lt_info.addSpacing(10)
        lt_info.addWidget(QLabel('期望时间：'))
        lt_info.addWidget(self.le_expected_time)
        lt_info.addSpacing(10)
        lt_info.addWidget(QLabel('紧急程度：'))
        lt_info.addWidget(self.cb_level)
        lt_info.addSpacing(10)
        lt_info.addWidget(QLabel('需求类型：'))
        lt_info.addWidget(self.cb_demand_type)
        lt_info.addStretch()
        gp_info.setLayout(lt_info)
        #### 处理记录 ################################
        self.lb_submiter = DemandLabel()     # 提交人
        self.lb_submitime = DemandLabel()    # 提交日期
        self.lb_shxm = DemandLabel()         # 提交人
        self.lb_shsj = DemandLabel()         # 提交日期
        self.lb_kfxm = DemandLabel()         # 开发姓名
        self.lb_kfsj = DemandLabel()         # 开发日期
        self.lb_gzxm = DemandLabel()         # 跟踪姓名
        self.lb_gzsj = DemandLabel()         # 跟踪日期
        self.lb_ysxm = DemandLabel()         # 验收姓名
        self.lb_yssj = DemandLabel()         # 验收日期
        self.lb_zfxm = DemandLabel()         # 作废姓名
        self.lb_zfsj = DemandLabel()         # 作废日期
        lt_user.addWidget(QLabel('提交：'), 0, 0, 2, 1)
        lt_user.addWidget(self.lb_submitime, 0, 1, 1, 1)
        lt_user.addWidget(self.lb_submiter, 1, 1, 1, 1)
        lt_user.addWidget(QLabel('审核：'), 0, 2, 2, 1)
        lt_user.addWidget(self.lb_shsj, 0, 3, 1, 1)
        lt_user.addWidget(self.lb_shxm, 1, 3, 1, 1)
        lt_user.addWidget(QLabel('开发：'), 0, 4, 2, 1)
        lt_user.addWidget(self.lb_kfsj, 0, 5, 1, 1)
        lt_user.addWidget(self.lb_kfxm, 1, 5, 1, 1)
        lt_user.addWidget(QLabel('跟踪：'), 0, 6, 2, 1)
        lt_user.addWidget(self.lb_gzsj, 0, 7, 1, 1)
        lt_user.addWidget(self.lb_gzxm, 1, 7, 1, 1)
        lt_user.addWidget(QLabel('验收：'), 0, 8, 2, 1)
        lt_user.addWidget(self.lb_yssj, 0, 9, 1, 1)
        lt_user.addWidget(self.lb_ysxm, 1, 9, 1, 1)
        lt_user.addWidget(QLabel('作废：'), 0, 10, 2, 1)
        lt_user.addWidget(self.lb_zfsj, 0, 11, 1, 1)
        lt_user.addWidget(self.lb_zfxm, 1, 11, 1, 1)
        # lt_user.setHorizontalSpacing(10)  # 设置水平间距
        # lt_user.setVerticalSpacing(10)  # 设置垂直间距
        # lt_user.setContentsMargins(5, 5, 5, 5)  # 设置外间距
        lt_user.setColumnStretch(11, 1)  # 设置列宽，添加空白项的
        gp_user.setLayout(lt_user)
        ### 现状描述 ########################
        lt_question = HBoxLayout()
        gp_question = GroupBox('现状描述')
        gp_question.setContentsMargins(0, 0, 0, 0)
        self.rt_question_describe = RichTextWidget()
        self.rt_question_describe.setPlaceholderText("业务场景描述：含现状操作流程、描述、问题及痛点。")
        lt_question.addWidget(self.rt_question_describe)
        gp_question.setLayout(lt_question)
        ### 需求描述 #################
        lt_demand = HBoxLayout()
        gp_demand = GroupBox('需求描述')
        gp_demand.setContentsMargins(0, 0, 0, 0)
        self.rt_demand_describe = RichTextWidget()
        self.rt_demand_describe.setPlaceholderText("1、期望达成的目的；\n2、系统需求描述（含功能需求、流程、逻辑及描述等）；")
        lt_demand.addWidget(self.rt_demand_describe)
        gp_demand.setLayout(lt_demand)
        # 添加主布局
        main_layout.addLayout(lt_title)
        main_layout.addSpacing(20)
        main_layout.addWidget(gp_user)
        main_layout.addWidget(gp_demand_title)
        main_layout.addWidget(gp_info)
        main_layout.addWidget(gp_question)
        main_layout.addWidget(gp_demand)
        self.setLayout(main_layout)

    # 编辑模式
    def on_demand_init(self,state:int,data:dict):
        '''
        :param state: 状态：提交状态下 才可修改
        :param data: 数据
        :return:
        '''
        for key,widget in self.data_set_obj.items():
            if not widget_set_value(widget,data.get(key,'')):
                if key in ['question','demand']:
                    widget.setHtml(data.get(key,''))

    # 提交数据库
    def on_btn_submit_click(self,state:int,xqid:int):
        # 说明已经进入了其他节点
        if state>1:
            return
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

        # 新提交的
        if state == 0:
            # 绑定数据获取对象
            data_get_obj = {
                'state': '1',
                'dname': self.le_demand_title.text(),
                'submiter': self.login_name,
                'submitime': cur_datetime(),
                'expect_date': self.le_expected_time.text(),
                'question': self.rt_question_describe.html(),
                'demand': self.rt_demand_describe.html(),
                'system': self.cb_system.currentText(),
                'module': self.cb_module.currentText(),
                'level': self.cb_level.currentText(),
                'dtype': self.cb_demand_type.currentText(),
            }
            try:
                self.session.bulk_insert_mappings(MT_TJ_XQGL, [data_get_obj])
                self.session.commit()
                mes_about(self, "需求提交：提交成功！")
                self.signal_close.emit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'需求提交：插入 TJ_XQGL 记录失败！错误代码：%s' %e)
        # 编辑的
        elif state==1:
            print(self.login_name,self.lb_submiter.text())
            if self.login_name!=self.lb_submiter.text():
                return
            try:
                self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID == xqid).update({
                    MT_TJ_XQGL.dname: self.le_demand_title.text(),
                    MT_TJ_XQGL.submiter: self.login_name,
                    MT_TJ_XQGL.submitime: cur_datetime(),
                    MT_TJ_XQGL.expect_date: self.le_expected_time.text(),
                    MT_TJ_XQGL.question: self.rt_question_describe.html(),
                    MT_TJ_XQGL.demand: self.rt_demand_describe.html(),
                    MT_TJ_XQGL.system: self.cb_system.currentText(),
                    MT_TJ_XQGL.module: self.cb_module.currentText(),
                    MT_TJ_XQGL.level: self.cb_level.currentText(),
                    MT_TJ_XQGL.dtype: self.cb_demand_type.currentText(),
                })
                self.session.commit()
                mes_about(self, "需求提交：保存成功！")
                self.signal_close.emit()
            except Exception as e:
                self.session.rollback()
                mes_about(self,'需求提交：更新TJ_XQGL 记录失败！错误代码：%s' %e)


# 需求 通用窗口
class DemandWidget(Widget):

    signal_save = pyqtSignal(int,int)           # 保存信号，需求状态,需求ID
    signal_init = pyqtSignal(int,dict)          # 初始化信号
    signal_delete = pyqtSignal(int, int)        # 作废信号
    signal_close = pyqtSignal()                 # 关闭主窗口的信号

    def __init__(self, win_title, gp_title, text_title, parent=None):
        super(DemandWidget, self).__init__(parent)
        self.initUI(win_title, gp_title, text_title)
        self.signal_init.connect(self.on_demand_init)
        self.signal_save.connect(self.on_btn_save_click)
        self.signal_delete.connect(self.on_btn_delete_click)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = -1

    def initUI(self, win_title, gp_title, text_title):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('IT需求单 - %s' % win_title)
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_title = QHBoxLayout()
        lt_title.addStretch()
        lt_title.addWidget(lb_demand_title)
        lt_title.addStretch()
        ####处理人信息##########
        lt_top = QHBoxLayout()
        self.lb_handle_time = DemandLabel()
        self.lb_handle_user = DemandLabel()
        lt_top.addWidget(QLabel("完成日期："))
        lt_top.addWidget(self.lb_handle_time)
        lt_top.addWidget(QLabel("%s人：" %win_title))
        lt_top.addWidget(self.lb_handle_user)
        lt_top.addStretch()
        ### 使用情况说明 ########################
        lt_middle = HBoxLayout()
        gp_middle = GroupBox(gp_title)
        gp_middle.setContentsMargins(0, 0, 0, 0)
        self.richtext = RichTextWidget()
        self.richtext.setMinimumHeight(250)
        self.richtext.setPlaceholderText(text_title)
        lt_middle.addWidget(self.richtext)
        gp_middle.setLayout(lt_middle)
        # 添加主布局
        lt_main.addLayout(lt_title)
        lt_main.addSpacing(20)
        lt_main.addLayout(lt_top)
        lt_main.addSpacing(10)
        lt_main.addWidget(gp_middle)
        self.setLayout(lt_main)

    # 提交数据库
    def on_btn_save_click(self,state:int,xqid:int):
        pass

    def on_demand_init(self,state:int,data:dict):
        self.richtext.setReadOnly(self.isEditable(state))

    def isEditable(self,state:int):
        if state==self.self_state-1:
            #上一步已完成，当前步骤可以继续
            return False
        elif state==self.self_state:
            # 当前步已完成，如果是本人操作，也可以继续
            if self.login_name==self.lb_handle_user.text():
                return False
            else:
                return True
        else:
            # 待提交的状态，不允许审核
            return True

    def on_btn_delete_click(self,state:int,xqid:int):
        pass

# 需求评价
class DemandEvaluateWidget(DemandWidget):

    def __init__(self, parent=None):
        win_title = "评价"
        gp_title = "意见箱"
        text_title = "\n功能修改后，说说您的使用体验。"
        super(DemandEvaluateWidget, self).__init__(win_title, gp_title, text_title, parent)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = 5
        ##### 增加特有的
        lt_top = QFormLayout()
        gp_top = GroupBox('好评率')
        self.zdy_pj1 = EvaluateButtonBox(['<100%', '=100%'])
        self.zdy_pj2 = EvaluateButtonBox(['延期完成', '按期完成', '提前完成'])
        self.zdy_pj3 = EvaluateButtonBox(['差评', '普通', '满意'])
        lt_top.addRow(QLabel("解决效果："), self.zdy_pj1)
        lt_top.addRow(QLabel("承诺时间："), self.zdy_pj2)
        lt_top.addRow(QLabel("操作体验："), self.zdy_pj3)
        gp_top.setLayout(lt_top)
        self.layout().addWidget(gp_top)

    # 提交数据库
    def on_btn_save_click(self,state:int,xqid:int):
        if self.isEditable(state):
            return
        if not self.richtext.text():
            return
        # 当前节点是本人提交的或者是新节点
        try:
            self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID==xqid).update({
                MT_TJ_XQGL.shnr:self.richtext.html(),
                MT_TJ_XQGL.shsj:cur_datetime(),
                MT_TJ_XQGL.shxm:self.login_name,
                MT_TJ_XQGL.state:str(self.self_state),
                MT_TJ_XQGL.zdy_pj1: self.zdy_pj1.get_score(),
                MT_TJ_XQGL.zdy_pj2: self.zdy_pj2.get_score(),
                MT_TJ_XQGL.zdy_pj3: self.zdy_pj3.get_score(),
            })
            self.session.commit()
            mes_about(self, "验收评价：保存成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '验收评价：更新 TJ_XQGL 记录失败！错误代码：%s' % e)

    def on_demand_init(self,state:int,data:dict):
        if data:
            # 非新增
            self.richtext.setHtml(data.get('yspj',''))
            self.lb_handle_user.setText(data.get('ysxm',''))
            self.lb_handle_time.setText(data.get('yssj', ''))

        super(DemandEvaluateWidget,self).on_demand_init(state,data)
        self.zdy_pj1.setDisabled(self.isEditable(state))
        self.zdy_pj2.setDisabled(self.isEditable(state))
        self.zdy_pj3.setDisabled(self.isEditable(state))

# 评价组按钮
class EvaluateButtonBox(QWidget):

    def __init__(self,datas:list):
        super(EvaluateButtonBox,self).__init__()
        self.initUI(datas)
        self.cur_score = -1

    def initUI(self,datas):
        lt_main = QHBoxLayout(self)
        for index,data in enumerate(datas):
            btn = QRadioButton(str(data))
            btn.setObjectName(str(index))
            if index == len(datas)-1:
                self.cur_score = index
                btn.setChecked(True)
            btn.clicked.connect(partial(self.on_btn_click,index))
            lt_main.addWidget(btn)

        self.setLayout(lt_main)

    # 单机
    def on_btn_click(self,index):
        self.cur_score = index

    # 获取
    def get_score(self):
        return self.cur_score

    # 设置
    def set_score(self,score):
        for i in range(self.layout().count()):
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget.objectName()==str(score):
                widget.setChecked(True)
                self.cur_score = score


# 需求审核
class DemandAuditWidget(DemandWidget):

    def __init__(self, parent=None):
        win_title = "审核"
        gp_title = "预期收益"
        text_title = "\n评估预期的收益和价值（须有量化的数据说明及相应的衡量标准）。"
        super(DemandAuditWidget, self).__init__(win_title, gp_title, text_title, parent)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = 2

    # 提交数据库
    def on_btn_save_click(self,state:int,xqid:int):
        if self.isEditable(state):
            return
        if not self.richtext.text():
            return
        # 当前节点是本人提交的或者是新节点
        try:
            self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID==xqid).update({
                MT_TJ_XQGL.shnr:self.richtext.html(),
                MT_TJ_XQGL.shsj:cur_datetime(),
                MT_TJ_XQGL.shxm:self.login_name,
                MT_TJ_XQGL.state:str(self.self_state)
            })
            self.session.commit()
            mes_about(self, "需求审核：保存成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '需求审核：更新 TJ_XQGL 记录失败！错误代码：%s' % e)

    def on_demand_init(self,state:int,data:dict):
        if data:
            # 非新增
            self.richtext.setHtml(data.get('shnr',''))
            self.lb_handle_user.setText(data.get('shxm',''))
            self.lb_handle_time.setText(data.get('shsj', ''))

        super(DemandAuditWidget, self).on_demand_init(state, data)

# 需求开发
class DemandDevelopWidget(DemandWidget):

    def __init__(self, parent=None):
        win_title = "开发"
        gp_title = "解决方案"
        text_title = "\n评估需求可行性及资源匹配情况"
        super(DemandDevelopWidget, self).__init__(win_title, gp_title, text_title, parent)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = 3

    # 提交数据库
    def on_btn_save_click(self,state:int,xqid:int):
        if self.isEditable(state):
            return
        if not self.richtext.text():
            return

        try:
            self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID==xqid).update({
                MT_TJ_XQGL.jjfa:self.richtext.html(),
                MT_TJ_XQGL.kfsj:cur_datetime(),
                MT_TJ_XQGL.kfxm:self.login_name,
                MT_TJ_XQGL.state: str(self.self_state)
            })
            self.session.commit()
            mes_about(self, "需求开发：保存成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '需求开发：更新 TJ_XQGL 记录失败！错误代码：%s' % e)

    def on_demand_init(self,state:int,data:dict):
        if data:
            # 非新增
            self.richtext.setHtml(data.get('jjfa',''))
            self.lb_handle_user.setText(data.get('kfxm',''))
            self.lb_handle_time.setText(data.get('kfsj', ''))

        super(DemandDevelopWidget, self).on_demand_init(state, data)

# 需求跟踪
class DemandTrackWidget(DemandWidget):

    def __init__(self,parent=None):
        win_title = "跟踪"
        gp_title = "使用情况"
        text_title = "\n描述功能下放后使用情况"
        super(DemandTrackWidget, self).__init__(win_title,gp_title,text_title,parent)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = 4

    # 提交数据库
    def on_btn_save_click(self,state:int,xqid:int):
        if self.isEditable(state):
            return
        if not self.richtext.text():
            return
        try:
            self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID==xqid).update({
                MT_TJ_XQGL.syqk:self.richtext.html(),
                MT_TJ_XQGL.gzsj:cur_datetime(),
                MT_TJ_XQGL.gzxm:self.login_name,
                MT_TJ_XQGL.state: str(self.self_state)
            })
            self.session.commit()
            mes_about(self, "使用跟踪：保存成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '使用跟踪：更新 TJ_XQGL 记录失败！错误代码：%s' % e)

    def on_demand_init(self,state:int,data:dict):
        if data:
            # 非新增
            self.richtext.setHtml(data.get('syqk',''))
            self.lb_handle_user.setText(data.get('gzxm',''))
            self.lb_handle_time.setText(data.get('gxsj', ''))

        super(DemandTrackWidget, self).on_demand_init(state, data)

# 需求作废
class DemandDeleteWidget(DemandWidget):

    def __init__(self, parent=None):
        win_title = "作废"
        gp_title = "作废情况"
        text_title = "\n描述您要作废此需求的理由"
        super(DemandDeleteWidget, self).__init__(win_title, gp_title, text_title, parent)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = -1

    # 提交数据库
    def on_btn_save_click(self, state: int, xqid: int):
        if state==-1:
            mes_about(self,"当前需求已经作废！")

    def isEditable(self,state:int):
        pass

    def on_demand_init(self, state: int, data: dict):
        if data:
            # 非新增
            self.richtext.setHtml(data.get('zfyy', ''))
            self.lb_handle_user.setText(data.get('zfxm', ''))
            self.lb_handle_time.setText(data.get('zfsj', ''))

    def on_btn_delete_click(self, state: int, xqid: int):
        if not self.richtext.text():
            mes_about(self,"请填写作废理由！")
            return
        try:
            self.session.query(MT_TJ_XQGL).filter(MT_TJ_XQGL.DID == xqid).update({
                MT_TJ_XQGL.zfyy: self.richtext.html(),
                MT_TJ_XQGL.zfsj: cur_datetime(),
                MT_TJ_XQGL.zfxm: self.login_name,
                MT_TJ_XQGL.state: None
            })
            self.session.commit()
            mes_about(self, "需求作废：保存成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '需求作废：更新 TJ_XQGL 记录失败！错误代码：%s' % e)


# 需求标签
class DemandLabel(UserLabel):

    def __init__(self):
        super(DemandLabel,self).__init__()
        self.setFixedWidth(70)
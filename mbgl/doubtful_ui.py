from widgets.cwidget import *
from mbgl.model import *
from functools import partial

# 四高+甲状腺结节 疑似筛选
class DoubtfulUI(Widget):

    def __init__(self):
        super(DoubtfulUI,self).__init__()
        self.initParas()
        self.initUI()
        # UI信号槽
        self.cb_jb1.stateChanged.connect(partial(self.on_checkbox_change,True))
        self.cb_jb2.stateChanged.connect(partial(self.on_checkbox_change,False))

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()

        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        # 特殊变量
        # 慢病病种
        self.jbbm_1 = {
            '高血压':'IS_GXY',
            '高血脂':'IS_GXZ',
            '高血糖':'IS_GXT',
            '高尿酸':'IS_GNS',
            '甲状腺':'IS_JZX'
        }

    # 导出功能
    def on_btn_export_click(self):
        self.table_health.export()

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        search_group = QGroupBox('条件检索')
        search_layout = QGridLayout()
        self.cb_jb1 = QCheckBox('台湾专家：')
        # self.ccb_jb1 = CheckComboBox(list(self.jbbm_1.keys()))
        self.ccb_jb1 = ComboCheckBox(list(self.jbbm_1.keys()))
        self.ccb_jb1.setMinimumWidth(150)
        self.cb_jb2 = QCheckBox('本院专家：')
        self.ccb_jb2 = QComboBox()
        self.ccb_jb2.addItems(['心内科','泌尿科','肝病科','妇科','心胸外科','消化内科'])
        self.ccb_jb2.setMinimumWidth(80)

        self.dg_rq = DateGroup()       # 检索时间
        self.dg_rq.jsrq.clear()
        self.dg_rq.jsrq.addItems(['签到日期','总检日期','审核日期'])
        self.mg_je = MoneyGroup()      # 检索金额
        self.tj_dw = TUintGroup(self.dwmc_bh,self.dwmc_py)       # 体检单位

        self.btn_query = ToolButton(Icon('query'),'查询')

        self.btn_query.setFixedWidth(64)
        self.btn_query.setFixedHeight(64)
        self.btn_query.setAutoRaise(False)
        # self.btn_export.setFixedWidth(64)
        # self.btn_export.setFixedHeight(64)
        # self.btn_export.setAutoRaise(False)

        # 第一列
        search_layout.addWidget(self.cb_jb1, 0, 0, 1, 1)
        # 第二列
        search_layout.addWidget(self.ccb_jb1, 0, 1, 1, 1)
        # 第三列
        search_layout.addWidget(self.cb_jb2, 0, 2, 1, 1)
        # 第四列
        search_layout.addWidget(self.ccb_jb2, 0, 3, 1, 1)
        search_layout.addItem(self.tj_dw, 1, 0, 1, 5)
        # 第六列
        search_layout.addItem(self.dg_rq, 0, 5, 1, 4)
        search_layout.addItem(self.mg_je, 1, 5, 1, 4)
        search_layout.addWidget(self.btn_query, 0, 9, 2, 2)

        search_layout.setHorizontalSpacing(10)            #设置水平间距
        search_layout.setVerticalSpacing(10)              #设置垂直间距
        search_layout.setContentsMargins(10, 10, 10, 10)  #设置外间距
        search_layout.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        search_group.setLayout(search_layout)


        self.gp_quick_search = QuickSearchGroup()
        
        lt_top.addWidget(search_group)
        lt_top.addWidget(self.gp_quick_search)
        # lt_top.addStretch()

        self.cols = OrderedDict([('tjbh','体检编号'),
                                 ('xm','姓名'),
                                 ('xb','性别'),
                                 ('nl','年龄'),
                                 ('sjhm','手机号码'),
                                 ('sfzh','身份证号'),
                                 ('ysje','体检金额'),
                                 ('is_gxy','高血压'),
                                 ('is_gxz', '高血脂'),
                                 ('is_gxt', '高血糖'),
                                 ('is_gns', '高尿酸'),
                                 ('is_jzx', '甲状腺'),
                                 ('glu', '血糖'),
                                 ('glu2', '餐后2小时血糖'),
                                 ('hbalc', '糖化血红蛋白'),
                                 ('ua', '尿酸'),
                                 ('tch', '总胆固醇'),
                                 ('tg', '甘油三酯'),
                                 ('hdl', '高密度脂蛋白'),
                                 ('ldl', '低密度脂蛋白'),
                                 ('hbp', '收缩压'),
                                 ('lbp', '舒张压'),
                                 ('dwmc', '单位名称')
                                 ])
        #### 刷选表格 ###########################################
        self.table_health = SlowHealthTable(self.cols)
        self.table_health.setContextMenuPolicy(Qt.CustomContextMenu)              ######允许右键产生子菜单
        self.table_health.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        self.gp_middle = QGroupBox('疑似列表(0)')
        lt_middle = QHBoxLayout()
        lt_middle.addWidget(self.table_health)
        self.gp_middle.setLayout(lt_middle)
        ########### 功能区 #################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        # 按钮功能区
        self.btn_item = QPushButton(Icon('项目'), '项目查看')         # 查看 LIS 结果
        self.btn_czjl = QPushButton(Icon('操作'), '操作记录')         # 查看体检记录
        self.btn_his_visit = QPushButton(Icon('就诊'), '历史就诊')    # 查看历史就诊
        self.btn_cur_visit = QPushButton(Icon('就诊'), '预约就诊')    # 查看体检记录
        self.btn_forbidden = QPushButton(Icon('暂停'), '报告禁用')  # 查看体检记录
        self.btn_phone = QPushButton(Icon('电话'),'电话记录')         # 查看电话记录
        self.btn_sms = QPushButton(Icon('短信'),'短信记录')           # 查看短信记录
        self.btn_export = QPushButton(Icon('导出'), '数据导出')       # 数据导出

        lt_bottom.addWidget(self.btn_item)
        lt_bottom.addWidget(self.btn_czjl)
        lt_bottom.addWidget(self.btn_his_visit)
        lt_bottom.addWidget(self.btn_cur_visit)
        # lt_bottom.addWidget(self.btn_forbidden)
        lt_bottom.addWidget(self.btn_phone)
        lt_bottom.addWidget(self.btn_sms)
        lt_bottom.addWidget(self.btn_export)
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addLayout(lt_top)
        #lt_main.addStretch()
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    def on_checkbox_change(self,is_one:bool,p_int:int):
        if is_one:
            # 操作了第一个复选框，2 选中，0 未选
            if p_int:
                self.cb_jb2.setDisabled(True)
                self.ccb_jb2.setDisabled(True)
            else:
                self.cb_jb2.setDisabled(False)
                self.ccb_jb2.setDisabled(False)
        else:
            # 操作了第2个复选框，2 选中，0 未选
            if p_int:
                self.cb_jb1.setDisabled(True)
                self.ccb_jb1.setDisabled(True)
            else:
                self.cb_jb1.setDisabled(False)
                self.ccb_jb1.setDisabled(False)
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: info_work_summary.py
@time: 2019-2-20 15:02
@version：0.1
@desc: 工作总结
'''

from widget_online import *
from .model import *

# 供应商联系表
class WorkSummaryWidget(Widget):

    def __init__(self,parent=None):
        super(WorkSummaryWidget,self).__init__(parent)
        # 初始化界面
        self.initUI()
        # 绑定信号槽
        self.initSignal()
        self.on_btn_search_click()

    def initSignal(self):
        self.table_worksummary.doubleClicked.connect(self.on_table_overtime_dclick)
        self.btn_insert.clicked.connect(self.on_btn_insert_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('检索条件')
        gp_top.setLayout(lt_top)
        ######
        lt_middle = HBoxLayout()
        self.gp_middle = GroupBox('值班(0)')
        self.table_worksummary_cols = OrderedDict([
            ('WID', "ID"),
            ('state', "状态"),
            ('editor', "总结人"),
            ('editime', "总结日期"),
            ('sjxm', "评语人"),
            ('pysj', "评语日期"),
            ('score', "评分"),
            ('xjqk', "巡检情况"),
            ('jyfs', "举一反三"),
            ('bzzj', "本周总结"),
            ('xzjh', "下周计划"),
            ('zsk', "知识库"),
            ('jsqk', "晋升情况"),
            ('jyfs', "举一反三"),
            ('sjpy', "上级评阅")
        ])
        self.table_worksummary = WorkSummaryTable(self.table_worksummary_cols)
        lt_middle.addWidget(self.table_worksummary)
        self.gp_middle.setLayout(lt_middle)
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox()
        self.btn_insert = QPushButton('新增')
        lt_bottom.addStretch()
        lt_bottom.addWidget(self.btn_insert)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    # 双击修改
    def on_table_overtime_dclick(self,QModelIndex):
        kwargs = {'state': {'提交': '0', '审阅': '1'}}
        state = int(kwargs.get(self.table_worksummary.itemValueOfKey(QModelIndex.row(),'state'),0))
        editor = self.table_worksummary.itemValueOfKey(QModelIndex.row(), 'editor')
        ui = WorkSummaryManager(self)
        ui.signal_action.emit(state,editor,self.table_worksummary.selectRow2Dict(**kwargs))
        ui.exec_()
        self.on_btn_search_click()

    # 查询
    def on_btn_search_click(self):
        results = self.session.query(MT_TJ_WorkSummary).all()
        self.table_worksummary.load([result.to_dict() for result in results])
        self.gp_middle.setTitle('工作总结(%s)' %self.table_worksummary.rowCount())

    # 增加
    def on_btn_insert_click(self):
        ui = WorkSummaryManager(self)
        ui.signal_action.emit(-1,'',{})
        ui.exec_()
        self.on_btn_search_click()

class WorkSummaryManager(Dialog, SettingWidget):

    signal_action = pyqtSignal(int,str,dict)

    def __init__(self, parent=None):
        super(WorkSummaryManager, self).__init__(parent)
        self.resize(880, 600)
        self.setWindowTitle("工作总结")
        self.setChildWidgets()
        self.signal_action.connect(self.setData)
        # 增加作废按钮
        self.btn_audit = self.buttonBox.addButton("审核",QDialogButtonBox.ActionRole)
        self.btn_audit.clicked.connect(self.on_btn_audit_click)
        # 当前状态，快速使用
        self.cur_state = 0
        self.cur_id = 0
        self.cur_editor = None
        self.cur_data = {}

    def setChildWidgets(self):
        widgets = OrderedDict([
            ('巡检情况', InspectionWidget),
            ('举一反三', ProblemWidget),
            ('本周总结', SummaryWidget),
            ('下周计划', PlanWidget),
            ('知识库', KnowledgeWidget),
            ('晋升项',PromotionWidget),
            ('领导评语',AuditWidget)
        ])
        for label, widget_obj in widgets.items():
            widget = widget_obj()
            self.addWidget(label, widget)

    # 打开初始化
    def setData(self, state:int,editor:str,data:dict):
        # 更新当前状态
        self.cur_state = state
        self.cur_editor = editor
        # 作废按钮变灰色
        if self.cur_state==-1:
            self.btn_audit.setDisabled(True)
            self.buttonBox.buttons()[0].setEnabled(False)
        self.cur_id = int(data.get('WID', 0))
        for widget in self.widgets():
            # 设置当前窗口
            # if widget.self_state == state:
            #     self.setCurWidget(widget)
            widget.signal_init.emit(state,editor, data)             # 初始化信号
            widget.signal_save.emit(state, editor, self.cur_id)     # 保存信号
            widget.signal_save_return.connect(self.on_save)         # 保存返回数据信号

    # 接收保存信号返回的数据
    def on_save(self,data:dict):
        for key,value in data.items():
            self.cur_data[key] = value

    #保存编辑信号发送
    def on_btn_submit_click(self):
        # 管理员无权保存
        if self.login_id == 'BSSA':
            mes_about(self, "系统管理员无权操作！")
            return
        # 自己才能编辑自己的总结
        if self.cur_editor and self.cur_editor!=self.login_name:
            mes_about(self, "您无权修改他人工作总结！")
            return
        # 上级领导已经审阅，也不能修改总结
        if self.cur_state==1:
            mes_about(self,"您的工作总结已被领导审阅，无法重新编辑保存！")
            return
        for widget in self.widgets():
            widget.signal_save.emit(self.cur_state, self.cur_editor, self.cur_id)     # 发送保存信号

        # 增加自身信息
        self.cur_data['editor'] = self.login_name
        self.cur_data['editime'] = cur_datetime()
        try:
            if self.cur_state==-1:
                # 新增
                self.session.bulk_insert_mappings(MT_TJ_WorkSummary, [self.cur_data])
            else:
                # 编辑
                data_obj = self.session.query(MT_TJ_WorkSummary).filter(MT_TJ_WorkSummary.WID==self.cur_id).first()
                update = {setattr(data_obj, k, v) for k, v in self.cur_data.items()}
            self.session.commit()
            mes_about(self, "工作总结：提交成功！")
            self.close()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '工作总结：插入 TJ_WorkSummary 记录失败！错误代码：%s' % e)

    # 关闭窗口
    def on_btn_cancle_click(self):
        button = mes_warn(self, "你退出当前窗口吗？")
        if button != QMessageBox.Yes:
            return
        self.close()

    # 审阅工作总结
    def on_btn_audit_click(self):
        if self.login_name != '张倩':
            mes_about(self, "您无权对工作总结进行评语！")
            return

        for widget in self.widgets():
            if widget.self_key=='sjpy':
                widget.signal_audit.emit(self.cur_id)
                widget.signal_close.connect(self.close)

class WorkSummaryTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(WorkSummaryTable, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(str(row_data[col_name]))
                # 布局位置
                if col_index == len(self.heads)-1:
                    item.setTextAlignment(Qt.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.horizontalHeader().setStretchLastSection(True)


# 通用窗口
class CommonWidget(Widget):

    signal_save = pyqtSignal(int,str,int)       # 状态，人员，唯一ID
    signal_save_return = pyqtSignal(dict)       # key - value
    signal_init = pyqtSignal(int,str,dict)      # 状态，人员，数据

    def __init__(self, win_title, gp_title, text_title, parent=None):
        super(CommonWidget, self).__init__(parent)
        self.initUI(win_title, gp_title, text_title)
        self.signal_init.connect(self.on_widget_init_click)
        self.signal_save.connect(self.on_widget_save_click)
        # 当前窗口自身的状态值，用来判断是否可以编辑当前窗口内容
        self.self_state = -1
        self.self_key = None

    def initUI(self, win_title, gp_title, text_title):
        lt_main = QVBoxLayout()
        lb_demand_title = QLabel('工作总结 - %s' % win_title)
        lb_demand_title.setStyleSheet('''font: 75 28pt '微软雅黑';color: rgb(0,128,0);''')
        lt_title = QHBoxLayout()
        lt_title.addStretch()
        lt_title.addWidget(lb_demand_title)
        lt_title.addStretch()
        ### 使用情况说明 ########################
        lt_middle = HBoxLayout()
        gp_middle = GroupBox(gp_title)
        gp_middle.setContentsMargins(0, 0, 0, 0)
        self.richtext = RichTextWidget()
        self.richtext.setMinimumHeight(480)
        self.richtext.setPlaceholderText(text_title)
        lt_middle.addWidget(self.richtext)
        gp_middle.setLayout(lt_middle)
        # 添加主布局
        lt_main.addLayout(lt_title)
        lt_main.addSpacing(10)
        lt_main.addWidget(gp_middle)
        self.setLayout(lt_main)

    # 不直接提交数据，返回数据给主窗口
    def on_widget_save_click(self,state:int,editor:str,wsid:int):
        self.signal_save_return.emit({self.self_key: self.richtext.html()})

    # 初始化
    def on_widget_init_click(self,state:int,editor:str,data:dict):
        self.richtext.setReadOnly(self.isEditable(state,editor))
        self.richtext.setHtml(data.get(self.self_key,''))

    # 是否可编辑
    def isEditable(self,state:int,editor:str):
        if state==1:
            # 已被上级审核，不能编辑了
            return True
        elif state == 0:
            # 如果是非本人操作，也不能编辑
            if editor and self.login_name==editor:
                return False
            else:
                return True
        else:
            # 新增
            return False

class InspectionWidget(CommonWidget):

    def __init__(self):
        super(InspectionWidget,self).__init__(
            win_title='巡检情况',
            gp_title='巡检情况(2分)',
            text_title = '\n1、发现的问题及详细描述；\n\n2、跟踪解决进度；',
        )
        self.self_key = 'xjqk'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(InspectionWidget,self).on_widget_save_click(state,editor,wsid)

class ProblemWidget(CommonWidget):

    def __init__(self):
        super(ProblemWidget, self).__init__(
            win_title='举一反三',
            gp_title='举一反三(5分)',
            text_title='\n1、什么事件？\n\n2、怎么思考？\n\n3、如何解决？\n\n4、价值及提效情况？\n\n5、是否还会出现同类型问题？',
        )
        self.self_key = 'jyfs'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(ProblemWidget,self).on_widget_save_click(state,editor,wsid)


class SummaryWidget(CommonWidget):

    def __init__(self):
        super(SummaryWidget, self).__init__(
            win_title='本周总结',
            gp_title='本周总结(3分)',
            text_title='\n1、......；\n\n2、......；\n\n3、......；',
        )
        self.self_key = 'bzzj'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(SummaryWidget,self).on_widget_save_click(state,editor,wsid)


class PlanWidget(CommonWidget):

    def __init__(self):
        super(PlanWidget, self).__init__(
            win_title='下周计划',
            gp_title='下周计划(3分)',
            text_title='\n1、......；\n\n2、......；\n\n3、......；',
        )
        self.self_key = 'xzjh'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(PlanWidget,self).on_widget_save_click(state,editor,wsid)

class KnowledgeWidget(CommonWidget):

    def __init__(self):
        super(KnowledgeWidget, self).__init__(
            win_title='知识库',
            gp_title='知识库(1分)',
            text_title='\n1、固定资产；\n\n2、机密文档；\n\n3、运维知识；\n\n4、问题跟进；\n\n5、值班交接；',
        )
        self.self_key = 'zsk'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(KnowledgeWidget,self).on_widget_save_click(state,editor,wsid)

class PromotionWidget(CommonWidget):

    def __init__(self):
        super(PromotionWidget, self).__init__(
            win_title='晋升努力',
            gp_title='晋升努力(3分)',
            text_title='\n1、在那些方面进行晋升项的尝试；',
        )
        self.self_key = 'jsqk'

    # # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    # def on_widget_save_click(self,state:int,editor:str,wsid:int):
    #     super(PromotionWidget,self).on_widget_save_click(state,editor,wsid)

class AuditWidget(CommonWidget):

    signal_audit = pyqtSignal(int)
    signal_close = pyqtSignal()

    def __init__(self):
        super(AuditWidget, self).__init__(
            win_title='领导评语',
            gp_title='领导评语(3分)',
            text_title='\n1、对同事进行周工作总结评语；',
        )
        # 增加控件
        lt_score = QHBoxLayout()
        gp_score = QGroupBox('总得分(20分)')
        self.sp_score = QSpinBox()
        self.sp_score.setMinimum(5)
        self.sp_score.setMaximum(20)
        self.sp_score.setValue(10)
        lt_score.addWidget(self.sp_score)
        gp_score.setLayout(lt_score)
        self.layout().addWidget(gp_score)
        #
        self.self_key = 'sjpy'
        self.signal_audit.connect(self.on_widget_audit_click)

    # 不直接提交数据到数据库，返回数据给主窗口，统计提交
    def on_widget_save_click(self,state:int,editor:str,wsid:int):
        pass

    # 直接提交到数据库
    def on_widget_audit_click(self,wsid:int):
        try:
            self.session.query(MT_TJ_WorkSummary).filter(MT_TJ_WorkSummary.WID==wsid).update({
                MT_TJ_WorkSummary.sjxm:self.login_name,
                MT_TJ_WorkSummary.pysj:cur_datetime(),
                MT_TJ_WorkSummary.score:self.sp_score.value(),
                MT_TJ_WorkSummary.sjpy:self.richtext.html()
            })
            self.session.commit()
            mes_about(self, "工作总结：审阅成功！")
            self.signal_close.emit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '工作总结：更新 TJ_WorkSummary 记录失败！错误代码：%s' % e)

    # 初始化
    def on_widget_init_click(self, state: int, editor: str, data: dict):
        super(AuditWidget,self).on_widget_init_click(state, editor, data)
        self.sp_score.setValue(int(data.get('score',0)))

# 需求标签
class DemandLabel(UserLabel):

    def __init__(self):
        super(DemandLabel,self).__init__()
        self.setFixedWidth(70)
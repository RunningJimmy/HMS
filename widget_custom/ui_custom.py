'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: ui_custom.py
@time: 2019-1-23 9:42
@desc: 
'''

from .common import *
import time


# 处理对话框，进度条，带后台线程，用于打印或者下载
class ReportHandleDialog(QDialog):
    # 初始化信号，传递参数
    signal_handle_init = pyqtSignal(list, str, str, str)
    # '''
    # :param list:体检编号列表，待处理
    # :param str:处理动作：打印、下载
    # :param str:如果是打印，则表示打印机名称，如果是下载 则表示下载的目录
    # :param str:打印成功推送url
    # '''

    # 单条处理完成信号，传递参数给调用方
    signal_handling = pyqtSignal(str, bool)
    # '''
    # :param str:体检编号
    # :param bool:处理是否成功
    # :param str:如果处理失败，则返回失败信息
    # '''

    def __init__(self, parent=None, title='明州体检'):

        super(ReportHandleDialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.initUI()
        # 绑定信号
        self.initSignal()

    # 绑定信号
    def initSignal(self):
        self.signal_handle_init.connect(self.initDatas)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)

    # 初始化UI
    def initUI(self):
        lables = {'num_all':'处理总数：', 'num_complete':'已处理数：', 'num_incomplete':'待处理数：','num_fail':'处理失败：'}
        lt_main = QVBoxLayout()
        ###########################################################
        self.lt_top = FlowLayout()
        gp_top = QGroupBox('处理进度总览')
        for key,value in lables.items():
            # 初始化赋值
            if not getattr(self, key, None):
                setattr(self, key, 0)
            # 标签和值属性一一对应
            lable_key = "lb_%s" %key
            setattr(self,lable_key , DetailLable(key))
            self.lt_top.addWidget(QLabel(value))
            self.lt_top.addWidget(getattr(self, lable_key))
        gp_top.setLayout(self.lt_top)
        # # 待接收的总数
        # self.lb_handle_all = ProcessLable()
        # # 已完成接收数
        # self.lb_handle_finished = ProcessLable()
        # # 未完成总数
        # self.lb_handle_unfinished = ProcessLable()
        # # 错误数
        # self.lb_handle_fail = ProcessLable()
        # # 添加布局
        # lt_top.addWidget(QLabel('处理总数：'))
        # lt_top.addWidget(self.lb_handle_all)
        # lt_top.addWidget(QLabel('已处理数：'))
        # lt_top.addWidget(self.lb_handle_finished)
        # lt_top.addWidget(QLabel('待处理数：'))
        # lt_top.addWidget(self.lb_handle_unfinished)
        # lt_top.addWidget(QLabel('处理失败：'))
        # lt_top.addWidget(self.lb_handle_fail)
        # gp_top.setLayout(lt_top)
        ###########################################################
        lt_middle = QHBoxLayout()
        gp_middle = QGroupBox('处理详情')
        ###########################################################
        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('处理进度')
        self.pb_progress = QProgressBar()
        self.pb_progress.setMinimum(0)
        self.pb_progress.setValue(0)
        lt_bottom.addWidget(self.pb_progress)
        gp_bottom.setLayout(lt_bottom)
        #########增加按钮组########################################
        lt_1 = QHBoxLayout()
        self.lb_timer = TimerLabel2()
        self.btn_start = QPushButton(Icon("启动"), "启动")
        self.btn_stop = QPushButton(Icon("停止"), "停止")
        self.btn_stop.setDisabled(True)
        lt_1.addWidget(self.lb_timer)
        lt_1.addStretch()
        lt_1.addWidget(self.btn_start)
        lt_1.addWidget(self.btn_stop)
        # 布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        lt_main.addLayout(lt_1)
        self.setLayout(lt_main)

    # 进度变化
    def on_progress_change(self, tjbh: str, state: bool):
        # 传递信号
        self.signal_handling.emit(tjbh, state)
        # 更新变量
        # self.datas.remove(tjbh)             # 用于暂停功能，重启启动用
        if state:
            setObjAttr(self,'num_complete',1)
        else:
            setObjAttr(self, 'num_fail', 1)
        # 未完成
        setObjAttr(self, 'num_incomplete', -1)

        # 刷新UI
        self.setLableText('num_complete')
        self.setLableText('num_incomplete')
        self.setLableText('num_fail')
        # self.lb_handle_finished.setText(str(self.num_finished))
        # self.lb_handle_unfinished.setText(str(self.num_unfinished))
        # self.lb_handle_fail.setText(str(self.num_fail))
        self.pb_progress.setValue(getattr(self,'num_complete') + getattr(self,'num_fail'))
        # 刷新进度条
        dProgress = (self.pb_progress.value() - self.pb_progress.minimum()) * 100.0 / (self.pb_progress.maximum() - self.pb_progress.minimum())
        # self.progress.setFormat("当前进度为：%s%" %dProgress)
        self.pb_progress.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 对齐方式

    def update_date(self):
        layout = self.lt_top.layout()
        print(layout.count())

    # 标签和值属性一一对应
    def setLableText(self,value_key):
        lable_key = "lb_%s" %value_key
        lable_obj =  getattr(self, lable_key)
        lable_obj.setText(str(str(getattr(self, value_key))))

    # 启动
    def on_btn_start_click(self):
        # 刷新界面控件
        self.btn_start.setDisabled(True)
        # self.btn_stop.setDisabled(False)
        self.lb_timer.start()
        setObjAttr(self,'num_all',len(self.datas))
        self.setLableText('num_all')
        self.pb_progress.setMaximum(getattr(self,'num_all'))
        if not self.report_handle_thread:
            self.report_handle_thread = ReportHandleThread()

        self.report_handle_thread.setTask(self.datas, self.action, self.other, self.url)
        self.report_handle_thread.signalCur.connect(self.on_progress_change, type=Qt.QueuedConnection)
        self.report_handle_thread.signalExit.connect(self.on_thread_exit, type=Qt.QueuedConnection)
        self.report_handle_thread.start()

    # 停止接收数据
    def on_btn_stop_click(self):
        # 刷新界面控件
        # self.btn_start.setDisabled(False)
        # self.btn_stop.setDisabled(True)
        self.lb_timer.stop()
        # 停止线程
        try:
            if self.report_handle_thread:
                self.report_handle_thread.stop()
        except Exception as e:
            print(e)
        self.close()

    # 初始化数据
    def initDatas(self, datas: list, action: str, other: str, url):
        '''
        :param datas: 体检编号
        :param action: print/down
        :param other: printer/filepath
        :return:
        '''
        self.datas = datas
        self.action = action
        self.other = other
        self.url = url
        self.on_btn_start_click()

        # 特殊变量
        self.datas = None
        self.action = None
        self.report_handle_thread = None
        # # 总数
        # self.num_all = 0
        # # 完成
        # self.num_finished = 0
        # # 未完成
        # self.num_unfinished = 0
        # # 失败
        # self.num_fail = 0

    def on_thread_exit(self):
        self.on_btn_stop_click()
        self.report_handle_thread = None
        mes_about(self, '处理完成！')
        self.close()

    def closeEvent(self, QCloseEvent):

        try:
            if self.report_handle_thread:
                # button = mes_warn(self,"当前正在打印报告，您是否确定立刻退出？")
                # if button == QMessageBox.Yes:
                self.report_handle_thread.stop()
                self.report_handle_thread = None
                # else:
                #     return
        except Exception as e:
            print(e)
        super(ReportHandleDialog, self).closeEvent(QCloseEvent)


# 打印线程
class ReportHandleThread(QThread):
    signalCur = pyqtSignal(str, int)  # 处理过程：成功/失败
    signalExit = pyqtSignal()

    def __init__(self):
        super(ReportHandleThread, self).__init__()
        self.runing = False
        self.initParas()

    def initParas(self):
        # 初始化环境变量
        self.num = 1
        self.report_down_url = "http://tjbg.nbmzyy.com:5005/api/report/down/pdf/%s"

    def stop(self):
        self.runing = False

    # 启动任务
    def setTask(self, tjbhs: list, action: str, other: str, url: str):
        self.tjbhs = tjbhs
        self.action = action
        self.other = other
        self.url = url
        self.runing = True

    def run(self):
        while self.runing:
            # 判断处理打印还是下载
            if self.action == 'print':
                for tjbh in self.tjbhs:
                    # 如果前台关闭，则后台关闭下一次循环
                    if self.runing:
                        url = self.report_down_url % tjbh
                        filename = file_tmp('%s.pdf' % tjbh)
                        if net_down(url, filename):
                            # 打印成功
                            if print_pdf_gsprint(filename) == 0:
                                self.signalCur.emit(tjbh, 1)
                                net_request(self.url, 'post')
                            else:
                                self.signalCur.emit(tjbh, 0)
                        else:
                            self.signalCur.emit(tjbh, 0)
            else:
                # 下载
                for tjbh in self.tjbhs:
                    # 如果前台关闭，则后台关闭下一次循环
                    if self.runing:
                        url = self.report_down_url % tjbh
                        filename = os.path.join(self.other, '%s.pdf' % tjbh)
                        if net_down(url, filename):
                            self.signalCur.emit(tjbh, 1)
                        else:
                            self.signalCur.emit(tjbh, 0)

            self.stop()
            self.signalExit.emit()

#详情标签
class DetailLable(QLabel):

    def __init__(self,obj_name):
        super(DetailLable, self).__init__()
        self.setObjectName(obj_name)
        self.setMinimumWidth(50)
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(0, 85, 255);''')


# 计时标签
class TimerLabel2(QLabel):
    def __init__(self, *args):
        super(TimerLabel2, self).__init__(*args)
        self.timer = QTimer(self)
        self.num = 0
        self.setStyleSheet('''font: 75 18pt \"微软雅黑\";color: rgb(255, 0, 0);''')
        self.setText(time.strftime('%H:%M:%S', time.gmtime(self.num)))
        self.timer.timeout.connect(self.on_timer_out)

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def on_timer_out(self):
        self.num = self.num + 1
        self.setText(time.strftime('%H:%M:%S', time.gmtime(self.num)))

# 对象某属性自增或者自减
def setObjAttr(obj,key,value):
    setattr(obj,key, getattr(obj, key) + value)


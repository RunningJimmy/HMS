'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: cchart.py
@time: 2019-1-18 14:20
@desc: 定制的UI 展示对话框
'''
from widgets.cwidget import *
from widgets.utils import CefWidget
from utils import get_chart_url

class SingleChartUI(Dialog):

    opened = pyqtSignal()

    def __init__(self, parent=None):
        super(SingleChartUI, self).__init__(parent)
        self.initUI()
        # 绑定信号槽
        self.opened.connect(self.on_btn_query_click)
        self.btn_query.clicked.connect(self.on_btn_query_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        # 查询区
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('条件检索')
        # 检索条件：体检日期
        self.de_start = QDateEdit(QDate.currentDate().addDays(-6))
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        self.btn_query = QPushButton(Icon('query'), '查询')
        # 添加布局
        lt_top.addWidget(QLabel("日期："))
        lt_top.addWidget(self.de_start)
        lt_top.addWidget(QLabel(' - '))
        lt_top.addWidget(self.de_end)
        lt_top.addWidget(self.btn_query)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        self.browser = CefWidget()
        self.browser.setMinimumWidth(850)
        self.browser.setMinimumHeight(450)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    def on_btn_query_click(self):
        tstart, tend = self.de_start.text(), self.de_end.text()
        self.browser.load(get_chart_url(self.windowTitle(), tstart, tend))
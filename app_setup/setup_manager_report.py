'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: setup_manager_report.py
@time: 2019-1-14 16:30
@desc: 报告设置：外网电子报告批量下载，个人报告设置，
'''

from widgets.cwidget import *
from utils import gol

class SetupManagerReport(DirTabWidget):

    def __init__(self):
        nodes= ['招工报告','个人报告','团体报告']
        super(SetupManagerReport,self).__init__('报告设置',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(SetupManagerReport, self).addTab(title)
        if title=='招工报告':
            from .enterprise_head_ui import EnterpriseHeadUI
            widget = EnterpriseHeadUI(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SetupManagerReport, self).closeEvent(*args, **kwargs)

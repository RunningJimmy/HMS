'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: setup_manager_group.py
@time: 2019-1-14 16:44
@desc: 单位设置
'''

from widgets.cwidget import *
from utils import gol

class SetupManagerUser(DirTabWidget):

    def __init__(self):
        nodes= ['招工报告','个人报告','团体报告']
        super(SetupManagerUser,self).__init__('报告设置',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(SetupManagerUser, self).addTab(title)
        if title=='招工报告':
            from .enterprise_head_ui import EnterpriseHeadUI
            widget = EnterpriseHeadUI(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SetupManagerUser, self).closeEvent(*args, **kwargs)
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: setup_manager_other.py
@time: 2019-1-15 15:14
@desc: 其他设置，无法归类的
'''

from widgets.cwidget import *
from utils import gol

class SetupManagerOther(DirTabWidget):

    def __init__(self):
        nodes= ['操作记录']
        super(SetupManagerOther,self).__init__('其他配置',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(SetupManagerOther, self).addTab(title)

        if title=='操作记录':
            from .operate_setup import OperateSetup
            widget = OperateSetup(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SetupManagerOther, self).closeEvent(*args, **kwargs)
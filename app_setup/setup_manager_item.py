'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: item_setup_manager.py
@time: 2019-1-12 21:55
@desc: 项目维护：项目类别，组合项目、科室项目、
'''

from widgets.cwidget import *
from utils import gol

class SetupManagerItem(DirTabWidget):

    def __init__(self):
        nodes= ['项目类别','组合项目','科室项目']
        super(SetupManagerItem,self).__init__('项目维护',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(SetupManagerItem, self).addTab(title)

        if title=='组合项目':
            from .item_setup import CItemWidget
            widget = CItemWidget(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SetupManagerItem, self).closeEvent(*args, **kwargs)
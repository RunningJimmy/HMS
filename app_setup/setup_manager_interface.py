'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: interface_setup_manager.py
@time: 2019-1-11 8:54
@desc: 接口配置管理：WEB、app、微信、电话、短信、HIS、LIS、PACS
'''

from widgets.cwidget import *
from utils import gol

class SetupManagerInterface(DirTabWidget):

    def __init__(self):
        nodes= ['短信模板','电话配置','检验对照','检查对照','HIS对照']
        super(SetupManagerInterface,self).__init__('科室管理',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(SetupManagerInterface, self).addTab(title)
        if title=='短信模板':
            from .sms_template_setup import SmsTemplateSetup
            widget = SmsTemplateSetup(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(SetupManagerInterface, self).closeEvent(*args, **kwargs)
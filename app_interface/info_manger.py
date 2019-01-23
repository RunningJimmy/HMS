'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: hms(健康管理系统)
@file: info_manger.py
@time: 2019-1-4 14:00
@desc:信息科科室管理：固定资产、供应商管理、接口文档、值班交接
'''

from widgets.cwidget import *
from utils import gol

class InfoManager(DirTabWidget):

    def __init__(self):
        nodes= ['固定资产','机密文档','值班交接']
        super(InfoManager,self).__init__('科室管理',nodes)
        default_menu_name = gol.get_value('menu_child_name','')
        if default_menu_name in nodes:
            self.addTab(default_menu_name)

    def addTab(self,title):
        super(InfoManager, self).addTab(title)
        if title=='固定资产':
            from .info_asset import InfoEquipAsset
            widget = InfoEquipAsset(self)
            self.rwidget.addPage(widget,Icon(title),title)

        elif title=='机密文档':
            if gol.get_value('login_user_id','')=='BSSA':
                from .info_supplier import InfoSupplier
                widget = InfoSupplier(self)
                self.rwidget.addPage(widget,Icon(title),title)
            else:
                mes_about(self,"您没有查看的权限！")

        elif title=='值班交接':
            from .info_overtime import InfoOverTime
            widget = InfoOverTime(self)
            self.rwidget.addPage(widget,Icon(title),title)

    def closeEvent(self, *args, **kwargs):
        super(InfoManager, self).closeEvent(*args, **kwargs)

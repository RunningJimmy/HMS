'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: ui_custom.py
@time: 2019-1-23 9:42
@desc: 
'''

from widget_base import *

# 主要：用于包裹表格
class GroupBox(QGroupBox):

    def __init__(self,*__args):
        super(GroupBox,self).__init__(*__args)
        self.setFlat(True)
        self.setFont(QFont("宋体",10))

# 主要：用于包裹表格
class HBoxLayout(QHBoxLayout):

    def __init__(self,parent=None):
        super(HBoxLayout,self).__init__(parent)
        self.setContentsMargins(0,10,0,0)





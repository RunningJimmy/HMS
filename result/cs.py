'''
@author: zhufd
@license: (C) Copyright 2018
@contact: 245838515@qq.com
@software: garner
@file: cs.py
@time: 2018-12-26 21:40
@desc:
'''

from widgets.cwidget import *

class ItemTemplateUI(Widget):

    def __init__(self,parent=None):
        super(ItemTemplateUI,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        ####### 检查所见 ##############
        gp_top = QGroupBox("检查所见")
        lt_top = QHBoxLayout()
        self.pte_result = QPlainTextEdit()
        lt_top.addWidget(self.pte_result)
        gp_top.setLayout(lt_top)
        ####### 诊断描述 ##############
        gp_middle = QGroupBox("诊断描述")
        lt_middle = QHBoxLayout()
        self.pte_describe = QPlainTextEdit()
        lt_middle.addWidget(self.pte_describe)
        gp_middle.setLayout(lt_middle)
        ####### 图像预览 ##############
        gp_bottom = QGroupBox("图像预览")
        lt_bottom = QHBoxLayout()
        self.pte_result = QPlainTextEdit()
        lt_bottom.addWidget(self.pte_result)
        gp_bottom.setLayout(lt_bottom)

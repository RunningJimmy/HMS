'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: button.py
@time: 2019-1-24 10:18
@version：0.1
@desc: 按钮组件
'''
from .common import *

#多选 下拉框
class ComCheckBox(QComboBox):

    def __init__(self, items:list,parent=None):
        super(ComCheckBox, self).__init__(parent)
        self.initUI()
        items.insert(0, '所有')
        for item in items:
            self.addWidget(item)
        # 默认 所有
        self.on_items_check(2)

    def initUI(self):
        self.le_items = QLineEdit()
        self.le_items.setReadOnly(True)
        # 存放 QCheckbox 容器
        self.lw_checkbox = QListWidget()
        # 设置
        self.setModel(self.lw_checkbox.model())
        self.setView(self.lw_checkbox)
        self.setLineEdit(self.le_items)

    def addWidget(self,item:str):
        cb_item = QCheckBox(item)
        if item=='所有':
            cb_item.stateChanged.connect(self.on_items_check)
        else:
            cb_item.stateChanged.connect(self.on_item_check)

        self.lw_checkbox.setItemWidget(QListWidgetItem(self.lw_checkbox), cb_item)

    def on_item_check(self,state:int):
        self.le_items.clear()
        if self.itemSelectCount() == 0:
            self.setCheckState(0)
        elif self.itemSelectCount() == self.count() - 1:
            self.setCheckState(2)
        else:
            self.setCheckState(1)
        self.le_items.setText(";".join(self.itemSelectText()))

    def on_items_check(self, state:int):
        if state == 2:
            self.setItemsChecked(True,1)
        elif state == 1:
            if self.itemSelectCount() == 0:
                self.setCheckState(2)
            # elif self.itemSelectCount() == self.count() - 1:
            #     self.setItemChecked(0, True)
            # else:
            #     self.setCheckState(2)
        elif state == 0:
            self.setItemsChecked(False)

    # 选中的文本
    def itemSelectText(self):
        '''
        :return: list
        '''
        tmp =[]
        for index in range(1, self.count()):
            if self.itemChecked(index):
                tmp.append(self.itemText(index))
        return tmp

    def itemSelectCount(self):
        '''
        :return: int
        '''
        count = 0
        for index in range(1, self.count()):
            if self.itemChecked(index):
                count = count + 1

        return count

    def itemText(self,index):
        '''
        :param index:
        :return: str
        '''
        return self.itemWidget(index).text()

    def itemChecked(self,index:int):
        '''
        :param index:
        :return: bool
        '''
        return self.itemWidget(index).isChecked()

    def itemWidget(self,index:int):
        '''
        :param index:
        :return: QCheckBox
        '''
        return self.lw_checkbox.itemWidget(self.lw_checkbox.item(index))

    def setItemChecked(self,state:bool,index=0):
        '''
        :param index: item对应widget的索引
        :param state: 是否选中
        :return:
        '''
        self.itemWidget(index).setChecked(state)

    def setCheckState(self,state:int,index=0):
        '''
        :param index: item对应widget的索引
        :param state: 是否选中、半选中  采用int类型
        :return:
        '''
        self.itemWidget(index).setCheckState(state)

    def setItemsChecked(self,state:bool,start_index = 0):
        '''
        :param state: 是否选中
        :param start_index: 默认所有，也可以是部分
        :return:
        '''
        for index in range(start_index,self.count()):
            self.setItemChecked(state,index)

# 工具栏按钮
class ToolButton(QToolButton):

    def __init__(self,icon,name):
        super(ToolButton,self).__init__()
        self.setIcon(icon)
        self.setText(name)
        self.setIconSize(QSize(32,32))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)
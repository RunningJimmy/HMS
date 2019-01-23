'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: toolkit.py
@time: 2019-1-22 15:11
@desc: 工具箱
'''
from ctypes import CDLL
from functools import partial
from widgets.cwidget import *
from widgets.calculator import CalculatorUI

class ToolkitUI(QDialog):

    def __init__(self,parent=None):
        super(ToolkitUI,self).__init__(parent)
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
        self.initUI()
        self.initSignal()

    def initSignal(self):
        self.btn_screenshot.menu_clicked.connect(self.on_btn_screenshot_click)
        self.btn_calculator.clicked.connect(self.on_btn_calculator_click)

    def initUI(self):
        lt_main = QHBoxLayout()
        self.btn_screenshot = MenuPopupButton(Icon('screenshot'), "快速截图",["隐藏界面","不隐藏"])
        self.btn_calculator = ToolButton(Icon('calculator'), "计算器")
        lt_main.addWidget(self.btn_screenshot)
        lt_main.addWidget(self.btn_calculator)
        self.setLayout(lt_main)

    # 截图
    def on_btn_screenshot_click(self,state:bool):
        if state:
            self.showMinimized()
            time.sleep(0.3)
        dll = CDLL('ScreenShot.dll')
        dll.PrScrn()

    def on_btn_calculator_click(self):
        self.close()
        ui = CalculatorUI(self)
        ui.exec_()



class MenuPopupButton(QToolButton):

    menu_clicked =pyqtSignal(bool)

    def __init__(self,icon:QIcon,text,menu_text:list,parent=None):
        super(MenuPopupButton,self).__init__(parent)
        self.setIcon(icon)
        self.setText(text)
        self.setIconSize(QSize(32, 32))
        self.setAutoRaise(True)
        self.setPopupMode(QToolButton.InstantPopup)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        menu=QMenu()
        menu.addAction(icon,menu_text[0],partial(self.on_btn_click,True))
        menu.addAction(icon,menu_text[1],partial(self.on_btn_click,False))
        self.setMenu(menu)

    def on_btn_click(self,state:bool):
        self.menu_clicked.emit(state)
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: widget_set.py
@time: 2019-2-11 16:39
@version：0.1
@desc: 参数配置界面
'''

# '''
# 左侧为QListWidget，右侧使用QScrollArea设置QVBoxLayout，然后依次往里面添加QWidget
# 右侧添加QWidget的时候有两种方案
# 左侧list根据序号来索引，右侧添加widget时给定带序号的变量名，如widget_0,widget_1,widget_2之类的，这样可以直接根据QListWidget的序号关联起来
# 左侧list添加item时给定右侧对应的widget变量值
# 相关事件：
# 1、绑定左侧QListWidget的itemClicked的到该item的索引
# 2、绑定右侧滚动条的valueChanged事件得到pos
# 注意：当itemClicked时定位滚动条的值时，需要设置一个标志位用来避免valueChanged重复调用item的定位
# '''

from widget_custom.common import *

#设置区域,用于添加多个窗口
class SettingScrollArea(QScrollArea):

    def __init__(self, parent=None):
        super(SettingScrollArea, self).__init__(parent)



class SettingWidget(QWidget):

    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)

        # 滚动信号
        self.signal_block = False

    def initSignal(self):
        # 绑定滚动条和左侧item事件
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.onValueChanged)
        self.listWidget.itemClicked.connect(self.onItemClicked)

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_main.setContentsMargins(0, 0, 0, 0)
        lt_main.setSpacing(0)
        # 左边控件
        self.widget_left = QListWidget()
        self.widget_left.setFrameShape(QFrame.NoFrame)
        self.widget_left.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget_left.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget_left.setObjectName("listWidget")
        lt_main.addWidget(self.widget_left)
        # 右边控件
        self.widget_right = QScrollArea()
        self.widget_right.setFrameShape(QFrame.NoFrame)
        self.widget_right.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget_right.setWidgetResizable(True)
        self.widget_right.setObjectName("scrollArea")

    def onValueChanged(self, value):
        """滚动条"""
        if self.signal_block:
            # 防止item点击时改变滚动条会触发这里
            return
        for i in range(8):  # 因为这里右侧有8个widget
            widget = getattr(self, 'widget_%d' % i, None)
            # widget不为空且在可视范围内
            if widget and not widget.visibleRegion().isEmpty():
                self.listWidget.setCurrentRow(i)  # 设置item的选中
                return

    def onItemClicked(self, item):
        """左侧item"""
        row = self.listWidget.row(item)  # 获取点击的item的索引
        # 由于右侧的widget是按照命名widget_0 widget_1这样比较规范的方法,可以通过getattr找到
        widget = getattr(self, 'widget_%d' % row, None)
        if not widget:
            return
        # 定位右侧位置并滚动
        self.signal_block = True
        self.scrollArea.verticalScrollBar().setSliderPosition(widget.pos().y())
        self.signal_block = False


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(open("Data/style.qss", "rb").read().decode("utf-8"))
    w = Window()
    w.show()
    sys.exit(app.exec_())
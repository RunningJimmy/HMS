'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: widget_set.py
@time: 2019-2-11 16:39
@version：0.1
@desc: 快速滚动到当前窗口，也可以啦滚动条的
'''

# '''
# 左侧为QListWidget，右侧使用QScrollArea设置QVBoxLayout，然后依次往里面添加QWidget
# 相关事件：
# 1、绑定左侧QListWidget的itemClicked的到该item的索引
# 2、绑定右侧滚动条的valueChanged事件得到pos
# 注意：当itemClicked时定位滚动条的值时，需要设置一个标志位用来避免valueChanged重复调用item的定位
# '''

from widget_custom.common import *

#设置区域,用于添加多个窗口
class SettingScrollWidget(QScrollArea):

    def __init__(self, parent=None):
        super(SettingScrollWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        # 设置滚动区域
        self.widget_contents = QWidget(self)
        # self.widget_contents.setGeometry(QRect(0, 0, 3000, 600))
        self.lt_main = QVBoxLayout()
        self.setWidget(self.widget_contents)
        self.widget_contents.setLayout(self.lt_main)

    # 添加窗口
    def addWidget(self, widget: QWidget):
        #self.lt_main.setContentsMargins(35, 20, 35, 20)
        self.lt_main.setSpacing(20)
        self.lt_main.addWidget(widget)

class SettingWidget(QWidget):

    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        self.initParas()
        self.initUI()
        self.initSignal()

    def initSignal(self):
        # 绑定滚动条和左侧item事件
        self.widget_right.verticalScrollBar().valueChanged.connect(self.onValueChanged)
        self.widget_left.itemClicked.connect(self.onLabelClicked)
        self.buttonBox.accepted.connect(self.on_btn_submit_click)
        self.buttonBox.rejected.connect(self.on_btn_cancle_click)

    def initUI(self):
        lt_main = QHBoxLayout()
        lt_main.setContentsMargins(0, 0, 0, 0)
        lt_main.setSpacing(0)
        # 左边布局
        lt_right = QVBoxLayout()
        lt_right.setContentsMargins(0, 0, 0, 0)
        lt_right.setSpacing(0)
        # 左边标签列表
        self.widget_left = QListWidget()
        self.widget_left.setStyleSheet(self.style)
        self.widget_left.setFrameShape(QFrame.NoFrame)
        self.widget_left.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget_left.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 右边滚动区域
        self.widget_right = SettingScrollWidget(self)
        # 保存按钮
        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("保存",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        lt_right.addWidget(self.widget_right)
        lt_right.addSpacing(25)
        lt_right.addWidget(self.buttonBox)
        lt_right.addSpacing(10)
        lt_main.addWidget(self.widget_left)
        lt_main.addLayout(lt_right)
        self.setLayout(lt_main)

    def onValueChanged(self, value):
        """滚动条"""
        if self.signal_block:
            # 防止item点击时改变滚动条会触发这里
            return
        widgets = list(self.child_widgets.values())
        for widget in widgets:
            # widget不为空且在可视范围内
            if widget and not widget.visibleRegion().isEmpty():
                self.widget_left.setCurrentRow(widgets.index(widget))  # 设置item的选中
                return

    def onLabelClicked(self,item:QListWidgetItem):
        widget = self.child_widgets.get(item.text())
        if not widget:
            return
        # 定位右侧位置并滚动
        self.signal_block = True
        self.widget_right.verticalScrollBar().setSliderPosition(widget.pos().y())
        self.signal_block = False

    # 标签与窗口必须一一对应
    def addWidget(self,label:str,widget:QWidget):
        '''
        :param label: 标签
        :param widget: 窗口
        :return:
        '''
        item = QListWidgetItem(label)
        item.setSizeHint(QSize(30, 50))
        item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        self.widget_left.addItem(item)
        self.widget_right.addWidget(widget)
        self.child_widgets[label] = widget

    # 返回滚动区域子窗口
    def widgets(self):
        return self.child_widgets.values()

    # 设置窗口
    def setCurWidget(self,widget:QWidget):
        index = list(self.widgets()).index(widget)
        self.widget_left.setCurrentRow(index)
        self.onLabelClicked(self.widget_left.item(index))

    def on_btn_submit_click(self):
        pass

    def on_btn_cancle_click(self):
        pass

    def initParas(self):
        # 滚动信号
        self.signal_block = False
        self.child_widgets = OrderedDict()
        # 样式表
        self.style = '''
             QListWidget {
                outline: 0px;
             }
             QListWidget {
                 min-width: 80px;
                 max-width: 80px;
                 color: Black;
                 background: #F5F5F5;
            }
            QListWidget::Item:selected {
                background: lightGray;
                border-left: 5px solid red;
            }
            HistoryPanel:hover {
                background: rgb(52, 52, 52);
            }
            '''
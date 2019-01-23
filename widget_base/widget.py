'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: widget.py
@time: 2019-1-23 9:13
@desc: 基础组件，无关业务
'''
from .common import *




# 消息弹出框，指定时间自动关闭
class WindowNotify(QWidget):

    singal_closed = pyqtSignal()  # 弹窗关闭信号

    def __init__(self, title="测试", size=(300, 400), timeout=5000, parent=None):
        super(WindowNotify, self).__init__(parent)
        self.setFixedSize(QSize(size[0], size[1]))
        self._timeout = timeout
        self._initUI()
        self._initParas()
        self._initSignal()
        self.setTitle(title)

    def _initUI(self):
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        lt_main = QVBoxLayout()
        lt_main.setContentsMargins(0, 0, 0, 0)
        lt_main.setSpacing(6)
        # 标题栏
        lt_top = QHBoxLayout()
        lt_top.setContentsMargins(10, 0, 0, 0)
        lt_top.setSpacing(0)
        widget_title = QWidget()
        widget_title.setObjectName("widget_title")
        widget_title.setMinimumSize(QSize(0, 26))
        self.lb_title = QLabel()
        self.lb_title.setObjectName("lb_title")
        self.btn_close = QPushButton("r")
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setMinimumSize(QSize(26, 26))
        self.btn_close.setMaximumSize(QSize(26, 26))
        # 添加标题布局
        lt_top.addWidget(self.lb_title)
        lt_top.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lt_top.addWidget(self.btn_close)
        widget_title.setLayout(lt_top)
        # 控件区
        self.widget_area = QWidget()
        # 底部
        lt_bottom = QHBoxLayout()
        lt_bottom.setContentsMargins(0, 5, 5, 5)
        lt_bottom.setSpacing(0)
        widget_bottom = QWidget()
        widget_bottom.setObjectName("widget_bottom")
        self.btn_sure = QPushButton("确定")
        self.btn_sure.setObjectName("btn_sure")
        self.btn_sure.setMinimumSize(QSize(75, 25))
        self.btn_sure.setCursor(QCursor(Qt.PointingHandCursor))
        # 添加底部布局
        lt_bottom.addItem(QSpacerItem(170, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lt_bottom.addWidget(self.btn_sure)
        widget_bottom.setLayout(lt_bottom)
        # 添加主布局
        lt_main.addWidget(widget_title)
        lt_main.addStretch()
        lt_main.addWidget(self.widget_area)
        lt_main.addStretch()
        lt_main.addWidget(widget_bottom)

        self.setLayout(lt_main)
        # 自动连接信号槽
        # QMetaObject.connectSlotsByName(self)

    def _initSignal(self):
        self.btn_close.clicked.connect(self.on_btn_close_click)  # 关闭按钮事件
        self.btn_sure.clicked.connect(self.on_btn_sure_click)  # 点击确定按钮
        self.animation_obj.finished.connect(self.on_animation_end)  # 动画
        self.timer_obj.timeout.connect(self.on_animation_close)  # 定时器

    def _initParas(self):
        self.is_show = True  # 是否 显示
        self.is_timeout = False  # 是否 超时
        # 桌面
        self.desktop_obj = QApplication.instance().desktop()
        # self.desktop_obj = QDesktopWidget()
        print(self.desktop_obj.screenGeometry().width(),
              self.desktop_obj.screenGeometry().height(),
              self.width(),
              self.height()
              )
        # 窗口初始开始位置
        self.start_pos = QPoint(
            self.desktop_obj.screenGeometry().width() - self.width() - 5,
            self.desktop_obj.screenGeometry().height()
        )
        # 窗口弹出结束位置
        self.end_pos = QPoint(
            self.desktop_obj.screenGeometry().width() - self.width() - 5,
            self.desktop_obj.availableGeometry().height() - self.height() - 5
        )
        # 初始化位置到右下角
        self.move(self.start_pos)
        # 动画
        self.animation_obj = QPropertyAnimation(self, b"pos")
        self.animation_obj.setDuration(1000)  # 1s
        # 定时器
        self.timer_obj = QTimer(self)
        # 样式表
        self.setStyleSheet('''
            QWidget#widget_title {
                background-color: rgb(76, 169, 106);
            }
            QWidget#widget_bottom {
                border-top-style: solid;
                border-top-width: 2px;
                border-top-color: rgb(185, 218, 201);
            }
            QLabel#lb_title {
                color: rgb(255, 255, 255);
            }
            QLabel#labelContent {
                padding: 5px;
            }
            QPushButton#btn_close {
                border: none;
                background: transparent;
                font-family: \"webdings\";
                color: rgb(255, 255, 255);
            }
            QPushButton#btn_close:hover {
                background-color: rgb(212, 64, 39);
            }
            QPushButton#btn_sure {
                border: none;
                background: transparent;
                color: rgb(255, 255, 255);
                border-radius: 5px;
                border: solid 1px rgb(76, 169, 106);
                background-color: rgb(76, 169, 106);
            }
            QPushButton#btn_sure:hover {
                color: rgb(0, 0, 0);
            }
        ''')

    def setTitle(self, title):
        if title:
            self.lb_title.setText(title)

    def setWindowTitle(self, p_str):
        super(WindowNotify, self).setWindowTitle(p_str)
        self.setTitle(p_str)

    def title(self):
        return self.lb_title.text()

    def setTimeout(self, timeout):
        if isinstance(timeout, int):
            self._timeout = timeout
        return self

    def timeout(self):
        return self._timeout

    def setMainArea(self, layout: QLayout):
        self.widget_area.setLayout(layout)

    def on_btn_close_click(self):
        self.is_show = False
        QTimer.singleShot(100, self.on_animation_close)

    def on_btn_sure_click(self):
        self.on_btn_close_click()

    def show(self, content=None):
        self.timer_obj.stop()  # 停止定时器,防止第二个弹出窗弹出时之前的定时器出问题
        self.hide()  # 先隐藏
        self.move(self.start_pos)  # 初始化位置到右下角
        super(WindowNotify, self).show()
        return self

    # 显示动画
    def on_animation_start(self):
        self.is_show = True
        self.animation_obj.stop()  # 先停止之前的动画,重新开始
        self.animation_obj.setStartValue(self.pos())
        self.animation_obj.setEndValue(self.end_pos)
        self.animation_obj.start()
        # 弹出5秒后,如果没有焦点则弹回去
        self.timer_obj.start(self._timeout)
        # QTimer.singleShot(self._timeout, self.closeAnimation)

    # 关闭动画
    def on_animation_close(self):
        if self.hasFocus():
            # 如果弹出后倒计时5秒后还有焦点存在则失去焦点后需要主动触发关闭
            self.is_timeout = True
            # 如果有焦点则不关闭
            return
        self.is_show = False
        self.animation_obj.stop()
        self.animation_obj.setStartValue(self.pos())
        self.animation_obj.setEndValue(self.start_pos)
        self.animation_obj.start()

    # 动画结束
    def on_animation_end(self):
        if not self.is_show:
            self.close()
            self.timer_obj.stop()
            self.singal_closed.emit()

    # 设置焦点(好像没啥用,不过鼠标点击一下后,该方法就有用了)
    def enterEvent(self, event):
        super(WindowNotify, self).enterEvent(event)
        self.setFocus(Qt.MouseFocusReason)

    # 取消焦点
    def leaveEvent(self, event):
        super(WindowNotify, self).leaveEvent(event)
        self.clearFocus()
        if self.is_timeout:
            QTimer.singleShot(1000, self.on_animation_close)

# 流水布局，自动换行
class FlowLayout(QLayout):

    def __init__(self, parent=None, margin=5, spacing=10):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

# 复选多选框
class CheckComboBox(QComboBox):

    def __init__(self, items, edit=True, delimiter=';'):

        super(CheckComboBox, self).__init__()
        self.select = ""
        self.delimiter = delimiter
        self.items = items
        ############################################
        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(edit)
        self.lineEdit.textChanged.connect(self.onTextChanged)
        # self.lineEdit.setText(self.all_name)
        self.listWidget = QListWidget()

        for i, j in enumerate(self.items):
            item = QListWidgetItem()
            # item.setData(Qt.UserRole, j)
            checkBox = QCheckBox(j)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, checkBox)
            checkBox.stateChanged.connect(self.onStateChanged)

        self.setModel(self.listWidget.model())
        self.setView(self.listWidget)
        self.setLineEdit(self.lineEdit)

        self.setEditable(True)

    def onStateChanged(self, state: int):
        selectedContent = ""
        control = QObject.sender(self)
        # print(control.text())
        ########### 全选 ##############################
        # if control.text()==self.all_name:
        #     if control.isChecked():
        #         print('选中')
        #     else:
        #         print('未选中')
        ########### 获取 ###############################
        for i in range(self.listWidget.count()):  # 遍历
            item = self.listWidget.item(i)  # 获得item
            checkBox = self.listWidget.itemWidget(item)  # 找到item对应widget
            if checkBox.isChecked():

                if not selectedContent:
                    selectedContent = checkBox.text()
                else:
                    selectedContent = selectedContent + self.delimiter + checkBox.text()

        self.select = selectedContent
        # print(selectedContent)
        self.setCurrentText(selectedContent)

    def onTextChanged(self, text: str):
        # self.lineEdit.setText(text)
        '''
        点击空白处，下拉列表会进行收回，QLineEdit的数据将会被自动清空
        '''
        self.lineEdit.setText(self.select)

    def setPlaceholderText(self, text: str):
        self.lineEdit.setPlaceholderText(text)

    # def setCompleter(self,QCompleter):
    #
    #     self.lineEdit.setCompleter(QCompleter)

    def textList(self):
        if self.select:
            return self.select.split("%s" % self.delimiter)

    def mousePressEvent(self, QMouseEvent):
        super(CheckComboBox, self).mousePressEvent(QMouseEvent)
        # print(2222)

class ComboCheckBox(QComboBox):

    def __init__(self, items):
        super(ComboCheckBox, self).__init__()
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        # 选择的行数
        self.row_num_sel = 0
        # QCheckBox 容器
        self.cb_boxs = []
        # 展示内容
        self.le_show = QLineEdit()
        self.le_show.setReadOnly(True)
        self.lw_lists = QListWidget()
        self.addQCheckBox(0)
        self.cb_boxs[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.cb_boxs[i].stateChanged.connect(self.show)
        self.setModel(self.lw_lists.model())
        self.setView(self.lw_lists)
        self.setLineEdit(self.le_show)

        # 绑定信号槽

    def addQCheckBox(self, i):
        self.cb_boxs.append(QCheckBox())
        qItem = QListWidgetItem(self.lw_lists)
        self.cb_boxs[i].setText(self.items[i])
        self.lw_lists.setItemWidget(qItem, self.cb_boxs[i])

    def Selectlist(self):
        Outputlist = []
        for i in range(1, self.row_num):
            if self.cb_boxs[i].isChecked() == True:
                Outputlist.append(self.cb_boxs[i].text())
        self.row_num_sel = len(Outputlist)
        return Outputlist

    def show(self):
        show = ''
        Outputlist = self.Selectlist()
        self.le_show.setReadOnly(False)
        self.le_show.clear()
        for i in Outputlist:
            show += i + ';'
        if self.row_num_sel == 0:
            self.cb_boxs[0].setCheckState(0)
        elif self.row_num_sel == self.row_num - 1:
            self.cb_boxs[0].setCheckState(2)
        else:
            self.cb_boxs[0].setCheckState(1)
        self.le_show.setText(show)
        self.le_show.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.cb_boxs[i].setChecked(True)
        elif zhuangtai == 1:
            if self.row_num_sel == 0:
                self.cb_boxs[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.cb_boxs[i].setChecked(False)

# 工具栏按钮
class ToolButton(QToolButton):

    def __init__(self,icon,name):
        super(ToolButton,self).__init__()
        self.setIcon(icon)
        self.setText(name)
        self.setIconSize(QSize(32,32))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)

# 圆形展示
class CircularPicLabel(QLabel):

    def __init__(self,pic_file,pic_size=200,antialiasing=True,parent=None):
        '''
        :param size: 圆形裁剪大小
        :param antialiasing: 抗锯齿
        :param parent:
        '''
        super(CircularPicLabel, self).__init__(parent)
        self.setMaximumSize(pic_size, pic_size)
        self.setMinimumSize(pic_size, pic_size)
        self.radius = pic_size/2

        #####################核心实现#########################
        # 大小和控件一样
        self.target = QPixmap(self.size())
        # 填充背景为透明
        self.target.fill(Qt.transparent)
        # 加载图片并缩放和控件一样大
        p = QPixmap(pic_file).scaled(pic_size, pic_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter = QPainter(self.target)
        if antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)


        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        #**** 切割为圆形 ****#
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)


class SearchLineEdit2(QLineEdit):
    """创建一个可自定义图片的输入框。"""

    style = '''
            QPushButton {
            border-image: url(resource/search.png);
        }

        QLineEdit#SearchLine{
            margin-bottom: 1px;
            border: 4px solid #171719;
            border-radius: 10px;
            color: #555555;
            font: 75 9pt "黑体";
            background: #171719;
        }

        QLineEdit#SearchLine:pressed {
            color: #D0D0D1;
        }
    '''

    def __init__(self, parent=None):
        super(SearchLineEdit2, self).__init__(parent)
        self.setMinimumSize(218, 20)
        # with open('QSS/searchLine.qss', 'r') as f:
        self.setStyleSheet(self.style)

        self.button = QPushButton(self)
        self.button.setMaximumSize(13, 13)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))

        self.setTextMargins(3, 0, 19, 0)

        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addSpacerItem(self.spaceItem)
        # self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addSpacing(10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    def setButtonSlot(self, funcName):
        self.button.clicked.connect(funcName)


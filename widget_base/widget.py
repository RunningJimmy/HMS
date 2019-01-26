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


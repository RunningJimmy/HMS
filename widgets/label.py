'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: lable.py
@time: 2019-1-14 13:40
@desc: 标签，放置文字、图片等
'''

from widgets.bwidget import *

class HeadPortraitLabel(QLabel):

    def __init__(self,parent=None):
        super(HeadPortraitLabel,self).__init__(parent)
        self.setMaximumSize(48, 48)
        self.setMinimumSize(48, 48)
        self.radius = 24
        self.initUI()

    def initUI(self):
        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明
        # 加载图片并缩放和控件一样大
        p = QPixmap("head.jpg").scaled(48, 48, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        # 抗锯齿
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
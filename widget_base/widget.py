'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: widget.py
@time: 2019-1-23 9:13
@desc: 基础组件，无关业务
'''
from widget_base.common import *
from ctypes.wintypes import POINT
import ctypes.wintypes
from PyQt5.QtWinExtras import QtWin
import win32api
import win32con
import win32gui


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

class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved",      POINT),
        ("ptMaxSize",       POINT),
        ("ptMaxPosition",   POINT),
        ("ptMinTrackSize",  POINT),
        ("ptMaxTrackSize",  POINT),
    ]


class Window(QWidget):

    BorderWidth = 5

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 主屏幕的可用大小（去掉任务栏）
        self._rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)
        # 增加薄边框
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        if QtWin.isCompositionEnabled():
            # 加上 Aero 边框阴影
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

    def nativeEvent(self, eventType, message):
        retval, result = super(Window, self).nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # 获取鼠标移动经过时的坐标
            x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            # 判断鼠标位置是否有其它控件
            if self.childAt(x, y) != None:
                return retval, result
            if msg.message == win32con.WM_NCCALCSIZE:
                # 拦截不显示顶部的系统自带的边框
                return True, 0
            if msg.message == win32con.WM_GETMINMAXINFO:
                # 当窗口位置改变或者大小改变时会触发该消息
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                # 修改最大化的窗口大小为主屏幕的可用大小
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                # 修改放置点的x,y坐标为0,0
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0
            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                # 左上角
                if (lx and ty):
                    return True, win32con.HTTOPLEFT
                # 右下角
                if (rx and by):
                    return True, win32con.HTBOTTOMRIGHT
                # 右上角
                if (rx and ty):
                    return True, win32con.HTTOPRIGHT
                # 左下角
                if (lx and by):
                    return True, win32con.HTBOTTOMLEFT
                # 上
                if ty:
                    return True, win32con.HTTOP
                # 下
                if by:
                    return True, win32con.HTBOTTOM
                # 左
                if lx:
                    return True, win32con.HTLEFT
                # 右
                if rx:
                    return True, win32con.HTRIGHT
                # 标题
                return True, win32con.HTCAPTION
        return retval, result


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    btn = QPushButton('exit', w, clicked=app.quit)
    btn.setGeometry(10, 10, 100, 40)
    w.show()
    sys.exit(app.exec_())
'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: message.py
@time: 2019-1-23 16:04
@version：0.1
@desc: 消息框
'''

import base64
from .common import *

# 消息弹出框，指定时间自动关闭，且窗口不可移动
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
        # print(self.desktop_obj.screenGeometry().width(),
        #       self.desktop_obj.screenGeometry().height(),
        #       self.width(),
        #       self.height()
        #       )
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

    def show(self):
        self.timer_obj.stop()  # 停止定时器,防止第二个弹出窗弹出时之前的定时器出问题
        self.hide()  # 先隐藏
        self.move(self.start_pos)  # 初始化位置到右下角
        super(WindowNotify, self).show()
        self.on_animation_start()

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

class MessageBox(QMessageBox):

    def __init__(self, *args, count=9, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle('明州体检')
        self.count = count
        self.setStandardButtons(self.Close)  # 关闭按钮
        self.btn_close = self.button(self.Close)  # 获取关闭按钮
        self.btn_close.setText('确定(%s)' % count)
        self.btn_close.clicked.connect(self.close)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_timer_out)
        self._timer.start(1000)

    def on_timer_out(self):
        self.btn_close.setText('确定(%s)' % self.count)
        self.count -= 1
        if self.count <= 0:
            self._timer.stop()
            self.accept()
            self.close()

def mes_about(parent, message):
    MessageBox(parent, text=message).exec_()

def mes_warn(parent, message):
    button = QMessageBox.warning(parent, "明州体检", message, QMessageBox.Yes | QMessageBox.No)
    return button

#图标
class NotificationIcon:

    Info, Success, Warning, Error, Close = range(5)

    Types = {
        Info: None,
        Success: None,
        Warning: None,
        Error: None,
        Close: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.Info] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC5ElEQVRYR8VX0VHbQBB9e/bkN3QQU0FMBSEVYFcQ8xPBJLJ1FWAqOMcaxogfTAWQCiAVRKkgTgfmM4zRZu6QhGzL0p0nDPr17e7bt7tv14RX/uiV48MJgAon+8TiAMRtMFogaqUJxADPwRRzg67kl8+xbWJWANR40iPQSSFgtX/mGQkaDr56V3VAKgGos4s2JXwJoF3naMPvMS+SrpTHs032GwGkdF+DsFMVnJm/oyGGeHico0EjIjpYes+YMyVd6R/flfkpBWCCQ9zaZM2LZDfLMGXsZ5kdI/lYBmINgHHyyLd1mWdBbAFAM/GY7K2WYx1AeB4T6L1N9umbGxZ0qktATaEAdCps48D39oq/LwEw3U5CN92LfczJoewfT7MAywDCaEbAuxeLrh0zz4L+0e4aAJfGy+sP3IMxlH1vpMJoSMCJDXgWtJeJVc6ACs9HBBrYODCJAFdYvAmkPJxnNqMwYht7Bn+T/lGg3z4DGEd3RPhQ54DBvwAOVkeqagRXfTLjh+x7+8sALOtfHLuiYzWOAiLoKbD58mnIGbCmLxUepS6NQmYlUGE0JeCTTXT9JvA9E9sZgO5iIpoyc6/YzcqSwQzgGgBXB7oXpH9klpRSkxY1xW/b7Iu2zk34PILPnazCqEPAtTWA8iZ0HsOu9L0bw4DzCJeNocMGNDpQ3IKO+6NUiJ4ysZNiBv5I3zPnmJmG5oM+wbS+9+qkvGi7NAXGmeUy0ioofa+XA0jH0UaMKpdRWs/adcwMqfV/tenqpqHY/Znt+j2gJi00RUzA201dXaxh9iZdZloJS+9H1otrkbRrD5InFqpPskxEshJQ468CkSmJC+i1HigaaxCAuCljgoDhwPdOjf7rFVxxuJrMkXScjtKc1rOLNpJk6nii5XmYzbngzlZn+RIb40kPJPTBYXUt6VEDJ8Pi6bWpNFb/jFYY6YGpDeKdjBmTKdMcxDGEmP73v2a2Gr/NOycGtglQZ/MPzEqCMLGckJEAAAAASUVORK5CYII=')))
        cls.Types[cls.Success] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACZUlEQVRYR8VXS3LTQBDtVsDbcAPMCbB3limkcAKSG4QFdnaYE2BOQLKzxSLJCeAGSUQheSnfwLmB2VJhXmpExpFHI2sk2RWv5FJPv9evP9NieuIfPzE+VSJw8qt3IMDvmahDoDYxt2UAACXMWIIowR5ffn8TJbaBWRE4CXvHAH9RgKXOgQUI48CfXZbZbiTw8Xe/w3d0zkydMkem91IZpyWOJu5sUXS+kEAqt3B+MNOLOuDqDEBLxxFHk7eza5MfIwEJDjhXTYD1s8zinYlEjsCD7FdNI9cJpEq0RFdPR47AMOzLCn69zegz6UgCP+pmfa8RSKudnPNdgCufTOLDxJtdPP7PoA1Cd8HEL5sSUCCD0B0x8bc1f8Bi6sevcgS2VXh6hMOwDz0gsUddNaxWKRjeuKfE/KlJ9Dq4UYH/o/Ns6scj+bgiMAjdayb26xLQwTfVEwg3gRcf6ARq578KuLo7VDc8psCQqwfjr4EfjYvkrAquFJ56UYpdSkAZSmNd1rrg0leOQFELgvA58OJTxVyRaAJORPOpF6UXnFUR5sDiXjs7UqsOMGMRlrWhTkJXpFL3mNrQZhA1lH3F0TiI5FurUQyMpn58VjhkSqQA4Tbw4nSVW6sBU5VXktXSeONlJH3s8jrOVr9RgVSFuNcWfzlh5n3LoKzMAPxxWuiULiQpiR2sZNnCyzIuWUr5Z1Ml0sgdHFZaShVDuR86/0huL3VXtDk/F4e11vKsTHLSCeKx7bYkW80hjLOrV1GhWH0ZrSlyh2MwdZhYfi8oZeYgLBmUiGd8sfVPM6syr2lUSYGaGBuP3QN6rVUwYV/egwAAAABJRU5ErkJggg==')))
        cls.Types[cls.Warning] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACmElEQVRYR8VXTW7TUBD+xjYSXZFukOIsSE9AskNJJMoJmq4r7OYEwAkabhBOkB/Emt4gVIojdpgbpIumEitX6gKB7UHPkauXxLHfc4F6Z3l+vvnmm/fGhAd+6IHzQwvA9cfOITMfAdQAcx1EdVEAM/tEFADsWyaPn57MfdXClABcT1qnzHSWJiwMzrwgoF91vXGRbS6AH59ajd8hDYmoURQo67tgxoij42rv62KX/04Agu44xmciVMokT32YERgGjquvZ1+y4mQCWPUa0/sk3vQlwqssEFsAVrQbU4XKL/ai2+5PPK6waQ4AOsoDnDARh83NdmwBuJq0fQI9L6p+L7rd3+/5gbAToMPI+FbkIzRRc72mbLcGIFE7jGFRIPHddmZrvstJh1X8CHGv6sxHqe1GkPYCoGcqgcoCAPPCdr2DLQC6wqMoPEj7qdqCNKllxs30sLpjYDluDUDGG5XqhY2sal3w4PiD7c7fJnHShMtJR8zpy/8CALiwndnhBgD1/t+XAXkaZAaUVHwnHulg0W6BNEWlAQD8zna8gQB0Ne70iXCm2j55jCUAei1gxvuaO+uXAcDg7zXHSy640iKUAehOEDJFqDmGQkiPLO5Fv+KADXOqvCuIsrPGsIyQdHou22YeRMJgOdHTQTkAfGk7XrLKrWlAvOhcRgBfWiZ3RQti0zxXuUFXCXMuo0TRitfxugjbIxC5RYzI6s9kIGFh+KLOpiW22id5AUuI8IaisFG4kCQg/sFKJgtPLix3KWXGeRETRbQDuCFCV2spTYMm+2FEI1WBbYIRPTeiqFtqLZeDraaD+qrbkpgQAvfl1WsXU0p/RjIjYYhTkNFgcCVlRlRKoAAc+5aF0V//NVPoc2kTLQZKZ8lx/AMXBmMwuXUwOAAAAABJRU5ErkJggg==')))
        cls.Types[cls.Error] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACrklEQVRYR82XW27aQBSG/4PtiNhIpStouoImKwjZAV1B07coWCpZQcgK6kh2lLeSFZSsIOwgdAdkBaUSEBQDpxpjU9vM+EJR03nDzJz/mzm3GcIrD3plfZQCeD47O1ho2jERNRmoE9AQG2BgBGBAwIiZe5Zh3JPjiG+5oxCAEF5q2iWITnMtRhOYu5XF4mr/9naYtSYXYGLbHQCXhYVTEwlom657rVqvBOB2uz71/a+ldq1SYe6ahnEhc4sSYGzbfQKOt915eh0D/ZrrnqS/SwEmrVYXRJ92Jb4OC+C65rrtuN0NgIltNwF837V4zN5Hy3V70e9NgFZrCKJ3CQDmJ9MwDsW36XzeB/AhA/CHqeuN2WxWX2paX2JraHneeynA+Pz8lCqVbxLjV5brimxAEJxqiEA8CjZVBvFy+bl2c9MV9hInoAw85qFpGEeRYQVEQjzMokcQHWxsiPne8jzh6j8AodGfyqNlHpiGcaKAkIk/gChwm2yYuv5W2FqfwLNtN5bAQ2bwySB83zENo50A8/1McaFRAU72XVek+mpk+D/JlIKI/xkee654uCbIhjVAqZIrgSgpLhiCwN4OAEj4vEB2yDybBCjsAol4ZD0nRdMQSRcUCsKUeNSw4o2mKMRGEOamoVx8FXDZKVosDYNMUHXAsBRnppo8RQcbpTgIGEkhykpFjnWxzGhPQYxt2yHgS/oIlKVYTJxImpG482nz+VG1Wh1N84pMCCGa0ULXHwmoJwCYnyzPW5fn/68dh7EgPbrMMl3gz7gro+n/7EoWD7w4a96l1NnJ1Yz5Lt6wCgFEk0r1CIkbiPnC9DxH5aHcd4FYGD5MOqVOg/muslh0/vphkm63k5eXZvA0I6qD+ZCI3jDzLxANiHn1NNvb6+30aVYgwLeeUsgFW1svsPA3Ncq4MHzVeO8AAAAASUVORK5CYII=')))
        cls.Types[cls.Close] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeElEQVQ4T2NkoBAwUqifgboGzJy76AIjE3NCWmL0BWwumzV/qcH/f38XpCfHGcDkUVwAUsDw9+8GBmbmAHRDcMlheAGbQnwGYw0DZA1gp+JwFUgKZyDCDQGpwuIlrGGAHHAUGUCRFygKRIqjkeKERE6+oG5eIMcFAOqSchGwiKKAAAAAAElFTkSuQmCC')))

    @classmethod
    def icon(cls, ntype):
        return cls.Types.get(ntype)


class NotificationItem(QWidget):

    closed = pyqtSignal(QListWidgetItem)

    def __init__(self, title, message, item, *args, ntype=0, callback=None, **kwargs):
        super(NotificationItem, self).__init__(*args, **kwargs)
        self.item = item
        self.callback = callback
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.bgWidget = QWidget(self)  # 背景控件, 用于支持动画效果
        layout.addWidget(self.bgWidget)

        layout = QGridLayout(self.bgWidget)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        # 标题左边图标
        layout.addWidget(
            QLabel(self, pixmap=NotificationIcon.icon(ntype)), 0, 0)

        # 标题
        self.labelTitle = QLabel(title, self)
        font = self.labelTitle.font()
        font.setBold(True)
        font.setPixelSize(22)
        self.labelTitle.setFont(font)

        # 关闭按钮
        self.labelClose = QLabel(
            self, cursor=Qt.PointingHandCursor, pixmap=NotificationIcon.icon(NotificationIcon.Close))

        # 消息内容
        self.labelMessage = QLabel(
            message, self, cursor=Qt.PointingHandCursor, wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
        font = self.labelMessage.font()
        font.setPixelSize(20)
        self.labelMessage.setFont(font)
        self.labelMessage.adjustSize()

        # 添加到布局
        layout.addWidget(self.labelTitle, 0, 1)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        layout.addWidget(self.labelClose, 0, 3)
        layout.addWidget(self.labelMessage, 1, 1, 1, 2)

        # 边框阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setColor(QColor(0, 0, 0, 25))
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)

        self.adjustSize()

        # 5秒自动关闭
        self._timer = QTimer(self, timeout=self.doClose)
        self._timer.setSingleShot(True)  # 只触发一次
        self._timer.start(5000)

    def doClose(self):
        try:
            # 可能由于手动点击导致item已经被删除了
            self.closed.emit(self.item)
        except:
            pass

    def showAnimation(self, width):
        # 显示动画
        pass

    def closeAnimation(self):
        # 关闭动画
        pass

    def mousePressEvent(self, event):
        super(NotificationItem, self).mousePressEvent(event)
        w = self.childAt(event.pos())
        if not w:
            return
        if w == self.labelClose:  # 点击关闭图标
            # 先尝试停止计时器
            self._timer.stop()
            self.closed.emit(self.item)
        elif w == self.labelMessage and self.callback and callable(self.callback):
            # 点击消息内容
            self._timer.stop()
            self.closed.emit(self.item)
            self.callback()  # 回调

    def paintEvent(self, event):
        # 圆角以及背景色
        super(NotificationItem, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)
        painter.fillPath(path, Qt.white)


class NotificationWindow(QListWidget):

    _instance = None

    def __init__(self, *args, **kwargs):
        super(NotificationWindow, self).__init__(*args, **kwargs)
        self.setSpacing(20)
        self.setMinimumWidth(412)
        self.setMaximumWidth(412)
        QApplication.instance().setQuitOnLastWindowClosed(True)
        # 隐藏任务栏,无边框,置顶等
        self.setWindowFlags(self.windowFlags() | Qt.Tool |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 去掉窗口边框
        self.setFrameShape(self.NoFrame)
        # 背景透明
        self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 不显示滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕高宽
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.setMinimumHeight(rect.height())
        self.setMaximumHeight(rect.height())
        self.move(rect.width() - self.minimumWidth() - 18, 0)

    def removeItem(self, item):
        # 删除item
        w = self.itemWidget(item)
        self.removeItemWidget(item)
        item = self.takeItem(self.indexFromItem(item).row())
        w.close()
        w.deleteLater()
        del item

    @classmethod
    def _createInstance(cls):
        # 创建实例
        if not cls._instance:
            cls._instance = NotificationWindow()
            cls._instance.show()
            NotificationIcon.init()

    @classmethod
    def info(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Info, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def success(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Success, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def warning(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Warning, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def error(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Error, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)

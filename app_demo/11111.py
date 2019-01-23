from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class Label(QLabel):

    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.radius = 16
        self.initUI()

    def initUI(self):
        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明
        # 加载图片并缩放和控件一样大
        p = QPixmap("head.jpg").scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
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



class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(Label(self))
        layout.addWidget(Label(self, antialiasing=False))
        self.setStyleSheet("background: black;")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
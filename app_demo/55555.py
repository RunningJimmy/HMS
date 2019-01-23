import sys

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QLabel

from  app_demo import QtNinePatch


class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        #.9 格式的图片
        self.image = QImage(r'F:\HMS\app_demo\xxxx.png')

    def showEvent(self, event):
        super(Label, self).showEvent(event)
        pixmap = QtNinePatch.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)

    def resizeEvent(self, event):
        super(Label, self).resizeEvent(event)
        pixmap = QtNinePatch.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)


app = QApplication(sys.argv)
w = Label()
w.resize(400, 200)
w.show()

sys.exit(app.exec_())
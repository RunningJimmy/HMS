from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QPushButton,
                             QVBoxLayout,
                             QTableWidgetItem)
from PyQt5.QtGui import QPixmap, QPainter, QImage, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QRect, QPoint, QSize, Qt


# 有预览框<br># 908204694@qq.com<br>#


def on_htmlButton_clicked():
    printer = QPrinter(QPrinter.HighResolution)
    # /* 打印预览 */
    preview = QPrintPreviewDialog(printer, widget)
    preview.paintRequested.connect(printHtml)

    #
    #   显示 预览框
    #
    # preview.exec()
    preview.exec_()


def printHtml(printer):
    html = """<html>
    <head></head>
    <body>
        <h1>55555</h1><b>bold</b><h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b><h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b><h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b><h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
        <h1>55555</h1><b>bold</b>
    </body>
    </html>"""

    textDocument = QTextDocument()
    textDocument.setHtml(html)
    # textDocument.print(printer)
    textDocument.print_(printer)


def on_picButton_clicked():
    printer = QPrinter(QPrinter.HighResolution)
    # /* 打印预览 */
    preview = QPrintPreviewDialog(printer, widget)

    """
     * QPrintPreviewDialog类提供了一个打印预览对话框，里面功能比较全，
     * paintRequested(QPrinter *printer)是系统提供的，
     * 当preview.exec()执行时该信号被触发，
     * plotPic(QPrinter *printer)是用户自定义的槽函数，图像的绘制就在这个函数里。
    """
    preview.paintRequested.connect(plotPic)

    preview.exec()  # /* 等待预览界面退出 */


def plotPic(printer):
    painter = QPainter(printer)
    image = QPixmap()
    image = widget.grab(QRect(QPoint(50,50),
                              QSize(widget.size().width(),
                                    widget.size().height()
                                    )
                              )
                        )  # /* 绘制窗口至画布 */
    # QRect
    rect = painter.viewport()
    # QSize
    size = image.size()
    size.scale(rect.size(), Qt.KeepAspectRatio)  # //此处保证图片显示完整
    painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
    painter.setWindow(image.rect())

    painter.drawPixmap(0, 0, image)  # /* 数据显示至预览界面 */


import sys

app = QApplication(sys.argv)
tablewidget = QTableWidget()
## 设置列数
tablewidget.setColumnCount(4)
tablewidget.horizontalHeader().setDefaultSectionSize(150)

## QStringList在PyQt5
header = ["name", "last modify time", "type", "size"]

tablewidget.setHorizontalHeaderLabels(header)
tablewidget.insertRow(0)
tablewidget.insertRow(0)

pItem1 = QTableWidgetItem("aa")
pItem2 = QTableWidgetItem("bb")
pItem3 = QTableWidgetItem("cc")
pItem4 = QTableWidgetItem("dd")
tablewidget.setItem(0, 0, pItem1)
tablewidget.setItem(0, 1, pItem2)
tablewidget.setItem(0, 2, pItem3)
tablewidget.setItem(0, 3, pItem4)

tablewidget.setMinimumSize(800, 600)

button = QPushButton('打印界面')
button.clicked.connect(on_picButton_clicked)

button_txt = QPushButton('打印文字')
button_txt.clicked.connect(on_htmlButton_clicked)

widget = QWidget()
layout = QVBoxLayout(widget)
layout.addWidget(button)
layout.addWidget(button_txt)
layout.addWidget(tablewidget)
widget.show()

sys.exit(app.exec_())
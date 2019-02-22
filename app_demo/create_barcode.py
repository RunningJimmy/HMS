'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: create_barcode.py
@time: 2019-2-21 16:52
@version：0.1
@desc: 
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class BarcodeWidget(QWidget):

    def __init__(self,parent=None):
        super(BarcodeWidget,self).__init__(parent)
        lt_main = QHBoxLayout()


class SerialnoLabel(QLabel):

    def __init__(self,parent=None):
        super(SerialnoLabel,self).__init__(parent)
        font = QFont('C39HrP24DhTt')
        font.setPointSize(36)
        self.setFont(font)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("NSAViewer")

    window = SerialnoLabel()
    window.show()
    app.exec_()
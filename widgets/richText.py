from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class RichTextWidget(QWidget):

    def __init__(self,parent=None):
        super(RichTextWidget,self).__init__(parent)
        self.initUI()


    def initUI(self):
        lt_main = QVBoxLayout()
        self.lt_top = QHBoxLayout
        # 功能区
        self.tb_tool1 = QToolBar()
        self.action_print = QAction()

        self.tb_tool1.addAction(QAction())
        rt = QTextEdit()
        lt_main.addWidget(rt)
        self.setLayout(lt_main)

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = RichTextWidget()
    ui.show()
    app.exec_()
from widgets.richText import RichTextWidget
from widgets.pic_widget import PicWidget

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = PicWidget()
    ui.show()
    app.exec_()
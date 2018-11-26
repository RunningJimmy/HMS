from widgets.cwidget import *

class NCD_UI(DirTabWidget):

    def __init__(self,title):
        # 就诊预约
        nodes= ['疾病筛查','慢病档案','预约就诊']
        super(NCD_UI,self).__init__(title,nodes)


    def addTab(self,title):
        super(NCD_UI, self).addTab(title)
        if title=='疾病筛查':
            from .doubtful import Doubtful
            widget=Doubtful()
            self.rwidget.addPage(widget,Icon('疑似慢病'),title)


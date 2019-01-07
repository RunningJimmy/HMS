from widgets.cwidget import *


# C13 呼气试验管理
class BreathManager(DirTabWidget):

    def __init__(self):
        #nodes = ['呼气试验', '结果录入', '历史查询', '工作量']
        nodes = ['呼气试验']
        super(BreathManager,self).__init__('采血台',nodes)
        self.addTab('呼气试验')

    def addTab(self,title):
        super(BreathManager, self).addTab(title)
        if title=='呼气试验':
            from C13.breathcheck import BreathCheck
            self.breathCheck = BreathCheck()
            self.rwidget.addPage(self.breathCheck, Icon('呼气室'), '呼气室')
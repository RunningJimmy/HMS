from widgets.utils import *

# 网页嵌入到窗口中
class BrowserWidget(QWidget):

    status = False  # 是否被打开

    def __init__(self,title,url,parent=None):
        super(BrowserWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.url = url
        self.show()
        self.initUI()

    def initUI(self):
        lt_main = QHBoxLayout()
        self.browser = CefWidget(self)
        lt_main.addWidget(self.browser)
        self.setLayout(lt_main)

    # 载入必须在整体控件show后面，不是仅仅show后面
    def showMaximized(self):
        super(BrowserWidget,self).showMaximized()
        self.browser.embedBrowser(self.url)

    def closeEvent(self, *args, **kwargs):
        self.status = True
        super(BrowserWidget, self).closeEvent(*args, **kwargs)

class CriticalValueUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '危急值上报'
        url = "http://10.8.200.67:8001/Login.aspx"
        super(CriticalValueUI,self).__init__(title,url,parent)

class OaUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '集团OA'
        url = "http://sso.auxgroup.com/login?service=https://newoa.auxgroup.com/index.jsp"
        super(OaUI,self).__init__(title,url,parent)

class PhonePlatUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '电话平台'
        url = "http://10.8.103.211:8088/ec2"
        super(PhonePlatUI,self).__init__(title,url,parent)

class XiHe_HealthUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '希和检后'
        url = "http://10.7.200.198:4415/Login.aspx"
        super(XiHe_HealthUI,self).__init__(title,url,parent)

class TaiWan_HealthUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '台湾检后'
        url = "http://10.7.200.57:8080/aux_medical/admin/index.php"
        super(TaiWan_HealthUI,self).__init__(title,url,parent)

class MediaUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '多媒体小屏'
        url = "http://10.8.200.104/admin/index/logon/"
        super(MediaUI,self).__init__(title,url,parent)

class AdverseEventUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '不良事件上报'
        url = "http://10.155.215.162/"
        super(AdverseEventUI,self).__init__(title,url,parent)

class GoodEvaluateUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '集团好评率'
        url = "http://10.8.200.67:9001/ApplauseRate/ApplauseRate.aspx?"
        super(GoodEvaluateUI,self).__init__(title,url,parent)

class WeiXinUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '微信后台'
        url = "http://app.nbmzyy.com/admin/"
        super(WeiXinUI,self).__init__(title,url,parent)

class WebsiteBackUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '官网后台'
        url = "http://10.7.200.127/auth/logout.do?lang=zh_CN"
        super(WebsiteBackUI,self).__init__(title,url,parent)

class WebsiteFrontUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '官网主页'
        url = "http://10.7.200.127/"
        super(WebsiteFrontUI,self).__init__(title,url,parent)

class AssetUI(BrowserWidget):

    def __init__(self,parent=None):
        title = '图特资产'
        url = "http://10.7.200.56/Home/Main/"
        super(AssetUI,self).__init__(title,url,parent)
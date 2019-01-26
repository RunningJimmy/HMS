'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: widget_demo.py
@time: 2019-1-23 15:01
@version：0.1
@desc: 基础组件 调用demo
'''

from widget_base import *
from widget_base.browser import cef

# 浏览器
def demo_open_url(url,title):
    # To shutdown all CEF processes on error
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url=url,window_title=title)
    cef.MessageLoop()
    cef.Shutdown()

# 下拉多选按钮组合
def demo_button():
    window = QWidget()
    layout = QHBoxLayout(window)
    b1 = ComCheckBox(["a","b","c","d","e"])
    layout.addWidget(b1)

    return window

# 消息弹出框
def WindowNotify_demo():
    window = QWidget()
    notify = WindowNotify(parent=window)
    layout = QHBoxLayout(window)
    b1 = QPushButton(
        "弹窗1", window, clicked=notify.show)
    layout.addWidget(b1)

    return window

def callback():
    print('回调点击')

def message_demo():
    w = QWidget()
    layout = QHBoxLayout(w)

    layout.addWidget(QPushButton(
        'Info', w, clicked=lambda: NotificationWindow.info('提示', '这是一条会自动关闭的消息', callback=callback)))
    layout.addWidget(QPushButton(
        'Success', w, clicked=lambda: NotificationWindow.success('提示', '这是一条会自动关闭的消息', callback=callback)))
    layout.addWidget(QPushButton(
        'Warning', w, clicked=lambda: NotificationWindow.warning(
            '提示',
            '这是提示文案这是提示文案这是提示文案这是提示文案。',
            callback=callback)))
    layout.addWidget(QPushButton(
        'Error', w, clicked=lambda: NotificationWindow.error(
            '提示',
            '<html><head/><body><p><span style=" font-style:italic; color:teal;">这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案</span></p></body></html>',
            callback=callback)))

    return w

if __name__ == "__main__":
    import sys
    import cgitb
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)
    #ui = WindowNotify_demo()
    ui = message_demo()
    #ui = demo_button()
    ui.show()
    sys.exit(app.exec_())
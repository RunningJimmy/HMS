'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: camera.py
@time: 2019-1-28 21:36
@version：0.1
@desc:
'''

'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: hms(健康管理系统)
@file: camera.py
@time: 2018-12-29 20:49
@desc:摄像头/视频读取模块
'''

from widget_base.common import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

try:
    import cv2
except Exception as e:
    cv2 = None
    print("载入模块cv2 失败，信息：%s" %e)


class CameraLabel(QLabel):

    # 通过Opencv模块来实现
    # 优点：读标准摄像头、读非标摄像头、读写视频、处理图片等
    # 缺点：1、对XP支持不好 2、多个摄像头同时读取(不能插在同一个Hub上)

    def __init__(self):
        super(CameraLabel, self).__init__()
        self.initParas()
        # 图片自适应label大小
        self.setScaledContents(True)

    # 初始化默认参数
    def initParas(self):
        self.resize(320, 240)
        self.setScaledContents(True)
        # self.show_width = 320
        # self.show_height = 240
        self.show_fps = 24

    # 设置显示参数
    def setShowSize(self,width=320,height=240,fps=24):
        '''
        :param width: 宽度
        :param height: 高度
        :param fps: 每秒帧数
        :return: None
        '''
        # self.show_width = width
        # self.show_height = height
        self.resize(width,height)
        self.setScaledContents(True)
        self.show_fps = fps

    # 设置图片大小
    def setPicSize(self,width:int,height:int):
        self.camera_obj.set(cv2.CAP_PROP_FRAME_WIDTH, width)    # 宽度
        self.camera_obj.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 高度

    # 打开摄像头
    def on_camera_open(self,camera_index=0):
        if not cv2:
            print("未找到模块：cv2")
            self.camera_obj = None
            return
        try:
            self.camera_obj = cv2.VideoCapture(camera_index)
            self.setPicSize(768,576)
            print("摄像头宽：%s,高：%s " %(self.camera_obj.get(cv2.CAP_PROP_FRAME_WIDTH),self.camera_obj.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            # 想要修改参数前请记住你摄像头参数的初始值;
            # 参数被改动了，是无法自动恢复到初始值的;
            # 除非特别需要，否则不要随意修改这些参数。
            # self.camera_obj.set(cv2.CAP_PROP_FRAME_WIDTH, self.show_width)    # 宽度
            # self.camera_obj.set(cv2.CAP_PROP_FRAME_HEIGHT, self.show_height)  # 高度
            # self.camera_obj.set(cv2.CAP_PROP_FPS, 30)                         # 帧数
            # self.camera_obj.set(cv2.CAP_PROP_BRIGHTNESS, 1)                   # 亮度
            # self.camera_obj.set(cv2.CAP_PROP_CONTRAST, 40)                    # 对比度
            # self.camera_obj.set(cv2.CAP_PROP_SATURATION, 50)                  # 饱和度
            # self.camera_obj.set(cv2.CAP_PROP_HUE, 50)                         # 色调
            # self.camera_obj.set(cv2.CAP_PROP_EXPOSURE, 50)                    # 曝光
            self.on_camera_start()
        except Exception as e:
            print("打开摄像头出错：%s" %e)
            self.camera_obj = None

    # 开始图像传输，采用线程定时方式
    def on_camera_start(self):
        self.timer_obj = QTimer(self)
        self.timer_obj.timeout.connect(self.on_camera_show)
        self.timer_obj.start(1000 / self.show_fps)

    def on_camera_show(self):
        if not self.camera_obj.isOpened():
            self.setText('打开失败，请检查配置！')
            self.setStyleSheet('''font: 75 14pt '黑体';color: rgb(204, 0, 0);''')
            return
        image = self.on_camera_read()
        if image:
            self.setPixmap(QPixmap.fromImage(image, Qt.AutoColor))

    # 读取图像
    def on_camera_read(self):
        # 按帧读取视频 其他方法
        # self.camera_obj.retrieve()
        ret,frame = self.camera_obj.read()
        # ret是布尔值 含义：如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。
        # frame就是每一帧的图像，是个三维矩阵
        if ret:
            # frame = cv2.flip(frame, flipCode=-1)  # 左右翻转,使用笔记本电脑摄像头才有用。
            # flipCode：翻转方向：1：水平翻转；0：垂直翻转；-1：水平垂直翻转
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ##############处理旋转#####################################
            # rows,cols,count = frame.shape
            # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
            # frame = cv2.warpAffine(frame, M, (cols, rows))
            image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888)
            # image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
            return image
        else:
            self.timer_obj.stop()
            return

    # 暂停
    def on_camera_stop(self):
        cv2.waitKey(0)

    # 拍照
    def on_camera_take(self,name):
        image = self.on_camera_read()
        if image:
            image.save(name)
            return image

    # 关闭摄像头
    def deleteLater(self):
        self.timer_obj.stop()
        self.camera_obj.release()
        super(CameraLabel, self).deleteLater()

    # 提供关闭接口
    def on_camera_close(self):
        self.timer_obj.stop()
        self.camera_obj.release()


# 带一寸照截图功能的摄像头
class CameraOneInch(CameraLabel):

    def __init__(self,rect=(105,129)):
        super(CameraOneInch,self).__init__()
        self.rect_select = rect
        self.mouse_pos = (self.width()/2,self.height()/2)
        # 是否暂停
        self.is_stop = False

    def setSelectRect(self,rect:tuple):
        self.rect_select = rect

    def mouseMoveEvent(self, QMouseEvent):
        self.setMouseTracking(True)                         # 鼠标形状变化
        super(CameraOneInch, self).mouseMoveEvent(QMouseEvent)
        pos = QMouseEvent.pos()
        if not self.is_stop:
            self.mouse_pos = (pos.x(),pos.y())

    # 双击 取消 鼠标跟踪，
    def mouseDoubleClickEvent(self, *args, **kwargs):
        super(CameraOneInch,self).mouseDoubleClickEvent(*args, **kwargs)
        self.is_stop = not self.is_stop

    def paintEvent(self, QPaintEvent):
        # 绘制工作在paintEvent的方法内部完成
        # 先绘制父对象内容，
        super(CameraOneInch,self).paintEvent(QPaintEvent)
        # 再绘制自身
        painter = QPainter(self)
        # QPainter负责所有的绘制工作:在它的begin()与end()间放置了绘图代码。
        # 实际的绘制工作由drawText()方法完成。
        painter.begin(self)
        self.drawText(QPaintEvent, painter)
        painter.end()

    def drawText(self, event, painter):
        # 反走样
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 设置画笔颜色、宽度
        painter.setPen(QPen(QColor(0, 160, 230), 2))
        # 根据鼠标位置画出矩形框
        axis_x, axis_y, rect_width, rect_height = calculate_rect((self.width(),self.height()),self.mouse_pos,self.rect_select)
        painter.drawRect(axis_x, axis_y, rect_width, rect_height)

    # 拍照，只拍一寸照大小，重载
    def on_camera_take(self,filename=None):
        image = self.on_camera_read()
        if image:
            tmp = image.copy(calculate_rect((self.width(), self.height()), self.mouse_pos, self.rect_select))
            tmp.save(filename)
            return tmp

# 实际是一个9宫格 => 3*3 象限 ,不能溢出边界
def calculate_rect(widget_size:tuple,mouse_point:tuple,rect_size:tuple):
    '''
    :param widget_size:  图像窗口大小
    :param mouse_point:  矩形中心位置即鼠标的位置
    :param rect_size:    矩形大小
    :return:右下角坐标位置
    '''
    # 解析参数
    widget_width,widget_height = widget_size
    mouse_x,mouse_y = mouse_point
    rect_width,rect_height = rect_size
    # 根据矩形左下角的坐标位置 处理溢出问题得到校正后真实的左下角坐标位置
    # axis_x_tmp = mouse_x - rect_width / 2        # 距离Y轴距离，即矩形框距离窗体边框的水平距离，左边距
    # axis_y_tmp = mouse_y - rect_height / 2       # 距离X轴距离，即矩形框距离窗体边框的垂直距离，下边距
    # axis_x_max = widget_width - rect_width       # 距离Y轴距离，左边距,最大距离
    # axis_y_max = widget_height - rect_height     # 距离X轴距离，下边距,最大距离
    axis_x = calculate_range(mouse_x - rect_width / 2, 0, widget_width - rect_width)
    axis_y = calculate_range(mouse_y - rect_height / 2, 0, widget_height - rect_height)

    return axis_x,axis_y,rect_width,rect_height

# 三段式求值：
# 若当前值比最小值小，则返回最小值
# 若当前值比最大值大，则返回最大值
# 若介于最小值和最大值之间，则返回自身
def calculate_range(value:float,range_min:int,range_max:int):
    '''
    :param value:当前值
    :param range_min:最小值
    :param range_max:最大值
    :return:int
    '''
    if value < range_min:
        return range_min
    elif range_min < value < range_max:
        return value
    else:
        return range_max

class CameraWidget(QWidget):

    def __init__(self,parent=None):
        super(CameraWidget,self).__init__(parent)
        self.setFixedSize(300,200)
        self.initUI()
        self.initSignal()


    def initSignal(self):
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_take.clicked.connect(self.on_btn_take_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)
        self.btn_close.clicked.connect(self.on_btn_close_click)

    def initUI(self):
        lt_main = QVBoxLayout()
        lt_main.setContentsMargins(0, 0, 0, 0)
        self.camera_ui = CameraLabel()
        widget_setup = QWidget()
        lt_extension = QHBoxLayout()
        self.btn_start = QPushButton('启动')
        self.btn_start.setDisabled(False)
        self.btn_stop = QPushButton('暂停')
        self.btn_stop.setDisabled(True)
        self.btn_close = QPushButton('关闭')
        self.btn_take = QPushButton('拍照')
        self.btn_setup = QPushButton('设置')
        lt_extension.addWidget(self.btn_start)
        lt_extension.addWidget(self.btn_stop)
        lt_extension.addWidget(self.btn_close)
        lt_extension.addWidget(self.btn_take)
        lt_extension.addWidget(self.btn_setup)
        widget_setup.setLayout(lt_extension)

        # 添加主布局
        lt_main.addWidget(self.camera_ui)
        lt_main.addWidget(widget_setup)
        self.setLayout(lt_main)

    # 打开摄像头
    def on_btn_start_click(self):
        self.camera_ui.on_camera_open()
        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)

    # 拍照
    def on_btn_take_click(self):
        filename = desktop("%s.png" %cur_timestamp())
        print(filename)
        self.camera_ui.on_camera_take(filename)

    # 关闭摄像头
    def on_btn_close_click(self):
        self.camera_ui.on_camera_close()

    # 暂停读取 摄像头内容
    def on_btn_stop_click(self):
        self.camera_ui.on_camera_stop()
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)

# Qt自带的摄像头模块
class CameraDefaultWidget(QWidget):

    def __init__(self,parent=None):
        super(CameraDefaultWidget,self).__init__(parent)
        self.initUI()
        self.initParas()
        self.cb_camera_selector.currentIndexChanged.connect(self.on_camera_select)
        self.btn_stop.clicked.connect(self.on_camera_stop)
        self.btn_start.clicked.connect(self.on_camera_start)
        self.btn_take.clicked.connect(self.on_camera_take)
        # 特殊变量

    def initUI(self):
        lt_main = QVBoxLayout()
        # 摄像头 展示
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('摄像头')
        # 设置取景器
        self.viewfinder = QCameraViewfinder()
        # self.viewfinder.show()
        lt_top.addWidget(self.viewfinder)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)
        # 摄像头 社遏制
        lt_middle = QHBoxLayout()
        gp_middle  = QGroupBox('设置')
        self.cb_camera_selector = QComboBox()
        self.cb_camera_degree = QComboBox()
        self.cb_camera_degree.addItems(['0','90','180','270'])
        lt_middle.addWidget(QLabel("切换摄像头："))
        lt_middle.addWidget(self.cb_camera_selector)
        lt_middle.addWidget(QLabel("旋转角度："))
        lt_middle.addWidget(self.cb_camera_degree)
        lt_middle.addStretch()
        gp_middle.setLayout(lt_middle)

        lt_bottom = QHBoxLayout()
        gp_bottom = QGroupBox('功能栏')
        self.btn_start = QPushButton('启动')
        self.btn_stop = QPushButton('停止')
        self.btn_take = QPushButton('拍照')
        lt_bottom.addWidget(self.btn_start)
        lt_bottom.addWidget(self.btn_stop)
        lt_bottom.addWidget(self.btn_take)
        lt_bottom.addStretch()
        gp_bottom.setLayout(lt_bottom)
        # 添加布局
        lt_main.addWidget(gp_top)
        lt_main.addWidget(gp_middle)
        lt_main.addWidget(gp_bottom)
        self.setLayout(lt_main)

    def initParas(self):
        self.cb_camera_selector.addItems([QCamera.deviceDescription(c) for c in QCamera.availableDevices()])
        self.camera_objs = QCameraInfo.availableCameras()

        # 打开默认的摄像头
        self.on_camera_select(0)
        self.set_image = QImageEncoderSettings()
        self.set_audio = QAudioEncoderSettings()
        self.set_video = QVideoEncoderSettings()

    # 选择摄像头
    def on_camera_select(self, i):
        self.cur_camera_name = self.cb_camera_selector.currentText()
        self.camera = QCamera(self.camera_objs[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.save_seq = 0
        self.on_camera_start()

        self.camera_objture = QCameraImageCapture(self.camera)
        self.camera_objture.error.connect(lambda i, e, s: self.alert(s))


    # 拍照
    def on_camera_take(self,filename=None):
        if filename:
            pass
        else:
            self.viewfinder.setContrast(100)
            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
            self.camera_objture.capture(os.path.join("d:/", "%s-%04d-%s.jpg" % (
                self.cur_camera_name,
                self.save_seq,
                timestamp
            )))
            self.save_seq += 1

    # 开始
    def on_camera_start(self):
        self.camera.start()
        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)

    # 停止
    def on_camera_stop(self):
        self.camera.stop()
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)

    def alert(self, mes):
        """
        Handle errors coming from QCamera dn QCameraImageCapture by displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(mes)

if __name__ == "__main__":
    import sys
    import cgitb
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)
    ui = CameraDefaultWidget()
    # ui.on_camera_open()
    ui.show()
    sys.exit(app.exec_())
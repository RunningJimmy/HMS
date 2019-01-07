'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: hms(健康管理系统)
@file: bcamera.py
@time: 2018-12-29 20:49
@desc:摄像头/视频读取模块
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
try:
    import cv2
except Exception as e:
    cv2 = None
    print("载入模块cv2 失败，信息：%s" %e)

class CameraWidget(QLabel):

    # 通过Opencv模块来实现
    # 优点：读标准摄像头、读非标摄像头、读写视频、处理图片等
    # 缺点：1、对XP支持不好 2、多个摄像头同时读取(不能插在同一个Hub上)

    def __init__(self,show_x,show_y):
        super(CameraWidget, self).__init__()
        self.resize(show_x,show_y)
        self.setScaledContents(1)
        self.initParas()

    # 初始化默认参数
    def initParas(self):
        self.show_width = 320
        self.show_height = 240
        self.show_fps = 24

    # 设置显示参数
    def setShowSize(self,width=320,height=240,fps=24):
        '''
        :param width: 宽度
        :param height: 高度
        :param fps: 每秒帧数
        :return: None
        '''
        self.show_width = width
        self.show_height = height
        self.show_fps = fps

    # 打开摄像头
    def open(self,camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        print("摄像头宽：%s,高：%s " %(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # 想要修改参数前请记住你摄像头参数的初始值;
        # 参数被改动了，是无法自动恢复到初始值的;
        # 除非特别需要，否则不要随意修改这些参数。
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.show_width)      # 宽度
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.show_height)    # 高度
        # self.cap.set(cv2.CAP_PROP_FPS, 30)                         # 帧数
        # self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 1)                   # 亮度
        # self.cap.set(cv2.CAP_PROP_CONTRAST, 40)                    # 对比度
        # self.cap.set(cv2.CAP_PROP_SATURATION, 50)                  # 饱和度
        # self.cap.set(cv2.CAP_PROP_HUE, 50)                         # 色调
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, 50)                    # 曝光
        self.start()

    # 开始图像传输，采用线程定时方式
    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onCapture)
        self.timer.start(1000 / self.show_fps)

    def onCapture(self):
        if not self.cap.isOpened():
            self.setText('打开失败，请检查配置！')
            self.setStyleSheet('''font: 75 14pt '黑体';color: rgb(204, 0, 0);''')
            return
        image = self.read()
        if image:
            self.setPixmap(QPixmap.fromImage(image, Qt.AutoColor))

    # 读取图像
    def read(self):
        # 按帧读取视频 其他方法
        # self.cap.retrieve()
        ret,frame = self.cap.read()
        # ret是布尔值 含义：如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。
        # frame就是每一帧的图像，是个三维矩阵
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ##############处理旋转#####################################
            # rows,cols,count = frame.shape
            # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
            # frame = cv2.warpAffine(frame, M, (cols, rows))
            image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888)
            # image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
            #                QImage.Format_RGB888).rgbSwapped()
            return image
        except Exception as e:
            self.timer.stop()

    # 暂停
    def stop(self):
        cv2.waitKey(0)

    # 拍照
    def onTakeImage(self,name):
        image = self.read()
        if image:
            image.save(name)
            return image

    # 关闭摄像头
    def deleteLater(self):
        self.timer.stop()
        self.cap.release()
        super(CameraWidget, self).deleteLater()


class CameraDefaultUI(QWidget):

    def __init__(self,parent=None):
        super(CameraDefaultUI,self).__init__(parent)
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
        self.viewfinder.show()
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
        self.btn_start = QPushButton(Icon('启动'), '启动')
        self.btn_stop = QPushButton(Icon('停止'), '停止')
        self.btn_take = QPushButton(Icon('拍照'), '拍照')
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

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))


    # 拍照
    def on_camera_take(self,filename=None):
        if filename:
            pass
        else:
            self.viewfinder.setContrast(100)
            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
            self.capture.capture(os.path.join("d:/", "%s-%04d-%s.jpg" % (
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
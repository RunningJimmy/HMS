from widgets.bwidget import *
from functools import partial

# 图片组件
# 放大、缩小、旋转、打印、上一张、下一站
class PicWidget(QDialog):

    open_new = pyqtSignal(list,int)
    # 参数1：所有图的二进制数据列表，
    # 参数2：图数量

    def __init__(self,parent=None):
        super(PicWidget,self).__init__(parent)
        self.setMinimumHeight(800)
        self.initUI()
        # self.open()
        self.open_new.connect(self.on_open_all)
        # 信号槽
        self.cb_adjust_size.stateChanged.connect(self.on_pic_adjust_size)
        self.btn_print.clicked.connect(self.on_pic_print)
        # 缩放
        self.btn_normal.clicked.connect(self.on_pic_original_size)
        self.btn_zoom_in.clicked.connect(partial(self.on_pic_zoom, False))
        self.btn_zoom_out.clicked.connect(partial(self.on_pic_zoom, True))
        # 翻转
        self.btn_filp_hor.clicked.connect(partial(self.on_pic_filp, True))
        self.btn_filp_ver.clicked.connect(partial(self.on_pic_filp, False))
        # 旋转
        self.btn_rotate_left.clicked.connect(partial(self.on_pic_rotate,-90))
        self.btn_rotate_right.clicked.connect(partial(self.on_pic_rotate,90))
        # 上一张 下一张
        self.btn_next.clicked.connect(self.on_btn_next_click)
        self.btn_previous.clicked.connect(self.on_btn_previous_click)

        # 特殊变量
        self.scale_factor = 0.0     # 比例因子
        self.printer = QPrinter()
        self.datas = None           # 所有数据
        self.cur_index = 0          # 图片对象索引

    def on_open_all(self,datas:list,num:int):
        self.cur_index = 0
        self.datas = datas
        self.on_pic_show(self.datas[self.cur_index])
        if num>1:
            self.btn_next.setDisabled(False)
            self.btn_previous.setDisabled(False)
        else:
            self.btn_next.setDisabled(True)
            self.btn_previous.setDisabled(True)

    # 数据传递打开
    def on_pic_show(self,data:bytes):
        '''
        :param data: 二进制数据
        :return:
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.src_pic_obj = pixmap.toImage()
        self.lb_pic.setPixmap(pixmap)
        self.scale_factor = 1.0
        self.on_pic_adjust_size(2)

    # 手工打开
    def open(self):
        # 原始图片
        filename = 'C:/Users/Administrator/Desktop/cachet.png'
        self.src_pic_obj = QImage(filename)
        if self.src_pic_obj.isNull():
            QMessageBox.information(self, "明州体检","Cannot load %s." % filename)
            return
        self.lb_pic.setPixmap(QPixmap.fromImage(self.src_pic_obj))
        self.scale_factor = 1.0
        self.on_pic_adjust_size(2)

    def initUI(self):
        lt_main = QVBoxLayout()
        #################################
        gp_pic = QGroupBox('图片预览')
        lt_pic = QVBoxLayout(self)
        self.lb_pic = QLabel()
        self.lb_pic.setAlignment(Qt.AlignCenter)
        self.lb_pic.setBackgroundRole(QPalette.Base)
        self.lb_pic.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lb_pic.setScaledContents(True)
        self.sa_pic_area = QScrollArea()
        self.sa_pic_area.setBackgroundRole(QPalette.Dark)
        self.sa_pic_area.setWidget(self.lb_pic)
        lt_pic.addWidget(self.sa_pic_area)
        gp_pic.setLayout(lt_pic)
        #####################################
        gp_btns = QGroupBox()
        lt_btns = QHBoxLayout()
        self.cb_adjust_size = QCheckBox('自适应')
        self.cb_adjust_size.setChecked(True)
        self.btn_print = QPushButton(Icon('打印'),'打印')
        self.btn_zoom_out = QPushButton(Icon('放大'),'放大')
        self.btn_normal = QPushButton(Icon('原始'), '原始')
        self.btn_zoom_in = QPushButton(Icon('缩小'),'缩小')
        self.btn_filp_hor = QPushButton("水平翻转")
        self.btn_filp_ver = QPushButton("垂直翻转")
        self.btn_rotate_left = QPushButton(Icon('lrotate'),'逆时针')
        self.btn_rotate_right = QPushButton(Icon('rrotate'),'顺时针')
        self.btn_next = QPushButton(Icon('向右'),'下一个')
        self.btn_previous = QPushButton(Icon('向左'),'上一个')
        # 添加控件
        lt_btns.addWidget(self.cb_adjust_size)
        lt_btns.addWidget(self.btn_print)
        lt_btns.addWidget(self.btn_zoom_out)
        # lt_btns.addWidget(self.btn_normal)
        lt_btns.addWidget(self.btn_zoom_in)
        lt_btns.addWidget(self.btn_filp_hor)
        lt_btns.addWidget(self.btn_filp_ver)
        lt_btns.addWidget(self.btn_rotate_left)
        lt_btns.addWidget(self.btn_rotate_right)
        lt_btns.addWidget(self.btn_previous)
        lt_btns.addWidget(self.btn_next)
        gp_btns.setLayout(lt_btns)
        # 添加布局
        lt_main.addWidget(gp_pic)
        lt_main.addWidget(gp_btns)
        self.setLayout(lt_main)

    # 顺时针或者逆时针旋转90度
    def on_pic_rotate(self,p_int):
        trans = QTransform()
        trans.rotate(p_int)
        self.src_pic_obj = self.src_pic_obj.transformed(trans, Qt.SmoothTransformation)
        self.lb_pic.setPixmap(QPixmap.fromImage(self.src_pic_obj))

    # 顺时针或逆时针旋转45度
    def on_pic_rotate2(self,p_int):
        image = QImage(self.srcImage.size(),QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(image)
        # 以图片中心为原点
        hw = self.src_pic_obj.width() / 2
        hh = self.src_pic_obj.height() / 2
        painter.translate(hw, hh)
        painter.rotate(p_int)  # 旋转-45度
        painter.drawImage(-hw, -hh, self.src_pic_obj)  # 把图片绘制上去
        painter.end()
        self.src_pic_obj = image  # 替换
        self.lb_pic.setPixmap(QPixmap.fromImage(self.src_pic_obj))

    # 翻转
    def on_pic_filp(self,flag=True):
        if flag:
            # 水平翻转
            self.src_pic_obj = self.src_pic_obj.mirrored(True, False)
        else:
            # 垂直翻转
            self.src_pic_obj = self.src_pic_obj.mirrored(False, True)

        self.lb_pic.setPixmap(QPixmap.fromImage(self.src_pic_obj))

    # 自适应 大小
    def on_pic_adjust_size(self,p_int):
        if p_int:
            self.sa_pic_area.setWidgetResizable(True)
            self.btn_zoom_in.setDisabled(True)
            self.btn_zoom_out.setDisabled(True)
            self.btn_normal.setDisabled(True)
        else:
            self.on_pic_original_size()
            self.btn_zoom_in.setDisabled(False)
            self.btn_zoom_out.setDisabled(False)
            self.btn_normal.setDisabled(False)

    #图片原始大小
    def on_pic_original_size(self):
        self.sa_pic_area.setWidgetResizable(False)
        self.lb_pic.adjustSize()
        self.scale_factor = 1.0

    # 放大缩小
    def on_pic_zoom(self,flag=True):
        '''
        :param flag: 默认放大
        :return:
        '''
        if flag:
            self.scaleImage(1.25)
        else:
            self.scaleImage(0.8)
        # print(self.scale_factor)

    def scaleImage(self, factor):
        self.scale_factor *= factor
        self.lb_pic.resize(self.scale_factor * self.lb_pic.pixmap().size())
        self.adjustScrollBar(self.sa_pic_area.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.sa_pic_area.verticalScrollBar(), factor)
        # 不允许无限放大或缩小
        self.btn_zoom_out.setEnabled(self.scale_factor < 3.0)
        self.btn_zoom_in.setEnabled(self.scale_factor > 0.1)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()+ ((factor - 1) * scrollBar.pageStep()/2)))

    # 图片打印
    def on_pic_print(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.lb_pic.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.lb_pic.pixmap().rect())
            painter.drawPixmap(0, 0, self.lb_pic.pixmap())

    # 上一个
    def on_btn_previous_click(self):
        try:
            self.cur_index = self.cur_index - 1
            self.on_pic_show(self.datas[self.cur_index])
        except Exception as e:
            mes_about(self,'当前是最后一张')
        # if abs(self.cur_index) <= len(self.datas)-1:
        #     mes_about(self,'当前是最后一份报告')
        #     return

    # 下一个
    def on_btn_next_click(self):
        try:
            self.cur_index = self.cur_index + 1
            self.on_pic_show(self.datas[self.cur_index])
        except Exception as e:
            print(e)
            mes_about(self, '当前是最后一份')
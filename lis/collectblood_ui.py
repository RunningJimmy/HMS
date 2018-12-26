from widgets.cwidget import *
from .model import *
from utils import gol
from functools import partial
from utils.buildbarcode import BarCodeBuild

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()

class Lable(QLabel):

    def __init__(self,width=None):
        super(Lable,self).__init__()
        if not width:
            self.setMinimumWidth(75)
        else:
            self.setMinimumWidth(width)
        self.setStyleSheet('''font: 75 11pt '黑体';color: rgb(0, 85, 255);''')

class PicLable(QLabel):

    def __init__(self):
        super(PicLable,self).__init__()
        self.setText('身\n份\n证\n照\n片')
        self.setAlignment(Qt.AlignCenter)
        # 一寸照大小
        self.setFixedWidth(102)
        self.setFixedHeight(126)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")

    def show2(self,datas):
        # write_file(datas, filename)
        p = QPixmap()
        p.loadFromData(datas)          # 数据不落地,高效
        self.setPixmap(p)

class CollectBlood_UI(UI):

    def __init__(self,title):
        super(CollectBlood_UI,self).__init__(title)

        ####################左边布局#####################################
        left_up_gp = QGroupBox('筛选条件')
        left_up_lt = QVBoxLayout()
        self.le_serialno= QSerialNo()
        left_up_lt.addWidget(self.le_serialno)
        left_up_gp.setLayout(left_up_lt)

        self.left_middle_gp = QGroupBox('采血列表')
        left_middle_lt = QVBoxLayout()
        self.blood_cols = OrderedDict([
            # ("tmzt", "状态"),
            ("sgys", "试管"),
            ("tmbh", "条码号"),
            ("tjbh", "体检编号"),
            ("xmhz", "条码项目")
        ])
        self.blood_table = CollectBloodTable(self.blood_cols)
        # self.blood_table.verticalHeader().setVisible(False)   # 去掉行头
        self.blood_table.setMinimumWidth(200)

        left_middle_lt.addWidget(self.blood_table)
        self.left_middle_gp.setLayout(left_middle_lt)
        #
        left_down_lt = QHBoxLayout()
        self.btn_handover = QPushButton(Icon('样本交接'), '样本交接')
        self.btn_diff = QPushButton(Icon('样本交接'), '采样遗漏')
        left_down_lt.addWidget(self.btn_handover)
        left_down_lt.addWidget(self.btn_diff)
        left_down_lt.addStretch()
        self.left_layout.addWidget(left_up_gp)
        self.left_layout.addWidget(self.left_middle_gp)
        self.left_layout.addLayout(left_down_lt)
        #self.left_layout.addStretch()

        ######################中间布局######################################
        group1 = QGroupBox('人员信息')
        layout1 = QGridLayout()
        group2 = QGroupBox('条码信息')
        layout2 = QHBoxLayout()
        group3 = QGroupBox('抽血详情')
        self.layout3 = QGridLayout()
        group4 = QGroupBox('留样详情')
        self.layout4 = QGridLayout()
        group5 = QGroupBox('拒检详情')
        self.layout5 = QGridLayout()

        ########################控件区#####################################
        self.lb_user_id   = Lable()          # 体检编号
        self.lb_user_name = Lable()          # 姓名
        self.lb_user_sex =  Lable()          # 性别
        self.lb_user_age =  Lable()          # 年龄->自动转换出生年月
        # self.lb_depart   =  Lable()          #班级
        self.lb_dwmc    =   Lable()          #单位名称
        # self.lb_qdrq =   Lable()          # 签到日期，默认当天
        self.lb_sjhm   =    Lable()          #手机号码
        self.lb_sfzh    =   Lable()          #身份证号
        # self.lb_djrq =   Lable()          # 登记日期
        self.lb_pic = PicLable()

        self.lb_sno_all = Lable()
        self.lb_sno_cx = Lable()
        self.lb_sno_ly = Lable()
        self.lb_sno_done = Lable()
        self.lb_sno_undone = Lable()
        self.lb_sno_jj = Lable()

        ###################基本信息  第一行##################################
        layout1.addWidget(QLabel('体检编号：'), 0, 0, 1, 1)
        layout1.addWidget(self.lb_user_id, 0, 1, 1, 1)
        layout1.addWidget(QLabel('姓    名：'), 0, 2, 1, 1)
        layout1.addWidget(self.lb_user_name, 0, 3, 1, 1)
        layout1.addWidget(QLabel('性    别：'), 0, 4, 1, 1)
        layout1.addWidget(self.lb_user_sex, 0, 5, 1, 1)
        layout1.addWidget(self.lb_pic, 0, 6, 3, 3)

        ###################基本信息  第二行##################################
        layout1.addWidget(QLabel('年    龄：'), 1, 0, 1, 1)
        layout1.addWidget(self.lb_user_age, 1, 1, 1, 1)
        layout1.addWidget(QLabel('单位名称：'), 1, 2, 1, 1)
        layout1.addWidget(self.lb_dwmc, 1, 3, 1, 3)

        ###################基本信息  第三行##################################
        layout1.addWidget(QLabel('手机号码：'), 2, 0, 1, 1)
        layout1.addWidget(self.lb_sjhm, 2, 1, 1, 1)
        layout1.addWidget(QLabel('身份证号：'), 2, 2, 1, 1)
        layout1.addWidget(self.lb_sfzh, 2, 3, 1, 3)

        layout1.setHorizontalSpacing(5)            #设置水平间距
        layout1.setVerticalSpacing(5)              #设置垂直间距
        layout1.setContentsMargins(5, 5, 5, 5)  #设置外间距
        layout1.setColumnStretch(11, 1)             #设置列宽，添加空白项的

        group1.setLayout(layout1)

        layout2.addWidget(QLabel("总条码数："))
        layout2.addWidget(self.lb_sno_all)
        layout2.addSpacing(5)
        layout2.addWidget(QLabel("抽血条码："))
        layout2.addWidget(self.lb_sno_cx)
        layout2.addSpacing(5)
        layout2.addWidget(QLabel("留样条码："))
        layout2.addWidget(self.lb_sno_ly)
        layout2.addSpacing(5)
        layout2.addWidget(QLabel("已抽条码："))
        layout2.addWidget(self.lb_sno_done)
        layout2.addSpacing(5)
        layout2.addWidget(QLabel("拒检条码："))
        layout2.addWidget(self.lb_sno_jj)
        layout2.addSpacing(5)
        layout2.addWidget(QLabel("剩余条码："))
        layout2.addWidget(self.lb_sno_undone)
        layout2.addSpacing(5)
        layout2.addStretch()
        group2.setLayout(layout2)

        group3.setLayout(self.layout3)
        group4.setLayout(self.layout4)
        group5.setLayout(self.layout5)

        self.middle_layout.addWidget(group1)
        self.middle_layout.addWidget(group2)
        self.middle_layout.addWidget(group3)
        self.middle_layout.addWidget(group4)
        self.middle_layout.addWidget(group5)
        self.middle_layout.addStretch()

        ####################右边布局#####################################
        self.cb_is_photo = QCheckBox('扫单自动拍照')
        self.cb_is_photo.setChecked(True)
        self.btn_take_photo = QPushButton(Icon('体检拍照'),'手动拍照')
        gp_right_up = QGroupBox('摄像头')
        gp_right_up.setAlignment(Qt.AlignHCenter)
        lt_right_up = QVBoxLayout()
        # 是否载入摄像头
        if gol.get_value('photo_enable'):
            show_x = gol.get_value('photo_capture_width')
            show_y = gol.get_value('photo_capture_height')
            capture = gol.get_value('photo_capture')
            fps = gol.get_value('photo_fps')
            try:
                self.camera = CameraUI(show_x,show_y,capture,fps)
                lt_right_up.addWidget(self.camera)
            except Exception as e:
                mes_about(self,'载入摄像头功能失败，错误信息：%s' %e)
                self.camera = None
        else:
            self.camera = None

        lt_right_up.addStretch()
        gp_right_up.setLayout(lt_right_up)
        # 按钮区
        right_middle_gp = QGroupBox()
        right_middle_lt = QHBoxLayout()
        right_middle_lt.addWidget(self.cb_is_photo)
        right_middle_lt.addWidget(self.btn_take_photo)
        right_middle_gp.setLayout(right_middle_lt)
        # 照片显示位置
        right_down_gp = QGroupBox('采血照片')
        right_down_gp.setAlignment(Qt.AlignHCenter)
        right_down_lt = QVBoxLayout()
        self.photo_lable = QLabel()
        # self.photo_lable.setStyleSheet("QLabel{border:2px solid rgb(0, 85, 255);}")
        # self.photo_lable.setFixedWidth(gol.get_value('photo_capture_width'))
        # self.photo_lable.setFixedHeight(gol.get_value('photo_capture_height'))
        right_down_lt.addWidget(self.photo_lable)
        right_down_lt.addStretch()
        right_down_gp.setLayout(right_down_lt)
        self.right_layout.addWidget(gp_right_up)
        self.right_layout.addWidget(right_middle_gp)
        self.right_layout.addWidget(right_down_gp)
        self.right_layout.addStretch()


# 样本采集完成列表
class CollectBloodTable(TableWidget):


    def __init__(self, heads, parent=None):
        super(CollectBloodTable, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色
        self.pipe_yellow = 0        # 黄管
        self.pipe_red = 0           # 紫红管

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)                # 插入一行
            # 额外处理
            if not row_data['tmzt'] and row_data['sgys'] == '黄管':
                self.pipe_yellow = self.pipe_yellow + 1
            elif not row_data['tmzt'] and row_data['sgys'] == '紫红管':
                self.pipe_red = self.pipe_red + 1
            for col_index, col_name in enumerate(heads.keys()):
                item = QTableWidgetItem(row_data[col_name])
                if row_data['tmzt']:
                    # 被交接过
                    item.setBackground(QColor("#f0e68c"))
                else:
                    # 未被交接
                    item.setBackground(QColor("#FF0000"))
                # item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        # self.setColumnWidth(0, 50)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.horizontalHeader().setStretchLastSection(True)

    @property
    def get_num(self):
        return self.pipe_yellow,self.pipe_red

    # 插入首行
    def insert(self,data):
        self.insertRow(0)
        for col_index, col_value in enumerate(data):
            item = QTableWidgetItem(col_value)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(0, col_index, item)

class CollectHandleUI(Dialog):

    query = pyqtSignal(str)

    def __init__(self,parent=None):
        super(CollectHandleUI,self).__init__(parent)
        self.setWindowTitle("样本交接")
        self.setMinimumHeight(500)
        self.initParas()
        self.initUI()
        self.query.connect(self.on_btn_query_click)
        self.table_handover_master.itemClicked.connect(self.on_table_detail_click)
        self.table_handover_master.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_handover_master.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单

    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_handover_master.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
            menu = QMenu()
            item1 = menu.addAction(Icon("打印"), "条码补打")
            item2 = menu.addAction(Icon("打印"), "重新生成")
            item3 = menu.addAction(Icon("打印"), "条码预览")
            action = menu.exec_(self.table_handover_master.mapToGlobal(pos))

            serialno_text = self.table_handover_master.getCurItemValueOfKey('HZTM')
            serialno_sgys = self.table_handover_master.getCurItemValueOfKey('SGYS')
            serialno_sgsl = self.table_handover_master.getCurItemValueOfKey('SGSL')
            # 条码标签
            serialno_lable = "%s %s %s %s" % (serialno_sgys, str(serialno_sgsl), self.login_name, cur_time())
            # 按钮功能
            if action == item1:
                if not serialno_text:
                    return
                self.on_serialno_handle(serialno_text,serialno_lable, True)
            # 按钮功能
            elif action == item2:
                # 模拟点击
                self.on_table_detail_click(self.table_handover_master.currentItem())
                serialno_text = self.on_serialno_handle('',serialno_lable, True)
                operate_time = cur_datetime()
                # 更新UI
                self.table_handover_master.setCurItemValueOfKey('HZTM', serialno_text)
                self.table_handover_master.setCurItemValueOfKey('jjsj', operate_time)
                # 更新数据库
                self.on_table_handover_detail_update(serialno_text,operate_time)
            # 按钮功能
            elif action == item3:
                if not serialno_text:
                    return
                self.on_serialno_handle(serialno_text,serialno_lable, False)

    # 查询
    def on_btn_query_click(self,login_id:str):
        sql = get_collect_handle_sql(cur_date(),cur_date(1),login_id)
        # print(sql)
        try:
            results = self.session.execute(sql)
        except Exception as e:
            mes_about(self,"执行数据库查询出错，错误信息：%s" %e)
            return
        self.table_handover_master.load(results)
        self.gp_left.setTitle('样本采集汇总(%s)' % self.table_handover_master.all_count)

    # 处理条码：打印、补打、重新生成、预览
    def on_serialno_handle(self,serialno_text:str,serialno_lable:str,handle_type:bool):
        '''
        :param serialno_text: 条码号，如果为空，则重新生成
        :param serialno_lable: 条码标签
        :param handle_type: 处理类型，默认打印
        :return:
        '''
        # 生成条码
        serialno_text, serialno_pic = self.on_serialno_build(serialno_text)
        if not serialno_text:
            return
        # 生成条码UI
        lb_serialno = SerialNoLable()
        lb_serialno.set_data.emit(serialno_pic, serialno_lable)
        #######################################
        printer = QPrinter(QPrinter.HighResolution)
        # 自定义格式 标准设置
        printer.setPageSize(QPagedPaintDevice.Custom)
        printer.setPageSizeMM(QSizeF(55.0, 35.0))
        # printer.setPaperSize(QSizeF(55.0,35), QPrinter.Millimeter)
        if handle_type:
            #直接打印
            self.on_serialno_print(lb_serialno, printer)
        else:
            self.on_serialno_preview(lb_serialno, printer)

        return serialno_text

    # 预览条码
    def on_serialno_preview(self,widget:QWidget,printer:QPrinter):
        '''
        :param widget:  打印的窗口
        :param printer: 打印设备，默认打印机
        :return:
        '''
        preview = QPrintPreviewDialog(printer, widget)
        preview.paintRequested.connect(partial(self.on_serialno_print,widget))
        preview.exec()

    # painter渲染
    def on_serialno_print(self,widget:QWidget,printer:QPrinter):
        '''
        :param widget:  打印的窗口
        :param printer: 打印设备，默认打印机
        :return:
        '''
        #### 方法1 render  但是尺寸 匹配有问题，不能自动匹配上
        painter = QPainter(printer)
        # painter.begin()
        painter.setViewport(widget.rect())
        # widget.rect() 打印窗口不设置大小，默认640*480，标签设置320*240 才刚刚好，未找到原因
        painter.setWindow(0,0,320,240)
        widget.render(painter)
        painter.end()
        #### 方法2 在打印预览界面中点击设置页码确定后，尺寸才刚刚匹配好
        # painter = QPainter(printer)
        # image = QPixmap()
        # image = widget.grab(QRect(QPoint(0, 0),
        #                           QSize(widget.size().width(),
        #                                 widget.size().height()
        #                                 )
        #                           )
        #                     )  # /* 绘制窗口至画布 */
        # # QRect
        # rect = painter.viewport()
        # print(rect)
        # # QSize
        # size = image.size()
        # print(rect.x(), rect.y(), size.width(), size.height())
        # size.scale(rect.size(), Qt.KeepAspectRatio)  # //此处保证图片显示完整
        # painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        # painter.setWindow(image.rect())
        # # /* 数据显示至预览界面 */
        # painter.drawPixmap(0, 0, image)

    # 是否生成条码
    def on_serialno_build(self,serialno_text:str):
        '''
        :param serialno_text: 条码号
        :return:
        '''
        # 获取条码
        if not serialno_text:
            result = self.session.query(MT_GY_IDENTITY).filter(MT_GY_IDENTITY.tname == 'TJ_CZJLB').scalar()
            if not result:
                mes_about(self,"表GY_IDENTITY 未找到TJ_CZJLB记录，请联系管理员！")
                return '',bytes()
            fpid = result.value
            serialno_text = "%s%s" % (cur_date2(), str(fpid).zfill(4))
        # 生成条码图片
        BarCodeBuild(path=self.tmp_file).create(serialno_text)
        try:
            serialno_pic = open(os.path.join(self.tmp_file, "%s.png" % serialno_text), "rb").read()
        except Exception as e:
            mes_about(self, "发生错误：%s" % e)
            return '',bytes()

        return serialno_text,serialno_pic

    # 更新数据库
    def on_table_handover_detail_update(self,serialno_text:str,operate_time:str):
        # 更新数据库，自增ID
        try:
            self.session.query(MT_GY_IDENTITY).filter(MT_GY_IDENTITY.tname == 'TJ_CZJLB').update({
                MT_GY_IDENTITY.value: MT_GY_IDENTITY.value + 1
            })
            count=0
            for row in range(self.table_handover_detail.rowCount()):
                count = count + 1
                # 一盘最多100管
                if count==101:
                    break
                tjbh = self.table_handover_detail.getItemValueOfKey(row, 'tjbh')
                mxbh = self.table_handover_detail.getItemValueOfKey(row, 'mxbh')
                self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.tjbh == tjbh, MT_TJ_CZJLB.mxbh == mxbh).update({
                    MT_TJ_CZJLB.jjxm: self.login_name,
                    MT_TJ_CZJLB.jjsj: operate_time,
                    MT_TJ_CZJLB.sjfs: serialno_text
                })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, "更新数据库发生错误：%s" % e)

    # 单击主表获得副表详情
    def on_table_detail_click(self,QTableWidgetItem):
        row = QTableWidgetItem.row()
        sgys = self.table_handover_master.getItemValueOfKey(row, 'SGYS')
        jjxm = self.table_handover_master.getItemValueOfKey(row, 'jjxm')
        jjsj = self.table_handover_master.getItemValueOfKey(row, 'jjsj')
        sgsl = self.table_handover_master.getItemValueOfKey(row, 'SGSL')
        # 最多100管
        if int(sgsl)>100:
            sgsl=100
        if not jjxm:
            jjxm = None
        if not jjsj:
            jjsj = None
        results = self.session.query(MT_TJ_CZJLB).filter(MT_TJ_CZJLB.czsj.between(cur_date(), cur_date(1)),
                                                         MT_TJ_CZJLB.jllx.in_(('0010', '0011')),
                                                         cast(MT_TJ_CZJLB.bz, VARCHAR) == sgys,
                                                         MT_TJ_CZJLB.czgh == self.login_id,
                                                         MT_TJ_CZJLB.jjxm == jjxm,
                                                         MT_TJ_CZJLB.jjsj == jjsj
                                                         ).all()
        self.table_handover_detail.load([result.detail for result in results])
        self.gp_right.setTitle('样本采集明细(%s)' %self.table_handover_detail.rowCount())
        # 是否需要打印
        if QTableWidgetItem.text()=='打印':
            # 获取条码标签
            serialno_lable = "%s %s %s %s" % (sgys, str(sgsl), self.login_name, cur_time())
            serialno_text = self.on_serialno_handle('',serialno_lable,True)
            operate_time = cur_datetime()
            # 更新UI
            self.table_handover_master.setItemValueOfKey(row, 'HZTM', serialno_text)
            self.table_handover_master.setItemValueOfKey(row, 'jjxm', self.login_name)
            self.table_handover_master.setItemValueOfKey(row, 'jjsj', operate_time)
            # 更新数据库
            self.on_table_handover_detail_update(serialno_text,operate_time)

    def initParas(self):
        self.collect_cols = OrderedDict([
                                ("CZQY", "区域"),
                                ("SGYS", "试管"),
                                ("SGSL", "数量"),
                                ("HZTM", "封盘条码"),
                                ("jjxm", "交接护士"),
                                ("jjsj", "交接时间"),
                                ("qsxm", "签收人员"),
                                ("qssj", "签收时间"),
                            ])

        self.collect_detail_cols = OrderedDict([
                                ("tjbh", "体检编号"),
                                ("mxbh", "条码号"),
                                ("czsj", "采集时间"),
                                ("czqy", "采集区域"),
                                ("czxm", "采集护士"),
                                ("jlnr", "项目明细")
                            ])

    def initUI(self):
        lt_main = QVBoxLayout()
        # 上布局
        lt_top = QHBoxLayout()
        gp_top = QGroupBox('筛选条件')
        # 上布局 控件
        self.de_start = QDateEdit(QDate.currentDate())
        self.de_end = QDateEdit(QDate.currentDate().addDays(1))
        self.de_start.setCalendarPopup(True)
        self.de_start.setDisplayFormat("yyyy-MM-dd")
        self.de_end.setCalendarPopup(True)
        self.de_end.setDisplayFormat("yyyy-MM-dd")
        # 只有管理员选择其他日期
        if self.login_id != 'BSSA':
            self.de_start.setDisabled(True)
            self.de_end.setDisabled(True)
        self.collect_user = UserCombox()
        self.collect_user.addItems(['%s'%self.login_name,'所有'])
        areas = ['明州1楼','明州2楼','明州3楼','明州贵宾','江东']
        self.collect_area = CollectAreaGroup(['明州1楼','明州2楼','明州3楼','明州贵宾','江东'])
        for area in areas:
            if area in self.login_area:
                self.collect_area.set_area(area)
        self.btn_query = QPushButton(Icon('query'),'查询')
        lt_top.addWidget(QLabel("采集日期："))
        lt_top.addWidget(self.de_start)
        lt_top.addWidget(QLabel("-"))
        lt_top.addWidget(self.de_end)
        lt_top.addSpacing(6)
        lt_top.addWidget(QLabel("采集人："))
        lt_top.addWidget(self.collect_user)
        lt_top.addSpacing(6)
        lt_top.addLayout(self.collect_area)
        lt_top.addSpacing(6)
        lt_top.addWidget(self.btn_query)
        lt_top.addStretch()
        gp_top.setLayout(lt_top)

        # 中布局
        lt_middle = QHBoxLayout()
        ########### 汇总信息
        lt_left = QHBoxLayout()
        self.gp_left = QGroupBox('样本采集汇总(0)')
        self.gp_left.setMinimumWidth(530)
        self.table_handover_master = CollectHandleSumTable(self.collect_cols)
        lt_left.addWidget(self.table_handover_master)
        self.gp_left.setLayout(lt_left)
        ########### 详细信息
        lt_right = QHBoxLayout()
        self.gp_right = QGroupBox('样本采集明细(0)')
        self.gp_right.setMinimumWidth(500)
        self.table_handover_detail = CollectHandoverDTable(self.collect_detail_cols)
        lt_right.addWidget(self.table_handover_detail)
        self.gp_right.setLayout(lt_right)
        lt_middle.addWidget(self.gp_left)
        lt_middle.addWidget(self.gp_right)
        # 添加主布局
        lt_main.addWidget(gp_top)
        lt_main.addLayout(lt_middle)
        self.setLayout(lt_main)


# 样本交接 条码数量汇总  明州的时候 汇总
def get_collect_handle_sql(t_start, t_end, login_id):
    return '''
        SELECT LEFT(CZQY,2) as CZQY,CAST(BZ AS VARCHAR) AS SGYS,count(*) as SGSL,SJFS,

        JJXM,JJSJ,JSXM,JSSJ

        FROM TJ_CZJLB 

        WHERE CZSJ BETWEEN '%s' AND '%s'

        AND JLLX IN ('0010','0011')  

        AND CZGH = '%s'

        GROUP BY LEFT(CZQY,2),CAST(BZ AS VARCHAR),JJXM,JJSJ,JSXM,JSSJ,SJFS

        ORDER BY count(*) DESC ;

    ''' % (t_start, t_end, login_id)

# 抽血交接签收
class CollectHandleSumTable(TableWidget):

    def __init__(self, heads, parent=None):
        super(CollectHandleSumTable, self).__init__(heads, parent)
        self.setAlternatingRowColors(False)  # 使用行交替颜色
        self.all_count = 0

    # 具体载入逻辑实现
    def load_set(self, datas, heads=None):
        # 载入数据到表格
        for row_index, row_data in enumerate(datas):
            self.insertRow(row_index)  # 插入一行
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str2(col_value))
                # 特殊处理 计算试管总数量
                if col_index==2:
                    self.all_count = self.all_count + col_value
                if col_index==3:
                    if not col_value:
                        item = QTableWidgetItem('打印')
                        item.setFont(get_font())
                        item.setBackground(QColor(218, 218, 218))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)

        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 70)
        self.setColumnWidth(5, 80)
        self.setColumnWidth(6, 70)
        self.setColumnWidth(7, 80)

class SerialNoLable(QDialog):

    set_data = pyqtSignal(bytes,str)
    # 参数1 图片 二进制数据
    # 参数2 文字 字符串

    def __init__(self,parent=None):
        super(SerialNoLable,self).__init__(parent)
        # self.setFixedWidth(55)
        # self.setFixedHeight(35)
        self.setStyleSheet('''QWidget{background-color:#ffffff;}''')
        self.initUI()
        self.set_data.connect(self.initDatas)

    def initUI(self):
        lt_main = QVBoxLayout()
        # 条码
        self.lb_tm = QLabel()
        # 文字
        self.lb_wz = QLabel()
        # font = QFont()
        # font.setPointSize(12)
        # self.lb_wz.setFont(font)
        lt_main.addWidget(self.lb_tm)
        lt_main.addWidget(self.lb_wz)
        self.setLayout(lt_main)

    def initDatas(self,pic:bytes,title:str):
        p = QPixmap()
        p.loadFromData(pic)
        self.lb_tm.setPixmap(p)
        self.lb_tm.setScaledContents(True)
        self.lb_wz.setText(title)
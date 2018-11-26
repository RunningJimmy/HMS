from .doubtful_ui import *
from app_interface import *
from utils import cur_datetime
from report import ItemsStateUI,OperateUI

'''
妇科：4585 4527 4529 1914 1910 1930 1933 1909 501699 501780
肝病科 4619
心胸外科 280008 280018 4617 1441
消化内科 5001 4599 1911 1920 501725 501726  5010 
'''

class Doubtful(DoubtfulUI):

    def __init__(self):
        super(Doubtful,self).__init__()
        # 绑定信号
        self.ccb_jb1.currentTextChanged.connect()
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)  # 快速检索
        self.table_health.itemClicked.connect(self.on_table_set)
        self.btn_export.clicked.connect(self.on_btn_export_click)
        self.btn_query.clicked.connect(self.on_btn_query)
        ########## 功能栏
        self.btn_item.clicked.connect(self.on_btn_item_click)
        self.btn_czjl.clicked.connect(self.on_btn_czjl_click)
        self.btn_phone.clicked.connect(self.on_btn_phone_click)
        self.btn_sms.clicked.connect(self.on_btn_sms_click)
        self.btn_forbidden.clicked.connect(self.on_btn_forbidden_click)
        # 特殊变量
        ###################################################
        self.cur_tjbh = None     # 最后一次选择的体检编号
        self.where_jb = {}
        self.where_rq = ''
        self.where_je = ''
        ############### 系统对话框 #######################################
        self.item_ui = None       # 项目查看
        self.operatr_ui = None    # 操作记录界面
        self.phone_ui = None      # 电话记录对话框
        self.sms_ui = None        # 短信记录对话框

    #体检系统项目查看
    def on_btn_item_click(self):
        if not self.item_ui:
            self.item_ui = ItemsStateUI(self)
        self.item_ui.show()
        if self.cur_tjbh:
            self.item_ui.returnPressed.emit(self.cur_tjbh)


    #体检系统项目查看
    def on_btn_czjl_click(self):
        if not self.operatr_ui:
            self.operatr_ui = OperateUI(self)
        self.operatr_ui.show()
        if self.cur_tjbh:
            self.operatr_ui.returnPressed.emit(self.cur_tjbh)

    # 电话记录
    def on_btn_phone_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return
        sjhm = self.table_health.getCurItemValueOfKey('sjhm')
        if not self.phone_ui:
            self.phone_ui = PhoneUI(self)
        self.phone_ui.show()
        self.phone_ui.returnPressed.emit(self.cur_tjbh, sjhm)

    # 短信记录
    def on_btn_sms_click(self):
        if not self.cur_tjbh:
            mes_about(self, '请先选择一个人！')
            return

        sjhm = self.table_health.getCurItemValueOfKey('sjhm')
        if not self.sms_ui:
            self.sms_ui = SmsUI(self)
        self.sms_ui.show()
        self.sms_ui.returnPressed.emit(self.cur_tjbh,sjhm)

    def on_btn_forbidden_click(self):
        pass


    # 设置快速检索文本
    def on_table_set(self, tableWidgetItem):
        row = tableWidgetItem.row()
        tjbh = self.table_health.getItemValueOfKey(row,'tjbh')
        xm = self.table_health.getItemValueOfKey(row,'xm')
        sfzh = self.table_health.getItemValueOfKey(row,'sfzh')
        sjhm = self.table_health.getItemValueOfKey(row,'sjhm')
        self.gp_quick_search.setText(tjbh, xm, sjhm, sfzh)
        self.cur_tjbh = tjbh

    #快速检索
    def on_quick_search(self,p1_str,p2_str):
        if p1_str == 'tjbh':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.tjbh == p2_str).all()
        elif p1_str == 'sjhm':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.sjhm == p2_str).all()
        elif p1_str == 'sfzh':
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.sfzh == p2_str).all()
        else:
            results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.xm == p2_str).all()
        tmp = [result.to_dict for result in results]
        self.table_health.load(tmp)
        mes_about(self,'共检索出 %s 条数据！' %self.table_health.rowCount())

    def onCheckState(self,p_str,is_check:int):
        if is_check == 2:
            # 添加
            self.where_jb[p_str] = '1'
        elif is_check == 0:
            if p_str in list(self.where_jb.keys()):
                self.where_jb.pop(p_str)

    # 查询
    def on_btn_query(self):
        if not any([self.cb_jb1.isChecked(),self.cb_jb2.isChecked()]):
            mes_about(self,'台湾专家或者门诊专家必须选择一个！')
            return
        if self.cb_jb1.isChecked():

            # if not self.ccb_jb1.textList():
            #     mes_about(self,'请选择要筛选的慢病病种！')
            # else:
            cols = ['tjbh','xm','xb','nl','sfzh','sjhm','dwmc','ysje','is_gxy','is_gxz','is_gxt','is_gns'
                ,'is_jzx','glu','is_yc_glu','glu2','is_yc_glu2','hbalc','is_yc_hbalc','ua','is_yc_ua','tch'
                ,'is_yc_tch','tg','is_yc_tg','hdl','is_yc_hdl','ldl','is_yc_ldl','hbp','is_yc_hbp','lbp','is_yc_lbp']
            sql = get_mbgl_sql()
            if self.dg_rq.where_date:
                sql = sql + self.dg_rq.where_date
            if self.mg_je.get_where_text():
                sql = sql + self.mg_je.get_where_text()
            if self.tj_dw.where_dwbh:
                sql = sql + ''' AND DWBH = '%s' ''' %self.tj_dw.where_dwbh
            if self.where_jb:
                sql = sql + ''' AND %s ''' %' AND '.join(["%s = '%s' " %(key,value) for key,value in self.where_jb.items()])
            # print(sql)
            # return
            results = self.session.execute(sql).fetchall()
            new_results = [dict(zip(cols,result)) for result in results]
            self.table_health.load(new_results,self.cols)
            self.gp_middle.setTitle('疑似列表(%s)' %self.table_health.rowCount())
            mes_about(self, '检索出 %s 条数据！' %self.table_health.rowCount())

            # results = self.session.query(MT_MB_YSKH).filter(MT_MB_YSKH.qdrq == '2018-06-30').all()
            # tmp = [result.to_dict for result in results]
            # self.table.load(tmp)
        else:
            # 门诊专家疾病
            self.on_mzjb_query(self.ccb_jb2.currentText())

    # 导出功能
    def on_btn_export(self):
        self.table.export()

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_health.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

        menu = QMenu()
        item1 = menu.addAction(Icon("报告中心"), "报告禁止查询")
        item2 = menu.addAction(Icon("报告中心"), "报告恢复查询")
        # item3 = menu.addAction(Icon("预约"), "设置预约客户")
        # item4 = menu.addAction(Icon("预约"), "电话记录")
        # item5 = menu.addAction(Icon("预约"), "本次体检结果")
        # item6 = menu.addAction(Icon("预约"), "历年体检结果")
        # item7 = menu.addAction(Icon("预约"), "浏览体检报告")
        # item8 = menu.addAction(Icon("预约"), "下载电子报告")

        action = menu.exec_(self.table_health.mapToGlobal(pos))
        if action==item1:
            tjbh = self.table_health.getCurItemValueOfKey('tjbh')
            if not tjbh:
                mes_about(self, '请先选择一个人！')
                return
            button = mes_warn(self, '您确认禁止顾客本人查询体检报告吗？')
            if button == QMessageBox.Yes:
                result = self.session.query(MT_TJ_Forbidden).filter(MT_TJ_Forbidden.tjbh == tjbh).scalar()
                if result:
                    mes_about(self, '该顾客已被禁用！')
                else:
                    data_obj = {'tjbh': tjbh, 'operator': self.login_name, 'operatime': cur_datetime()}
                    data_obj2 = {
                        'tjbh': tjbh, 'jllx': '0129', 'jlmc': '报告禁止查询', 'mxbh': '',
                        'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                    }
                    try:
                        self.session.bulk_insert_mappings(MT_TJ_Forbidden, [data_obj])
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj2])
                        self.session.commit()
                        mes_about(self, '禁止顾客本人查询体检报告操作成功！')
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '禁止顾客查询报告操作失败，错误信息：%s' % e)
        if action == item2:
            tjbh = self.table_health.getCurItemValueOfKey('tjbh')
            if not tjbh:
                mes_about(self, '请先选择一个人！')
                return
            button = mes_warn(self, '您确认恢复顾客本人查询体检报告吗？')
            if button == QMessageBox.Yes:
                result = self.session.query(MT_TJ_Forbidden).filter(MT_TJ_Forbidden.tjbh == tjbh).scalar()
                if not result:
                    mes_about(self, '未找到该体检报告被禁用的记录')
                else:
                    data_obj = {
                        'tjbh': tjbh, 'jllx': '0129', 'jlmc': '报告恢复查询', 'mxbh': '',
                        'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                    }
                    try:
                        self.session.query(MT_TJ_Forbidden).filter(MT_TJ_Forbidden.tjbh == tjbh).delete()
                        self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                        self.session.commit()
                        mes_about(self, '恢复顾客本人查询体检报告操作成功！')
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '恢复顾客查询报告操作失败，错误信息：%s' % e)

    # 获取门诊心内科、肝病科查询条件
    def get_jb2_where_str(self):
        sql = get_base_where(self.dg_rq.where_date)
        if self.mg_je.get_where_text():
            sql = sql +  self.mg_je.get_where_text()
        if self.tj_dw.where_dwbh:
            sql = sql + ''' AND TJ_TJDJB.DWBH = '%s' ''' % self.tj_dw.where_dwbh
        sql = sql +' ) '
        return sql

    def on_mzjb_query(self,mzmc:str):
        cols = OrderedDict([
            ('tjzt','状态'),
            ('tjbh','体检编号'),
            ('xm','姓名'),
            ('xb','性别'),
            ('nl','年龄'),
            ('sjhm','手机号码'),
            ('sfzh', '身份证号'),
            ('tjje', '金额'),
            ('tjrq', '体检日期'),
            ('dwmc', '单位名称'),
            ('ywy', '业务员'),
            ('xmmc', '项目名称'),
            ('xmzd', '项目诊断/参考范围'),
            ('xmjg', '项目结果')
        ])
        if mzmc=='心内科':
            sql = self.get_jb2_where_str() + get_xnk_sql()
        elif mzmc == '肝病科':
            sql = self.get_jb2_where_str() + get_gbk_sql()
        elif mzmc == '泌尿科':
            sql = self.get_jb2_where_str() + get_mnk_sql()
        elif mzmc == '妇科':
            sql = self.get_jb2_where_str() + get_fk_sql()
        elif mzmc == '心胸外科':
            sql = self.get_jb2_where_str() + get_xxwk_sql()
        elif mzmc == '消化内科':
            sql = self.get_jb2_where_str() + get_xhnk_sql()
        else:
            return
        try:
            results = self.session.execute(sql)
            if mzmc == '泌尿科':
                results = get_clean_result(results)
            self.table_health.load2(results, cols)
            self.gp_middle.setTitle('疑似列表(%s)' % self.table_health.rowCount())
            mes_about(self, '检索出 %s 条数据！' % self.table_health.rowCount())
        except Exception as e:
            mes_about(self,'执行查询出错，错误信息：%s' %e)



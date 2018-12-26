from flask import send_file,make_response,request,jsonify,abort,url_for,render_template,send_from_directory
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from app_api.exception import *
from app_api.model import *
import zeep,json,base64,os,ujson,time,urllib.parse,requests
import mimetypes,subprocess
from utils import gol,str2
from app_api.dbconn import *
import win32api,shutil
import win32print
from pyecharts import Bar
from collections import OrderedDict

# 初始化视图
def init_views(app,db,print_queue=None,report_queue=None):

    app.secret_key = 'secret string'

    # ckeditor = CKEditor(app)

    '''
    :param app:         应用程序本身
    :return:
    '''
    @app.route("/")
    def static_create():
        return url_for('static', filename='/css/report.css')

    # @app.route('/editor', methods=['GET', 'POST'])
    # def index():
    #     form = PostForm()
    #     if form.validate_on_submit():
    #         title = form.title.data
    #         body = form.body.data
    #         # You may need to store the data in database here
    #         return render_template('post.html', title=title, body=body)
    #     return render_template('index.html', form=form)
    #
    # @app.route('/files/<filename>')
    # def uploaded_files(filename):
    #     path = app.config['UPLOADED_PATH']
    #     return send_from_directory(path, filename)
    #
    # @app.route('/upload', methods=['POST'])
    # def upload():
    #     f = request.files.get('upload')
    #     extension = f.filename.split('.')[1].lower()
    #     if extension not in ['jpg', 'gif', 'png', 'jpeg']:
    #         return upload_fail(message='Image only!')
    #     f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    #     url = url_for('uploaded_files', filename=f.filename)
    #     return upload_success(url=url)

    @app.route('/api/chart/<string:title>/<string:start>/<string:end>')
    def chart_show(title,start,end):
        datas = get_datas(db.session,title,start,end)
        bar = build_chart(title,datas)
        ret_html = render_template('pyecharts.html',
                                   myechart=bar.render_embed(),
                                   mytitle=u"明州体检",
                                   host='/static',
                                   script_list=bar.get_js_dependencies())
        return ret_html

    # 外出体检API 用户名获取
    @app.route('/api/wctj/user/<string:user_id>', methods=['GET'])
    def wctj_get_user(user_id):
        print('外出服务 %s,客户端(%s)，获取用户名请求！参数：%s' % (cur_datetime(), request.remote_addr,user_id))
        sql = "SELECT YHMC FROM SS_OPERATE_USER WHERE YHDM='%s' AND XTSB='101'; " %user_id
        result = db.session.execute(sql).fetchone()
        if result:
            return ujson.dumps(str2(result[0]))
        else:
            abort(404)

    # 外出体检API 验证用户 通过则获取权限科室 和 外出单位信息
    @app.route('/api/wctj/user/validate/<string:user_id>/<string:user_pd>', methods=['POST'])
    def wctj_validate_user(user_id, user_pd):
        sql1 = "SELECT YHMC FROM SS_OPERATE_USER WHERE YHDM='%s' AND YHKL='%s' AND XTSB='101'; " %(user_id,user_pd)
        sql2 ="SELECT KSBM FROM TJ_YGQSKS WHERE YGGH = '%s';" %user_id
        sql3 = "SELECT MC,DWBH,PYJM FROM TJ_DWDMB WHERE sfwc='1'; "
        result = db.session.execute(sql1).fetchone()
        if result:
            tmp = {}
            dwmc_bh = {}
            dwmc_py = {}
            results = db.session.execute(sql2).fetchall()
            tmp['ksbm'] = [i[0] for i in results]
            results = db.session.execute(sql3).fetchall()
            if results:
                for result in results:
                    dwmc_bh[result[1]] = str2(result[0])
                    dwmc_py[result[2].lower()] = str2(result[0])
            tmp['dwmc_bh'] = dwmc_bh
            tmp['dwmc_py'] = dwmc_py
            return ujson.dumps(tmp)
        else:
            abort(404)

    # 外出体检API 获取外出单位信息
    @app.route('/api/wctj/dwmc', methods=['GET'])
    def wctj_get_dwmc():
        print('外出服务 %s,客户端(%s)，获取单位信息请求！参数：无。' % (cur_datetime(), request.remote_addr))
        sql = "SELECT MC,DWBH FROM TJ_DWDMB WHERE sfwc='1' ; "
        results = db.session.execute(sql).fetchall()
        if results:
            return ujson.dumps(dict([(str2(result[0]),result[1]) for result in results]))
        else:
            abort(404)

    # 获取报告批量下载用户名
    @app.route('/api/user/get/<string:user_id>', methods=['GET'])
    def get_user_name(user_id):
        sql = "select YHMC from TJ_DWFZR where YHID='%s' AND YXBZ='1'; " %user_id
        result = db.session.execute(sql).fetchone()
        if result:
            return ujson.dumps(result)
        else:
            abort(404)

    # 验证报告批量下载用户
    @app.route('/api/user/validate/<string:user_id>/<string:user_pd>', methods=['POST'])
    def validate_user(user_id,user_pd):
        sql = "select YHID from TJ_DWFZR where YHID='%s' AND YHMM='%s' AND YXBZ='1'; " %(user_id,user_pd)
        sql2 = "select (select mc from TJ_DWDMB WHERE DWBH=TJ_DWFZRSQ.DWBH) AS DWMC,DWBH from TJ_DWFZRSQ where YHID='%s'; " %user_id
        result = db.session.execute(sql).fetchone()
        if result:
            results = db.session.execute(sql2).fetchall()
            return ujson.dumps(dict(results))
        else:
            abort(404)

    # 获取单位进度
    @app.route('/api/dwjd/all/<string:dwbh>', methods=['GET'])
    def get_dwjd_all(dwbh):
        print(' %s：客户端(%s)：单位(%s)进度请求！无额外参数。' % (cur_datetime(), request.remote_addr, dwbh))
        sql = get_report_progress_sum_sql(dwbh)
        requests = db.session.execute(sql).fetchall()
        if requests:
            return ujson.dumps(requests)
        else:
            abort(404)

    # 获取一段时间内单位体检进度
    @app.route('/api/dwjd/all/<string:dwbh>/<string:tstart>/<string:tend>', methods=['GET'])
    def get_dwjd_all_ofdate(dwbh,tstart,tend):
        print(' %s：客户端(%s)：单位(%s)进度请求！额外参数时间：%s, %s' % (cur_datetime(), request.remote_addr, dwbh, tstart,tend))
        sql = get_report_progress_sum2_sql(dwbh,tstart,tend)
        # print(sql)
        requests = db.session.execute(sql).fetchall()
        if requests:
            return ujson.dumps(requests)
        else:
            abort(404)

    # 获取个人体检进度
    @app.route('/api/grjd/get/<string:login_id>/<string:search_t>/<string:search_v>', methods=['GET'])
    def get_grjd_tjzt(login_id, search_t, search_v):
        print(' %s：客户端(%s)：个人体检进度请求！' % (cur_datetime(), request.remote_addr))
        if search_t == 'tjbh':
            where = ''' AND TJ_TJDJB.DWBH IN (SELECT DWBH FROM TJ_DWFZRSQ WHERE YHID='%s') AND TJ_TJDJB.TJBH='%s' ''' %(login_id,search_v)
        elif search_t == 'xm':
            where = ''' AND TJ_TJDJB.DWBH IN (SELECT DWBH FROM TJ_DWFZRSQ WHERE YHID='%s') AND TJ_TJDAB.XM='%s' ''' % (login_id, search_v)
        else:
            where = ''' AND TJ_TJDJB.DWBH IN (SELECT DWBH FROM TJ_DWFZRSQ WHERE YHID='%s') AND TJ_TJDAB.SFZH='%s' ''' %(login_id,search_v)
        sql = get_user_progress_sql(where)
        requests = db.session.execute(sql).fetchall()
        if requests:
            return ujson.dumps(requests)
        else:
            abort(404)

    # 获取单位进度详细
    @app.route('/api/dwjd/get/<string:dwbh>/<string:tjzt>/<string:ctjzt>', methods=['GET'])
    def get_dwjd_tjzt(dwbh,tjzt,ctjzt):
        print(' %s：客户端(%s)：单位(%s)，(%s)进度请求！无额外参数。' % (cur_datetime(), request.remote_addr, dwbh,ctjzt))
        if tjzt =='sum':
            tjzt_where = ''' WHERE 1 = 1 '''
        else:
            tjzt_where = ''' WHERE TJZT2='%s' ''' %tjzt
        sql = get_report_progress_sql(ctjzt, dwbh, tjzt_where)
        # print(sql)
        requests = db.session.execute(sql).fetchall()
        if requests:
            return ujson.dumps(requests)
        else:
            abort(404)

    # 获取指定时间内单位进度详细
    @app.route('/api/dwjd/get/<string:dwbh>/<string:tjzt>/<string:ctjzt>/<string:tstart>/<string:tend>', methods=['GET'])
    def get_dwjd_tjzt_ofdate(dwbh, tjzt, ctjzt,tstart,tend):
        print(' %s：客户端(%s)：单位(%s)，(%s)进度请求！额外参数：%s，%s' % (cur_datetime(), request.remote_addr, dwbh, ctjzt,tstart,tend))
        if tjzt =='sum':
            tjzt_where = ''' WHERE 1 = 1 '''
        else:
            tjzt_where = ''' WHERE TJZT2='%s' ''' %tjzt
        sql = get_report_progress2_sql(ctjzt, dwbh, tjzt_where,tstart,tend)
        requests = db.session.execute(sql).fetchall()
        if requests:
            return ujson.dumps(requests)
        else:
            abort(404)

    # 获取彩超、内镜图像
    @app.route('/api/pacs/pic/<string:tjbh>/<string:ksbm>/<string:xmbh>', methods=['GET','POST'])
    def get_pacs_pic(tjbh, ksbm,xmbh):
        print(' %s：客户端(%s)：检查图像接收请求！参数 tjbh(%s)，ksbm(%s)，xmbh(%s)' % (cur_datetime(), request.remote_addr, tjbh, ksbm,xmbh))
        url = "http://10.8.200.220:7059/WebGetFileView.asmx?WSDL"
        client = zeep.Client(url)
        tmp = client.service.f_GetUISFilesByTJ_IID(tjbh + xmbh)
        try:
            result = json.loads(tmp)
            if result['IsSuccess'] == 'true':
                sql = "DELETE FROM TJ_PACS_PIC WHERE tjbh='%s' and zhbh ='%s';" % (tjbh, xmbh)
                db.session.execute(sql)
                pic_datas = result['Datas']
                count = 0
                for pic_data in pic_datas:
                    count = count + 1
                    pic_name = '%s_%s_%s.jpg' % (tjbh, xmbh, count)
                    pic_pk = '%s%s' % (tjbh, xmbh)
                    filename = os.path.join("D:\space\pic",pic_name )
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(pic_data))

                    sql = "INSERT INTO TJ_PACS_PIC(TJBH,KSBM,PICPATH,PICNAME,ZHBH,PATH,PK)VALUES('%s','%s','%s','%s','%s','%s','%s')" %(
                        tjbh,ksbm,pic_name,pic_name,xmbh,pic_name,pic_pk
                    )
                    db.session.execute(sql)
                return ujson.dumps({'code': 1, 'mes': '图片传输成功', 'data': ''})
            else:
                print("B超图像接收失败!")
                abort(404)
        except Exception as e:
            print("B超图像接收失败，源数据：%s" %tmp)
            abort(404)

    #二维码生成
    # @app.route('/api/qrcode/post?tjbh=<string:tjbh>&xm=<string:xm>&sfzh=<string:sfzh>&sjhm=<string:sjhm>&login_id=<string:login_id>', methods=['POST'])
    @app.route('/api/qrcode/<string:tjbh>/<string:login_id>', methods=['GET'])
    def qrcode_create(tjbh,login_id):
        print(' %s：客户端(%s)：微信二维码请求！参数 tjbh：%s，login_id：%s' % (cur_datetime(), request.remote_addr, tjbh, login_id))
        user = get_user_info(tjbh,db)
        if user:
            url = 'http://10.7.200.60:80/tjadmin/pInfoSubmit'
            #url = 'http://10.7.200.27:8089/tjadmin/pInfoSubmit'
            head = {}
            head['realName'] = urllib.parse.quote(user['xm'])
            head['idCardNum'] = user['sfzh']
            head['phoneNumber'] = user['sjhm']
            head['email'] = ''
            head['address'] = ''
            head['Content-Type'] = 'application/json'
            try:
                response = requests.post(url, headers=head)
                if response.status_code == 200:
                    # f = open(r'C:\Users\Administrator\Desktop\pdf测试\1.png', "wb")
                    # for chunk in response.iter_content(chunk_size=512):
                    #     if chunk:
                    #         f.write(chunk)
                    # f.close()
                    return response.content
                else:
                    abort(404)
            except Exception as e:
                print("微信二维码请求失败！")
                abort(404)
        else:
            abort(404)

    # HTML 报告生成 医生总检审核完成
    # PDF 报告生成，护理审阅完成
    @app.route('/api/report/create/<string:filetype>/<int:tjbh>/<string:login_id>', methods=['GET','POST'])
    def report_create(filetype,tjbh,login_id):
        print(' %s：客户端(%s)：%s报告生成请求！参数 tjbh：%s，login_id：%s'  % (cur_datetime(), request.remote_addr,filetype, tjbh, login_id))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        mes_obj = {'tjbh':tjbh,'action':filetype}
        if report_queue:
            # print('%s 队列插入消息：%s' %(cur_datetime(),ujson.dumps(mes_obj)))
            report_queue.put(mes_obj)
        else:
            abort(404)
        if filetype=='html':
            return ujson.dumps({'code': 1, 'mes': 'HTML报告生成', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            return ujson.dumps({'code': 1, 'mes': 'PDF报告生成', 'data': ''})
        else:
            abort(404)

    # HTML 报告删除 医生取消审核
    # PDF 报告删除，护理取消审阅
    @app.route('/api/report/delete/<string:filetype>/<int:tjbh>/<string:login_id>/<string:czlx>', methods=['GET','POST'])
    def report_delete(filetype,tjbh,login_id,czlx):
        print(' %s：客户端(%s)：%s报告取消审核请求！参数 tjbh：%s，login_id：%s，czlx：%s' % (cur_datetime(), request.remote_addr, filetype, tjbh, login_id,czlx))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        if filetype=='html':
            # 审核取消
            try:
                # 报告审核总检取消、报告生成取消
                sql1 = " UPDATE TJ_TJDJB SET TJZT='%s' WHERE TJBH = '%s' ;" %(tjbh,czlx)
                sql2 = " UPDATE TJ_BGGL SET BGZT='0',BGTH='0',SYRQ=NULL,SYXM=NULL,SYGH=NULL WHERE TJBH = '%s' ;" % tjbh
                db.session.execute(sql1)
                db.session.execute(sql2)
                # if czlx =='5':
                #     sql2 = " UPDATE TJ_BGGL SET BGZT='0',BGTH='0' WHERE TJBH = '%s' ;" % tjbh
                #     db.session.execute(sql2)
            except Exception as e:
                print(e)
            return ujson.dumps({'code': 1, 'mes': '取消审核，删除HTML报告成功', 'data': ''})
        elif filetype=='pdf':
            # 审阅完成
            # 审核取消
            try:
                sql1 = "UPDATE TJ_TJDJB SET TJZT='%s' WHERE TJBH = '%s' " %(tjbh,czlx)
                sql2 = "UPDATE TJ_BGGL SET BGZT='0',BGTH='1' WHERE TJBH = '%s' " % tjbh
                db.session.execute(sql1)
                db.session.execute(sql2)
            except Exception as e:
                print(e)
            return ujson.dumps({'code': 1, 'mes': '取消审阅，删除PDF报告成功', 'data': ''})
        else:
            abort(404)

    # HTML 报告预览 用户发起
    # PDF 报告预览，用户发起
    @app.route('/api/report/preview/<string:filetype>/<int:tjbh>', methods=['GET'])
    def report_preview(filetype,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        if filetype =='html':      # request 请求
            sql = "select bglj from tj_bggl where tjbh='%s';" %tjbh
            result = db.session.execute(sql).scalar()
            if result:
                filename = os.path.join(result,'%s.html' %tjbh)
                if os.path.exists(filename):
                    return send_file(filename)

            abort(404)
        elif filetype =='pdf':     # report 报告
            result = db.session.query(MT_TJ_FILE_ACTIVE.filename).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == 'report').scalar()
            if result:
                # print("http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result)
                return "http://10.8.200.201:8080/web/viewer.html?file=/tmp/%s" % result
        else:
            abort(404)

    # PDF 报告下载，用户发起
    @app.route('/api/report/down/pdf/<int:tjbh>', methods=['GET'])
    def report_down(tjbh):
        print(' %s：客户端(%s)：%s报告下载请求！' % (cur_datetime(), request.remote_addr,tjbh))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        # 当前
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            if result.bglj:
                filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
                if os.path.exists(filename):
                    update_czjl(db.session,tjbh,request.remote_addr)
                    # 返回下载
                    response = make_response(send_file(filename, as_attachment=True))
                    response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
                    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
                    return response

        # 历史
        session = gol.get_value('tj_cxk')
        result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
        if result:
            filename = os.path.join('D:/pdf/',result.PDFURL)
            if os.path.exists(filename):
                update_czjl(db.session, tjbh, request.remote_addr)
                #返回下载
                response = make_response(send_file(filename, as_attachment=True))
                response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
                return response

        # 向历史的报告服务发送请求
        url = "http://10.8.200.201:4000/api/file/down/%s/%s" %(tjbh,'report')
        return api_file_down(url)

    # PDF 报告预览，用于外网PC客户端
    @app.route('/api/report/show/pdf/<int:tjbh>', methods=['POST'])
    def report_show(tjbh):
        print(' %s：外网客户端(%s)：%s报告预览请求！' % (cur_datetime(), request.remote_addr, tjbh))
        tmp_path = app.config['UPLOAD_FOLDER_TMP']
        tmp_filename = os.path.join(tmp_path, "%s.pdf" % tjbh)
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)

        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            if result.bglj:
                filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
                if os.path.exists(filename):
                    shutil.copy2(filename, tmp_filename)
                    return ujson.dumps({'code': 1, 'mes': '处理成功', 'data': ''})

        # 历史
        session = gol.get_value('tj_cxk')
        result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(
            MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
        if result:
            filename = os.path.join('D:/pdf/', result.PDFURL)
            if os.path.exists(filename):
                shutil.copy2(filename, tmp_filename)
                return ujson.dumps({'code': 1, 'mes': '处理成功', 'data': ''})

        abort(404)

    # PDF 报告打印记录
    @app.route('/api/report/print2/pdf/<int:tjbh>/<string:login_id>/<string:login_name>', methods=['POST'])
    def report_print2(tjbh,login_id,login_name):
        print(' %s：客户端(%s)：%s报告打印完成记录请求！' % (cur_datetime(), request.remote_addr, tjbh))
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).update(
                {
                    MT_TJ_BGGL.dyrq: cur_datetime(),
                    MT_TJ_BGGL.dyfs: '3',
                    MT_TJ_BGGL.dygh: login_id,
                    MT_TJ_BGGL.dyxm: login_name,
                    MT_TJ_BGGL.dycs: MT_TJ_BGGL.dycs + 1,
                    MT_TJ_BGGL.bgzt: MT_TJ_BGGL.bgzt if int(MT_TJ_BGGL.bgzt)>3 else '3',
                    MT_TJ_BGGL.dyzt: None
                }
            )

        sql = "INSERT TJ_CZJLB(JLLX,TJBH,MXBH,CZGH,CZSJ,CZQY,CZXM,JLMC)VALUES(" \
              "'0038','%s','','%s','%s','%s','%s','报告网上打印')" % (
            tjbh,login_id,cur_datetime(),request.remote_addr,login_name)

        try:
            db.session.execute(sql)
        except Exception as e:
            print(e)

        return ujson.dumps({'code': 1, 'mes': '处理成功', 'data': ''})

    # PDF 报告打印，用户发起
    @app.route('/api/report/print/pdf/<int:tjbh>/<string:printer>', methods=['POST'])
    def report_print(tjbh,printer):
        print(' %s：客户端(%s)：%s报告打印请求！' % (cur_datetime(), request.remote_addr, tjbh))
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = str(tjbh)
        else:
            abort(404)
        result = db.session.query(MT_TJ_BGGL).filter(MT_TJ_BGGL.tjbh == tjbh).scalar()
        if result:
            if result.bglj:
                filename = os.path.join(result.bglj,"%s.pdf" %tjbh)
                if os.path.exists(filename):
                    mes_obj = {'filename': filename, 'action': 'print', 'printer': printer}
                    if print_queue:
                        print_queue.put(mes_obj)
                        return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})

        # else:
            # 历史
        session = gol.get_value('tj_cxk')
        result = session.query(MT_TJ_PDFRUL).filter(MT_TJ_PDFRUL.TJBH == tjbh).order_by(MT_TJ_PDFRUL.CREATETIME.desc()).scalar()
        if result:
            filename = os.path.join('D:/pdf/',result.PDFURL)
        else:
            filename = os.path.join('D:/tmp/','%s.pdf' %tjbh)
            url = "http://10.8.200.201:4000/api/file/down/%s/%s" % (tjbh, 'report')
            request_get(url,filename)
        if os.path.exists(filename):
            mes_obj = {'filename': filename, 'action': 'print','printer':printer}
            if print_queue:
                print_queue.put(mes_obj)
                return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})
            else:
                abort(404)
            # result= print_pdf_gsprint(filename,printer)
            # if result==0:
            #     return ujson.dumps({'code': 1, 'mes': '报告打印成功！', 'data': ''})
            # else:
            #     return ujson.dumps({'code': 0, 'mes': '报告打印失败！', 'data': ''})
        else:
            abort(404)

    # 设备 预览
    @app.route('/api/equip/preview/<string:equip_file>/<string:tjbh>', methods=['POST'])
    def equip_preview(equip_file,tjbh):
        pass

    # 设备 报告下载
    @app.route('/api/equip/down/<int:equip_file>/<int:tjbh>', methods=['POST'])
    def equip_down(equip_file,tjbh):
        if len(str(tjbh)) == 8:
            tjbh = '%09d' % tjbh
        elif len(str(tjbh)) == 9:
            tjbh = tjbh
        pass

    # 设备 报告上传
    @app.route('/api/equip/upload/', methods=['POST'])
    def equip_upload():
        cur_path = get_cur_path(app.config['UPLOAD_FOLDER_EQUIP'])
        file_obj = request.files['file']
        new_file=os.path.join(cur_path, os.path.basename(file_obj.filename))
        file_obj.save(new_file)
        # 返回上传路径
        file_type = os.path.basename(file_obj.filename)[-3:]
        if file_type =='_08':
            print('%s 心电图：%s 文件上传成功！' %(cur_datetime(),new_file))
        elif file_type =='_01':
            print('%s 电测听：%s 文件上传成功！' %(cur_datetime(),new_file))
        elif file_type =='_04':
            print('%s 骨密度：%s 文件上传成功！' %(cur_datetime(),new_file))
        return ujson.dumps({'code': 1, 'mes': '上传成功', 'data': new_file})

    # 文件上传
    @app.route('/api/file/upload/', methods=['POST'])
    def file_upload():
        cur_path = get_cur_path(app.config['UPLOAD_FOLDER_PHOTO'])
        file_obj = request.files['file']
        user = request.headers['User']
        file_prefix, file_suffix = os.path.splitext(os.path.split(file_obj.filename)[1])
        new_file=os.path.join(cur_path, os.path.basename(file_obj.filename))
        file_obj.save(new_file)
        try:
            # 获取插入的SQL 更新 TJ_FILE_ACTIVE
            result = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == file_prefix[0:9],
                                                                MT_TJ_FILE_ACTIVE.filetype == file_prefix[-6:]).scalar()
            if result:
                db.session.delete(result)
            db.session.execute(get_file_upload_sql(new_file))
            db.session.commit()
        except Exception as e:
            print('更新失败！错误信息：%s' %e)
        if file_prefix[-6]=='000001':
            # 采血的照片，固定
            pass
        return ujson.dumps({'code':1,'mes':'上传成功','data':None})

    # 文件下载
    @app.route('/api/file/down/<string:tjbh>/<string:filetype>', methods=['GET'])
    def file_down(tjbh,filetype):
        '''
        :param tjbh:        体检编号
        :param filetype:    文件类型
        :return:
        '''
        results = db.session.query(MT_TJ_FILE_ACTIVE).filter(MT_TJ_FILE_ACTIVE.tjbh == tjbh,MT_TJ_FILE_ACTIVE.filetype == filetype).order_by(desc(MT_TJ_FILE_ACTIVE.createtime)).all()
        if results:
            filename = results[0].localfile
            # print(results[0].localfile)
            # response = make_response(send_file(results[0].localfile,as_attachment=True))
            # response.headers['Content-Type'] = mimetypes.guess_type(results[0].filename)[0]
            # response.headers['Content-Disposition'] = 'attachment; filename={}'.format(results[0].filename)
            # return response
            # 返回下载
            response = make_response(send_file(filename, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(filename))[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(filename))
            return response
        else:
            abort(404)

    # 程序文件下载更新
    @app.route('/api/version_file/<string:platform>/<float:version>', methods=['GET'])
    def update_file(platform,version):
        print(' %s：(%s)客户端(%s)：版本文件下载请求！当前版本号：%s' % (cur_datetime(),platform,request.remote_addr, str(version)))
        if platform=='win7':
            platform_name ='1'
        else:
            platform_name = '0'
        results = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version >version,MT_TJ_UPDATE.platform==platform_name).order_by(MT_TJ_UPDATE.version.asc()).all()
        if results:
            result = results[0]
            response = make_response(send_file(result.ufile, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.ufile)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.ufile)
            return response
        else:
            abort(404)

    # 外网程序文件下载更新
    @app.route('/api2/version_file/<string:platform>/<float:version>', methods=['GET'])
    def update_file2(platform, version):
        print(' %s：(%s)外网客户端(%s)：版本文件下载请求！当前版本号：%s' % (cur_datetime(), platform, request.remote_addr, str(version)))
        # if platform == 'win7':
        #     platform_name = '1'
        # else:
        #     platform_name = '0'
        results = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version > version,
                                                        MT_TJ_UPDATE.platform ==None,
                                                        ).order_by(MT_TJ_UPDATE.version.asc()).all()
        if results:
            result = results[0]
            response = make_response(send_file(result.ufile, as_attachment=True))
            response.headers['Content-Type'] = mimetypes.guess_type(result.ufile)[0]
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(result.ufile)
            return response
        else:
            abort(404)

    # 程序更新说明
    @app.route('/api/version/<string:platform>/<float:version>', methods=['GET'])
    def update_version(platform, version):
        print(' %s：(%s)客户端(%s)：版本更新请求！当前版本号：%s' % (cur_datetime(), platform, request.remote_addr, str(version)))
        if platform == 'win7':
            platform_name = '1'
        else:
            platform_name = '0'
        results = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version > version,
                                                       MT_TJ_UPDATE.platform == platform_name).order_by(MT_TJ_UPDATE.version.asc()).all()
        if results:
            result =results[0]
            return ujson.dumps({'version': result.version, 'describe': str2(result.describe)})
        else:
            abort(404)

    # 程序更新说明
    @app.route('/api2/version/<string:platform>/<float:version>', methods=['GET'])
    def update_version2(platform, version):
        print(' %s：(%s)客户端(%s)：版本更新请求！当前版本号：%s' % (cur_datetime(), platform, request.remote_addr, str(version)))
        # if platform == 'win7':
        #     platform_name = '1'
        # else:
        #     platform_name = '0'
        results = db.session.query(MT_TJ_UPDATE).filter(MT_TJ_UPDATE.version > version,
                                                        MT_TJ_UPDATE.platform == None).order_by(
            MT_TJ_UPDATE.version.asc()).all()
        if results:
            result = results[0]
            return ujson.dumps({'version': result.version, 'describe': str2(result.describe)})
        else:
            abort(404)

    # 图片识别出文字
    @app.route('/api/pic2txt/', methods=['POST'])
    def pic2txt():
        file_obj = request.files['file']
        print(' %s：客户端(%s)：OCR服务请求：%s' % (cur_datetime(), request.remote_addr,file_obj.filename))
        url = "http://10.7.200.127:10006/api/pic2txt/"
        try:
            response = requests.post(url, files=request.files)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print('URL：%s 请求失败！错误信息：%s' % (url, e))
            abort(404)

    @app.errorhandler(BaseError)
    def custom_error_handler(e):
        if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
            if isinstance(e, OrmError):
                app.logger.exception('%s %s' % (e.parent_error, e))
            else:
                app.logger.exception('错误信息: %s %s' % (e.extras, e))
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response

# 获得当日的保存目录
def get_cur_path(dirname):
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    cur_path = '%s%s/%s/%s/' %(dirname,dyear,dmonth,dday)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)

    return cur_path

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

# 获得文件上传的SQL
def get_file_upload_sql(filename):
    file_prefix, file_suffix = os.path.splitext(os.path.split(filename)[1])
    dday = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    dyear = dday[0:4]
    dmonth = dday[0:7]
    sql = '''
    INSERT INTO TJ_FILE_ACTIVE(TJBH,DWBH,RYEAR,RMONTH,RDAY,LOCALFILE,FILENAME,FILETYPE,CREATETIME) 
    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s') 
    ''' %(file_prefix[0:9],file_prefix[0:5],dyear,dmonth,dday,filename,os.path.split(filename)[1],file_prefix[-6:],cur_datetime())
    return sql

# 获取前缀、后缀名称
def get_pre_suf(filename):
    return os.path.splitext(os.path.basename(filename))

# 获得用户信息二维码
def get_user_info(tjbh,db):
    sql = "select XM,SFZH,SJHM FROM TJ_TJDAB WHERE DABH = (SELECT DABH FROM TJ_TJDJB where TJBH='%s') ;" %tjbh
    # print(sql)
    results = db.session.execute(sql).fetchall()
    if results:
        result = results[0]
        if all([result[1],result[2]]):
            return {'xm':str2(result[0]),'sfzh':result[1],'sjhm':result[2]}
        else:
            return {}
    else:
        return {}

def api_file_down(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        abort(404)

def print_pdf_gsprint(filename,printer=None):
    if not printer:
        printer = win32print.GetDefaultPrinter()
    command =r'gsprint -color -printer "%s" %s' %(printer,filename)
    result = subprocess.run(command, shell=True)
    return result.returncode

def request_get(url,save_file=None):
    '''
    :param url:             请求地址
    :param save_file:       下载文件 save_file
    :return:
    '''
    response = requests.get(url)
    if response.status_code==200:
        try:
            f = open(save_file, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def update_czjl(session,tjbh,addr):
    if '10.8.102.' or '10.8.103.' or '10.8.104.' or '10.7.103.' or '10.8.200' in addr:
        jllx = '0036'
        jlmc = '报告下载'
    else:
        jllx = '0039'
        jlmc = '报告网上下载'

    sql = "INSERT TJ_CZJLB(JLLX,TJBH,MXBH,CZGH,CZSJ,CZQY,CZXM,JLMC)VALUES('%s','%s','','','%s','%s','','%s')" %(jllx,tjbh,cur_datetime(),addr,jlmc)

    try:
        session.execute(sql)
        # session.commit()
    except Exception as e:
        print(e)

def update_print_record(session,tjbh,login_id,login_name,addr):
    if '10.8.102.' or '10.8.103.' or '10.8.104.' or '10.7.103.' or '10.8.200' in addr:
        jllx = '0038'
        jlmc = '报告网上打印'
    else:
        jllx = '0039'
        jlmc = '报告网上下载'

    sql = "INSERT TJ_CZJLB(JLLX,TJBH,MXBH,CZGH,CZSJ,CZQY,CZXM,JLMC)VALUES('%s','%s','','','%s','%s','','%s')" %(jllx,tjbh,cur_datetime(),addr,jlmc)

    try:
        session.execute(sql)
        # session.commit()
    except Exception as e:
        print(e)

# 构建图
def build_chart(title: str, datas: dict):
    axis_x = [str2(key) for key in datas.keys()]
    axis_y = list(datas.values())
    bar = Bar()
    # 通用配置项都在add()中进行配置 具体见官网 http://pyecharts.org/#/
    bar.add(title, axis_x, axis_y, is_more_utils=True, xaxis_rotate=90)
    return bar

def get_datas(session,title,tstart,tend):
    if title == '报告审阅':
        sql = "SELECT SYXM,COUNT(SYXM) AS RC FROM TJ_BGGL WHERE SYRQ>='%s' AND SYRQ<'%s' AND SYXM IS NOT NULL GROUP BY SYXM ORDER BY COUNT(SYXM) ASC;" % (
        tstart, tend)
    elif title == '报告打印':
        sql = "SELECT DYXM,COUNT(DYXM) AS RC FROM TJ_BGGL WHERE DYRQ>='%s' AND DYRQ<'%s' AND DYXM IS NOT NULL GROUP BY DYXM ORDER BY COUNT(DYXM) ASC;" % (
        tstart, tend)
    elif title == "报告整理":
        sql = "SELECT ZLXM,COUNT(ZLXM) AS RC FROM TJ_BGGL WHERE ZLRQ>='%s' AND ZLRQ<'%s' AND ZLXM IS NOT NULL GROUP BY ZLXM ORDER BY COUNT(ZLXM) ASC;" % (
        tstart, tend)
    elif title == "报告追踪":
        sql = "SELECT CZXM,COUNT(CZXM) AS RC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s' AND JLLX='0030' GROUP BY CZXM ORDER BY COUNT(CZXM); " % (
        tstart, tend)
    elif title == "样本采集":
        sql = "SELECT CZXM,COUNT(CZXM) AS RC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s' AND JLLX='0010' GROUP BY CZXM ORDER BY COUNT(CZXM); " % (
        tstart, tend)
    elif title == "呼气检查":
        sql = "SELECT CZXM,COUNT(CZXM) AS RC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s' AND JLLX='0026' AND SJFS='4' GROUP BY CZXM ORDER BY COUNT(CZXM); " % (
        tstart, tend)
    elif title == "心电图检查":
        sql = "SELECT CZXM,COUNT(CZXM) AS RC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s' AND JLLX='0021' GROUP BY CZXM ORDER BY COUNT(CZXM); " % (
        tstart, tend)
    elif title == "骨密度检查":
        sql = "SELECT CZXM,COUNT(CZXM) AS RC FROM TJ_CZJLB WHERE CZSJ>='%s' AND CZSJ<'%s' AND JLLX='0020' GROUP BY CZXM ORDER BY COUNT(CZXM); " % (
        tstart, tend)

    elif title == '登录人数':
        sql = ''' SELECT login_date,COUNT(login_name) as rc 
        FROM (SELECT DISTINCT substring(convert(char,login_in,120),1,10) as login_date, login_name from TJ_LOGIN WHERE login_in>='%s' AND login_in<'%s'
        ) AS tmp GROUP BY login_date ''' %(tstart, tend)
    else:
        sql =None
        return
    results = session.execute(sql).fetchall()
    return OrderedDict(results)
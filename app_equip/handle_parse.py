import requests,xmltodict
from app_equip.handle_equip import *
from app_equip.handle_pdf import *
from app_equip.model import *

# @author: zhufd
# @license: (C) Copyright 明州体检
# @contact: 245838515@qq.com
# @software: HMS(健康管理系统)
# @file: handle_parse.py
# @date: 2018-12-23
# @desc:业务处理包，解析过程、日志、数据库操作，提供给外层服务

# 总入口：解析文件
def equip_file_parse(filename,session,log,process_queue,
                     login_id,login_name,login_area, host_name, host_ip,
                     equip_type,url,xmbh,czlj_info,equip_info,
                     file_types:list,path_parse,path_error,file_handle=True):
    '''
    :param filename: 文件名，带路径
    :param session: 数据库会话
    :param log: 日志对象
    :param process_queue:进程队列
    :param login_id: 登录ID
    :param login_name: 登录姓名
    :param host_name: 登录主机
    :param host_ip: 登录IP
    :param equip_type: 设备类型
    :param url: 上传URL
    :param xmbh: 项目编号
    :param czlj_info: 数据操作对象，TJ_CZJLB
    :param equip_info: 数据操作对象，TJ_TJJLMXB
    :param file_types: 文件类型，列表类型
    :param path_parse: 解析成功->文件存放路径
    :param path_error: 解析失败->文件存放路径
    :param file_handle: 解析成功->是否删除原文件
    :return:
    '''
    # 前缀名 后缀名
    # file_prefix = os.path.splitext(filename)[0]
    file_suffix = os.path.splitext(filename)[1]
    if file_suffix not in file_types:
        return
    # 解析 电测听 数值
    if file_suffix == '.gnd':
        tjbh,jcrq,result,error = get_so_ac_result(filename)
        if error:
            log.info("文件：%s 解析电测听结果失败：%s" %(filename,error))
            return
        # 校正听力值并更新数据库
        insert_cyct(session, login_id, login_name,login_area,tjbh,jcrq,result, host_name, host_ip)
    elif file_suffix == '.pdf':
        # PDF 文件解析
        values = pdfhandle(filename, equip_type, path_parse, path_error, url,
                           log, file_handle)
        if not values:
            return
        tjbh,jcrq, file_new, file_up = values
        equip_info['file_path'] = file_up
        equip_info['tjbh'] = tjbh
        # 项目结果定制
        xmjg = "结果详见%s附件" % EquipName.get(equip_type)
        # 数据库处理
        dbhandle(
            session=session,
            log=log,
            login_id=login_id,
            tjbh=tjbh,
            xmbh=xmbh,
            xmjg=xmjg,
            jcrq=jcrq,
            filename=file_new,
            czjl_obj=czlj_info,
            equip_obj=equip_info
        )
        # 返回 消息给 UI
        if process_queue:
            process_queue.put(tjbh)
            log.info("向主进程UI传递消息：%s" % tjbh)
        # 转换为图片 再上传
        pichandle(file_new, xmbh, log, url)


def pichandle(file_name,xmbh,log,url):
    t1 = time.time()
    if xmbh=='0806':
        file_pic = pdf2pic(file_name,rotate=90)
    else:
        file_pic = pdf2pic(file_name)
    t2 = time.time()
    log.info("Pdf(%s)->Pic(%s)转换成功！耗时：%s秒" % (file_name,file_pic, str(round(t2-t1, 2))))
    response = api_equip_upload(url, file_pic)
    if response:
        log.info("文件(%s)：上传成功！" % file_pic)
    else:
        log.info("文件(%s)：上传失败！" % file_pic)

# PDF文件解析、上传
def pdfhandle(file_name,equip_type,path_parse,path_error,up_url,log,is_file_remove=True):
    '''
    :param file_name: 待处理的文件
    :param equip_type: 设备类型
    :param path_parse: 解析目录
    :param path_error: 错误目录
    :param up_url: 上传URL
    :param log: 日志对象
    :param is_file_remove: 是否删除文件
    :return:空/(体检编号，新文件名，上传后的文件名) 注：所有文件均带路径
    '''
    t1= time.time()
    lstr = pdf2txt(file_name)
    t2 = time.time()
    if not lstr:
        log.info("文件：%s 解析为文本，耗时：%s 秒，解析失败。" % (file_name, round(t2 - t1, 2)))
        return
    log.info("文件：%s 解析为文本，耗时：%s 秒。" %(file_name,round(t2-t1,2)))
    tjbh,jcrq = txt2tjbh(lstr,equip_type)
    t3 = time.time()
    if not tjbh:
        error_file = os.path.join(path_error,os.path.basename(file_name))
        shutil.copy2(file_name, error_file)
        os.remove(file_name)
        log.info("文件：%s 提取体检编号，耗时：%s 秒，提取失败，转移至error目录。" % (file_name, round(t3 - t2, 2)))
        return
    log.info("文件：%s 提取体检编号，耗时：%s 秒。" % (file_name, round(t3 - t2, 2)))
    new_file = os.path.join(path_parse,"%s_%s.pdf" %(tjbh,equip_type))
    # 移动文件目录 从create->parse
    shutil.copy2(file_name, new_file)
    # 上传文件
    response = api_equip_upload(up_url, new_file)
    t3 = time.time()
    if not response:
        log.info("文件：%s 上传失败，耗时：%s 秒。" % (new_file, round(t3 - t2, 2)))
        return
    file_up = response['data']
    log.info("文件：%s 上传成功，耗时：%s 秒。" % (new_file, round(t3 - t2, 2)))
    # 删除原文件
    if is_file_remove:
        os.remove(file_name)

    return tjbh,jcrq,new_file,file_up

# 操作日志
def db_czjl(session,log,tjbh,czjl_obj):
    czjl_obj['tjbh'] = tjbh
    czjl_obj['czsj'] = cur_datetime()
    # 更新记录：TJ_CZJLB
    try:
        session.bulk_insert_mappings(MT_TJ_CZJLB, [czjl_obj])
        session.commit()
    except Exception as e:
        session.rollback()
        log.info("体检顾客：%s，插入表TJ_CZJLB失败！错误信息：%s" %(tjbh,e))

# 设备接口
def db_equip(session,log,tjbh,xmbh,equip_obj):
    result = session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == tjbh,
                                               MT_TJ_EQUIP.xmbh == xmbh).scalar()
    if result:
            # 存在则更新,PDF更新
            session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh == tjbh,
                                              MT_TJ_EQUIP.xmbh == xmbh
                                                   ).update(
                                                            {
                                                                MT_TJ_EQUIP.modify_time: cur_datetime(),
                                                                MT_TJ_EQUIP.file_path: equip_obj['file_path'],            # 上传后的路径
                                                                # MT_TJ_EQUIP.operator: equip_obj['operator'],              # 操作工号
                                                                # MT_TJ_EQUIP.operate_time: equip_obj['operate_time'],      # 操作时间
                                                                # MT_TJ_EQUIP.hostname: equip_obj['hostname'],
                                                                # MT_TJ_EQUIP.hostip: equip_obj['hostip'],
                                                                # MT_TJ_EQUIP.operator2: equip_obj['operator2'],            # 操作姓名
                                                                MT_TJ_EQUIP.operate_area: equip_obj['operate_area'],      # 操作区域
                                                             }
                                                            )
            session.commit()
    else:
        try:
            equip_obj['create_time'] = cur_datetime()
            session.bulk_insert_mappings(MT_TJ_EQUIP, [equip_obj])
            session.commit()
        except Exception as e:
            session.rollback()
            log.info("体检顾客：%s，插入表TJ_EQUIP失败！错误信息：%s" % (tjbh, e))

# 项目明细
def db_jlmx(session,log,tjbh,xmbh,xmjg,jcrq,login_id):
    # 人体成分、电测听直接项目结束
    # 心电图、骨密度 则ZXPB=3
    result = session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.xmbh == xmbh).scalar()
    if result:
        if result.jsbz == '1':
            zxpb = '1'
            jsbz = '1'
        elif xmbh in ['0310','5402']:
            zxpb = '1'
            jsbz = '1'
        else:
            zxpb = '3'
            jsbz = '0'
        try:
            if xmbh == '0310':
                # 不更新
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == xmbh).update({
                    MT_TJ_TJJLMXB.zxpb: zxpb,
                    MT_TJ_TJJLMXB.jsbz: jsbz,
                    MT_TJ_TJJLMXB.qzjs: None,
                })
            elif xmbh == '5402':
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == xmbh).update({
                    MT_TJ_TJJLMXB.zxpb: zxpb,
                    MT_TJ_TJJLMXB.jsbz: jsbz,
                    MT_TJ_TJJLMXB.qzjs: None,
                    MT_TJ_TJJLMXB.jcys: login_id,
                    MT_TJ_TJJLMXB.jcrq: cur_datetime(),
                    MT_TJ_TJJLMXB.jg:xmjg
                })
            else:
                session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == tjbh,MT_TJ_TJJLMXB.zhbh == xmbh).update({
                    MT_TJ_TJJLMXB.zxpb: zxpb,
                    MT_TJ_TJJLMXB.jsbz: jsbz,
                    MT_TJ_TJJLMXB.qzjs: None,
                    MT_TJ_TJJLMXB.jcys: login_id,
                    MT_TJ_TJJLMXB.jcrq: jcrq,
                    MT_TJ_TJJLMXB.jg:xmjg
                })
            session.commit()
        except Exception as e:
            session.rollback()
            log.info("体检顾客：%s，更新表TJ_TJJLMXB失败！错误信息：%s" % (tjbh, e))
    else:
        log.info("体检顾客：%s，不存在项目：%s,请确认！" % (tjbh, xmbh))


# 心电图 特殊处理，插入数据库
def db_xdt(session,log,tjbh,filename):
    dcp_obj = {}
    dcp_obj['cusn'] = tjbh
    dcp_obj['department'] = '0018'
    dcp_obj['filename'] = '%s.PDF' % tjbh
    dcp_obj['filecontent'] = open(filename, 'rb').read()
    dcp_obj['uploadtime'] = cur_datetime()
    dcp_obj['flag'] = '0'
    try:
        session.query(MT_DCP_files).filter(MT_DCP_files.cusn == tjbh).delete()
        session.bulk_insert_mappings(MT_DCP_files, [dcp_obj])
        session.commit()
    except Exception as e:
        session.rollback()
        log.info("体检顾客：%s，插入表DCP_files失败！错误信息：%s" % (tjbh, e))

# 整合数据库处理
def dbhandle(session,log,login_id,tjbh,xmbh,xmjg,jcrq,filename,czjl_obj:dict,equip_obj:dict):
    db_czjl(session,log,tjbh,czjl_obj)
    db_equip(session,log,tjbh,xmbh,equip_obj)
    db_jlmx(session,log,tjbh,xmbh,xmjg,jcrq,login_id)
    if xmbh=='0806':
        db_xdt(session,log,tjbh,filename)

# post 请求
def api_equip_upload(url, filename):
    file_obj = {"file": (filename, open(filename, "rb"))}
    try:
        response = requests.post(url, files=file_obj)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print('URL：%s 请求失败！错误信息：%s' % (url, e))

#### 电测听取值
def minus_list(list1:list,list2:list):
    return list(map(lambda x,y:x - y,list1,list2))

def merge_list(list1:list):
    return  '|'.join([str(i) for i in list1])

#单耳听阈加权值（dB）
def f_avg(result:list):
    return int(((result[0]+result[1]+result[2])/3)*0.9+result[4]*0.1)

#双耳高频平均听阈（dB）
def f_avg2(result1:list,result2:list):
    return int((result1[3]+result1[4]+result1[5]+result2[3]+result2[4]+result2[5])/6)

#单耳平均听阈（dB）
def f_avg3(result:list):
    return int((result[3] + result[4] + result[5]) / 3)

#结果是否合格判断
def is_hg(result1:list,result2:list):
    if all([f_avg(result1)<25,f_avg(result2)<25,f_avg2(result1,result2)<40]):
        return '合格'
    else:
        return '不合格'

# 获取气导的数值，骨导不参与计算
def get_so_ac_result(file_name):
    with open(file_name,encoding="utf-8") as f:
        content = xmltodict.parse(f.read())
    # 获取本次检查记录
    session = content.get('Session',None)
    if not session:
        return None,None,None,"检查记录为空"
    # 获取体检编号
    tjbh = parse_nestdict(session,'Actors.Client.@Id')
    if not tjbh:
        return None,None,None,"体检编号获取失败"
    # 获取检查日期
    jcrq_tmp = session.get('@Date',None)
    if not jcrq_tmp:
        jcrq = cur_datetime()
    else:
        jcrq = jcrq_tmp[0:19].replace('T', ' ')
    # 获取结果信息
    results_tmp = session.get('Action',None)
    if not results_tmp:
        return tjbh,jcrq,results_tmp,"结果信息获取失败"
    tmp = {}
    result_key = 'Public.TAudioSession.ToneTHRAudiogram.TToneTHRAudiogram'      # 结果信息 路径
    so_key_key = 'MeasCond.@SignalOutput1'                                      # 气导、骨导 标记路径 以SignalOutput1 输出为主
    so_result_key = 'Curve.TTonePoint'                                          # 气导、骨导 结果路径，左、右耳
    so_value_key = '@Intensity1'                                                # 结果值 路径

    if isinstance(results_tmp,list):
        # 多组结果：可能是骨导+气导，也可能是多组气导
        for result_tmp in results_tmp:
            results = parse_nestdict(result_tmp,result_key)
            for result in results:
                so_key = parse_nestdict(result, so_key_key)
                # 获取列表
                so_value = [int(int(i.get(so_value_key, 0)) / 10) for i in parse_nestdict(result, so_result_key)]
                # 获取字典
                # so_value = dict((int(i.get('@Freq1', 0)),int(int(i.get('@Intensity1', 0)) / 10)) for i in parse_nestdict(result, so_result_key))
                if len(so_value) == 6:
                    tmp[so_key] = so_value
                else:
                    return tjbh,jcrq,None,"%s的数值不足6组:%s" %(so_key,str(so_value))

    else:
        # 单组结果，则为气导
        ac_results = parse_nestdict(results_tmp,result_key)
        for ac_result in ac_results:
            so_key = parse_nestdict(ac_result, so_key_key)
            # 获取列表
            so_value = [int(int(i.get(so_value_key, 0)) / 10) for i in parse_nestdict(ac_result, so_result_key)]
            # 获取字典
            # so_value = dict((int(i.get('@Freq1', 0)), int(int(i.get('@Intensity1', 0)) / 10)) for i in parse_nestdict(ac_result, so_result_key))
            if len(so_value) == 6:
                tmp[so_key] = so_value
            else:
                return tjbh, jcrq, None, "%s的数值不足6组:%s" % (so_key, str(so_value))


    return tjbh,jcrq,tmp,''

#获取纯音听力原始记录，校正后插入到TJ_EQUIP
def insert_cyct(session,login_id,login_name,login_area,tjbh,jcrq,result,host_name,host_ip,xmbh='0310'):
    # 从数据库中校对人员信息
    result_user = session.execute(get_tjxx_sql(tjbh)).fetchone()
    if not result_user:
        print("未找到体检编号为：%s的人员信息" %tjbh)
        return
    user_name = str2(result_user[1])     # 用户姓名
    user_sex = str2(result_user[2])      # 用户性别
    user_age = result_user[-1]           # 用户年龄

    if user_age>=22:
        #result = session.execute(standard_audition_sql(user_age, user_sex)).fetchone()
        # if result:
        #     standard_result = dict(zip([500,1000,2000,3000,4000,6000],[int(i[1]) for i in result]))
        results = session.execute(standard_audition_sql(user_age,user_sex)).fetchall()
        if results:
            result_tmp = sorted(results[0].items(), key=lambda item: item[0])
            standard_result = [int(i[1]) for i in result_tmp]
        else:
            standard_result = [0, 0, 0, 0, 0, 0]
            # standard_result = {500: 0, 1000: 0, 2000: 0, 3000: 0, 4000: 0, 6000: 0}
    else:
        standard_result = [0, 0, 0, 0, 0, 0]
        # standard_result = {500: 0, 1000: 0, 2000: 0, 3000: 0, 4000: 0, 6000: 0}
    #
    result["so_ACR_new"] = minus_list(result["so_ACR"], standard_result)
    result["so_ACL_new"] = minus_list(result["so_ACL"], standard_result)
    result["so_ACR_init"] = standard_result
    result["so_ACL_init"] = standard_result
    xmzd = is_hg(result["so_ACL_new"], result["so_ACR_new"])
    # 计算校正结果
    ms1 = merge_list(result["so_ACR"]) + '|' + merge_list(result["so_ACL"])
    ms2 = merge_list(result["so_ACR_new"]) + '|' + merge_list(result["so_ACL_new"])
    ms3 = merge_list(result["so_ACR_init"]) + '|' + merge_list(result["so_ACL_init"])
    ms4 = "右耳平均语频=%s\n" \
          "右耳平均高频=%s\n" \
          "左耳平均语频=%s\n" \
          "左耳平均高频=%s\n" \
          "双耳高频平均听阈=%s" % (f_avg(result["so_ACR_new"]), f_avg3(result["so_ACR_new"]),
                           f_avg(result["so_ACL_new"]), f_avg3(result["so_ACL_new"]),
                           f_avg2(result["so_ACR_new"], result["so_ACL_new"]))

    xmjg = '||||' + ms1 + '|||||' + ms2 + '|||||' + ms3 + '|$' + ms4
    try:
        # 表 TJ_EQUIP
        result = session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh==tjbh,MT_TJ_EQUIP.xmbh==xmbh).scalar()
        if result:
            # 不更新第一次操作用户
            session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh==tjbh,MT_TJ_EQUIP.xmbh==xmbh).update({
                MT_TJ_EQUIP.operate_time:jcrq,
                MT_TJ_EQUIP.equip_jg1:xmjg,
                MT_TJ_EQUIP.equip_jg2:xmzd
            })
            zxpb = '1'
            jsbz = '1'
        else:
            session.execute(insert_dct_sql(tjbh,cur_datetime(),user_name,jcrq,host_name,host_ip,xmjg,xmzd,login_id,login_name,login_area))
            zxpb = '3'
            jsbz = '0'
        # 表 TJ_TJJLMXB
        session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh==tjbh,MT_TJ_TJJLMXB.zhbh==xmbh).update({
            MT_TJ_TJJLMXB.zxpb: zxpb,
            MT_TJ_TJJLMXB.jsbz: jsbz,
            MT_TJ_TJJLMXB.qzjs: None,
            MT_TJ_TJJLMXB.jcrq: jcrq,
            MT_TJ_TJJLMXB.jcys: login_id,
            MT_TJ_TJJLMXB.jg: xmjg,
            MT_TJ_TJJLMXB.zd: xmzd,
            MT_TJ_TJJLMXB.shrq: jcrq,
            MT_TJ_TJJLMXB.shys: '120502002',
        })
        # 表 TJ_CZJLB 不做处理，由PDF文件上传时来处理
        session.commit()
        print("%s 体检顾客：%s，纯音测听结果（%s）解析成功！" % (cur_datetime(),user_name,xmjg))
    except Exception as e:
        session.rollback()
        print("执行数据库出错：%s" %e)

# 确认路径，不存在则创建
def mkdir(path,log):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        log.info("路径：%s 已启动监控。" %path)
        return True
    except Exception as e:
        log.info('路径：%s 不准确，请调整！错误信息：%s' %(path,e))
        return False

# 设备信息
EquipName={
    '01':'电测听',
    '02':'人体成分(投放)',
    '03':'人体成分',
    '04':'骨密度',
    '05':'超声骨密度',
    '06':'动脉硬化',
    '07':'大便隐血',
    '08':'心电图',
    '11':'肺功能',
    '12':'胸部正位'
}

# 设备信息
EquipNo={
    '01':'0310',
    '02':'5402',
    '03':'5402',
    '04':'501576',
    '05':'1000074',
    '06':'5401',
    '07':'2113',
    '08':'0806',
    '11':'0045',
    '12':'501716'
}

# 设备动作点
EquipAction={
    '01':'0023',
    '02':'0022',
    '03':'0022',
    '04':'0020',
    '05':'1000074',
    '06':'0024',
    '07':'2113',
    '08':'0021',
    '11':'0045',
    '12':'501716'
}

# 设备动作点
EquipActionName={
    '01':'电测听检查',
    '02':'人体成分检查',
    '03':'人体成分检查',
    '04':'骨密度检查',
    '05':'超声骨密度检查',
    '06':'动脉硬化检查',
    '07':'大肠癌检查',
    '08':'心电图检查',
    '11':'肺功能检查',
    '12':'DR检查'
}

# 嵌套字典解析
def parse_nestdict(nestdict:dict,keys:str,default=None):
    keys_list = keys.split('.')
    tmp = nestdict
    for key in keys_list:
        if isinstance(tmp,dict):
            val = tmp.get(key, None)
        else:
            val = None
        if val!= None:
            tmp = val
        else:
            return default

    return tmp

if __name__=="__main__":
    from pprint import pprint
    pprint(get_so_ac_result(r"E:\DR\create\01\My Suite\178240009 龙元明, (男) 2019-01-02T14.58.02.1866546+08.00.gnd"))

    # for root, dirs, files in os.walk(r"E:\DR\create\01\My Suite"):
    #     if files and not dirs:  # 必须是指定目录的下级目录
    #         for file in files:
    #             try:
    #                 print(get_so_ac_result(os.path.join(root, file)))
    #             except Exception as e:
    #                 print(os.path.join(root, file))
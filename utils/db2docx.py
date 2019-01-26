'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: db2docx.py
@time: 2019-1-18 8:32
@desc: 自动写入word文档
'''

from utils.bmodel import *
from utils.dbconn import get_tjxt_session
from docxtpl import DocxTemplate,RichText
from pydocx import PyDocX
import os
from win32com import client


def doc2pdf(doc_name, pdf_name):
    """
    :word文件转pdf
    :param doc_name word文件名称
    :param pdf_name 转换后pdf文件名称
    """
    try:
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
        return pdf_name
    except Exception as e:
        print(e)
        return


def get_info(session,tjbh):
    datas = {}
    # 所有组合
    citems = []
    # 所有子项
    sitems = {}
    results = session.query(V_JGMXB).filter(V_JGMXB.TJBH==tjbh).all()
    if not results:
        return datas
    for result in results:
        datas['user'] = result.get_user()
        if result.SFZH=='1':
            citems.append(result.get_citem())
        else:
            if result.ZHBH not in sitems:
                sitems[result.ZHBH] = []
            sitems[result.ZHBH].append(result.get_sitem())

    # 将子项明细打包进组合
    for citem in citems:
        citem['ZHBH'] = sitems[citem['ZHBH']]

    datas['items'] = citems

    return datas

def render_docx_template(template_file,filename,context):
    template_obj = DocxTemplate(template_file)
    template_obj.render(context)
    template_obj.save(filename)

def docx2html(docx_file,html_file):
    html = PyDocX.to_html(docx_file)
    f = open(html_file, 'w', encoding="utf-8")
    f.write(html)
    f.close()

if __name__=="__main__":
    template_file = r'C:\Users\Administrator\Desktop\word\检查表.docx'
    docx_file = r'C:\Users\Administrator\Desktop\word\检查表1.docx'
    pdf_file = r'C:\Users\Administrator\Desktop\word\检查表1.pdf'
    session = get_tjxt_session('10.8.200.201','tjxt','bsuser','admin2389')
    context = get_info(session,'180080244')
    render_docx_template(template_file,docx_file,context)
    doc2pdf(docx_file,pdf_file)


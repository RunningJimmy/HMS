from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from wand.image import Image
import os

# @author: zhufd
# @license: (C) Copyright 明州体检
# @contact: 245838515@qq.com
# @software: HMS(健康管理系统)
# @file: handle_pdf.py
# @date: 2018-12-20
# @desc:PDF处理工具包,与业务无关

# https://blog.csdn.net/xingxtao/article/details/79056341

# PDF转换文本
def pdf2txt(pdf_name):

    file = open(pdf_name, 'rb')             #  以二进制读模式打开
    praser = PDFParser(file)                #  用文件对象来创建一个pdf文档分析器
    doc = PDFDocument()                     #  创建一个PDF文档
    praser.set_document(doc)                #  连接分析器 与文档对象
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pdfStrList = []
    # 循环遍历列表，每次处理一个page的内容
    for page in doc.get_pages():            # doc.get_pages() 获取page列表
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        for x in layout:
            if hasattr(x, "get_text"):
                pdfStrList.append(x.get_text())
            else:
                pass
    return pdfStrList

# PDF转换图片
def pdf2pic(filename,rotate=0,resolution=300,format='png'):
    '''
    :param filename: PDF文件带路径
    :param rotate: 图片旋转角度，默认不旋转
    :param resolution: 图片分辨率
    :param format: 图片格式
    :return:filename 图片文件带路径
    '''
    pic_name = str(os.path.splitext(filename)[0]) +'.'+ format
    img_obj = Image(filename=filename, resolution=resolution)
    req_image = []
    for img in img_obj.sequence:
        img_page = Image(image=img)
        if rotate:
            img_page.rotate(rotate)
        req_image.append(img_page.make_blob(format))
    # 遍历req_image,保存为图片文件
    i = 0
    for img in req_image:
        ff = open(pic_name, 'wb')
        ff.write(img)
        ff.close()
        i += 1

    return pic_name

# 研究用
def pdf2pic2(pdf_name):
    pic_name = str(os.path.splitext(pdf_name)[0]) + '.png'
    with Image(filename=pdf_name, resolution=300) as img:
        with img.convert('png') as converted:
            converted.save(filename=pic_name)

# PDF剪切
def pdf2cut(pdf_in,pdf_out,axis_x,axis_y,width,height):
    pdf_read_obj = PdfFileReader(open(pdf_in, 'rb'))
    pdf_write_obj = PdfFileWriter()
    for page in pdf_read_obj.pages:
        page.mediaBox.setUpperLeft((axis_x, axis_y))
        page.mediaBox.setUpperRight((width, height))
        page.mediaBox.setLowerLeft((axis_x, axis_y-height))
        page.mediaBox.setLowerRight((axis_x+width, axis_y-height))
        pdf_write_obj.addPage(page)

    with open(pdf_out, 'wb') as f:
        pdf_write_obj.write(f)
        f.close()
    return pdf_out
    # ous = open(out_file, 'wb')
    # self.pdf_write.write(ous)
    # ous.close()

# 分割PDF，历史报告打印时用，历史报告心电图横向的
def pdfSplit(pdf_main,pdf_part):
    try:
        pdf_read_obj = PdfFileReader(pdf_main)
        pdf_write_obj = PdfFileWriter()
        page_num = pdf_read_obj.getNumPages()
        page_last_obj = pdf_read_obj.getPage(page_num - 1)
        page_last_obj.rotateClockwise(90)
        pdf_write_obj.addPage(page_last_obj)
        pdf_write_obj.write(open(pdf_part, 'wb'))
        return page_num - 1
    except Exception as e:
        return False
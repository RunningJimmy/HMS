'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: 2222222.py
@time: 2019-1-17 15:23
@desc: 
'''

from docxtpl import DocxTemplate, RichText


tpl = DocxTemplate(r'C:\Users\Administrator\Desktop\检查表.docx')

context = {
    'datas': [
        {'date': '2015-03-10', 'desc': RichText('Very critical alert', color='FF0000', bold=True), 'type': 'CRITICAL','bg': 'FF0000'},
        {'date': '2015-03-11', 'desc': RichText('Just a warning'), 'type': 'WARNING', 'bg': 'FFDD00'},
        {'date': '2015-03-12', 'desc': RichText('Information'), 'type': 'INFO', 'bg': '8888FF'},
        {'date': '2015-03-13', 'desc': RichText('Debug trace'), 'type': 'DEBUG', 'bg': 'FF00FF'},
    ],
}

tpl.render(context)
tpl.save(r'C:\Users\Administrator\Desktop\检查表1.docx')

# encoding:utf-8

import sys
import importlib
import glob
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

error_file = open('./error.txt', 'w')
parse_error_file = open('./parse_error.txt', 'w')
'''
 解析pdf 文本，保存到txt文件中
'''
def parse(pdf_file):
    fp = open(pdf_file, 'rb') # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    try:
        praser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)
    
        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()
    except Exception as e:
        parse_error_file.write(pdf_file+'\n')
        return
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        try:
            pages = list(doc.get_pages())
        except Exception as e:
            parse_error_file.write(pdf_file+'\n')
            return 
        results = ""
        print(f"pages num is {dir(doc.get_pages())}")
        # 循环遍历列表，每次处理一个page的内容
        for page in pages[6:60]: # doc.get_pages() 获取page列表
            try:
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        results += x.get_text()
                        # print(x.get_text())
            except Exception as e:
                pass 

        if len(results)>0:
            txtfile_name = pdf_file[:-4]+'.txt'
            with open(txtfile_name, 'w', encoding='utf-8') as f:

                begin = results.find(u"第四节 经营") if results.find(u"第四节 经营")>0 else 0
                end = results.find(u"第五节 重要") if results.find(u"第五节 重要")>0 else len(results)
                print(f"begin is {begin}, end is {end}")
                if results.find(u"九、公司未来")<0:
                    error_file.write(pdf_file+'\n')            
                f.write(results[begin:end])
                print(f"Succefully writing content into the {txtfile_name} file.")
        else:
            parse_error_file.write(pdf_file+'\n')
            

def parse_pdfs(m_dir='./annual_report'):
	pdf_files = glob.glob(m_dir+'/*.pdf')
	for pdf_file in pdf_files:
		parse(pdf_file)


if __name__ == '__main__':
	# print(parse('fw9.pdf'))
	parse_pdfs(m_dir='./annual_report2016')

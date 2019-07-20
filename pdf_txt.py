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
'''
 解析pdf 文本，保存到txt文件中
'''
def parse(pdf_file):
    fp = open(pdf_file, 'rb') # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    
    txtfile_name = pdf_file[:-4]+'.txt'
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

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

        results = ""
        with open(txtfile_name, 'w', encoding='utf-8') as f:
            # 循环遍历列表，每次处理一个page的内容
            for page in list(doc.get_pages())[8:50]: # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        results += x.get_text()
                        #page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
                        #page_content = '\n'.join(page.extract_text().split('\n')[:-1])
                        # print(results)
            begin = results.find(u"第四节 经营") if results.find(u"第四节")>0 else 0
            end = results.find(u"第五节 重要") if results.find(u"第五节")>0 else len(results)
            results = results[begin:end]
            begin = results.find(u"九、公司未来") 
            # end = results.find(u"十、") if results.find(u"十、")>0 else len(results)
            if results.find(u"九、公司未来")>0:
                # results += results[begin:end]
                pass
            else:
                error_file.write(pdf_file+'\n')
            f.write(results)
            print(f"Succefully writing content into the {txtfile_name} file.")

def parse_pdfs(m_dir='./annual_report'):
	pdf_files = glob.glob(m_dir+'/*.pdf')
	for pdf_file in pdf_files:
		parse(pdf_file)


if __name__ == '__main__':
	# print(parse('fw9.pdf'))
	parse_pdfs()
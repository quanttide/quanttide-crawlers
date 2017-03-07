# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3

# modify system default encoding
# with two statements of modifying, most of the encoding problems will be avoided
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  

#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-23'

__creation_date__ = '2016-6-23'

__moduleVersion__ = '1.0'

__doc__ = '''
A PDF parser
'''

__reference = '''
https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
'''

#----------module document----------


#----------module import----------

# import system modules
import codecs
import re
from cStringIO import StringIO

# import third-party modules
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# import my own modules
from decorator import printTime

#----------module import----------


#----------function definition----------

@printTime
def convert(fname,Converter='HTML',pages=None,write=False):
    '''
    Converter: 'HTML','Text','XML'
    pages: [beginPage, endPage]
    '''
    if not pages:
        pagenums = set()
    else:
        pages = map((lambda x:x-1),pages)
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    
    if Converter == 'HTML':
        converter = HTMLConverter(manager, output, laparams=LAParams())
    elif Converter == 'Text':
        converter = TextConverter(manager, output, laparams=LAParams())
    elif Converter == 'XML':
        converter = XMLConverter(manager, output, laparams=LAParams())
        
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    
    if write:
        if Converter=='HTML':
            format = '.html'
        elif Converter=='Text':
            format = '.txt'
        elif Converter == 'XML':
            format = '.xml'
        writeFile(fname,text,format)
    else:
        return text 


def writeFile(fname,text,format='.html'):
    pattern = re.compile('.*.pdf')
    match = pattern.match(fname)
    if match:
        new_fname = re.sub('.pdf',format,fname)
    else:
        new_fname = fname + format

    with codecs.open(new_fname,'wb') as f:
        f.write(text)
    
#----------function definition----------


#----------main function----------

if __name__ =='__main__':
    fname = 'testPDF.pdf'
    convert(fname,write=True)


#----------main function----------
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

__date__ = '2016-5-29'

__moduleVersion__ = ''

__doc__ = '''
Write data into .csv or databases.
#Without solving the encoding problem of .csv.
'''


#----------module document----------


#----------module import----------

# import system modules
import csv
import codecs
import os

# import third-party modules

# import my own modules

#----------module import----------


#----------function definition----------

def createFile(dictName,fileName,csv = False,*labels):
    # check or create a daily dictionary
    try:
        os.makedirs(dictName)
    except OSError, e:
        if e.errno != 17:
            raise(e)
        
    if csv:   
        fileName = ''.join([dictName,'/',fileName,'.csv'])
    else:
        fileName = ''.join([dictName,'/',fileName])
        
    # with 'labels', it will rewrite the file with 'fileName';
    # without 'labels', it will only return 'fileName' without cover the old file     
    if labels:
        with codecs.open(fileName,'wb',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(labels)
    
    return fileName


def writeCSV(fileName,*data):
    with codecs.open(fileName,'ab',encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    return True

#----------function definition----------


#----------main function----------


#----------main function----------
if __name__ == '__main__':
    fileName = createFile(dictName='sample', fileName='sample')
    data =['木有','真的']
    writeCSV(fileName,*data)
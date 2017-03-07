# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-26'

__creation_date__ = '2016-6-26'

__moduleVersion__ = '1.0'

__doc__ = '''
This is a data cleaning module for China's Prices Project.
'''

#----------module document----------

#----------module import----------

# import system modules
import re

#----------module import----------


#----------function definition----------

def dealSales(sales):
    'Clean "万" for sale data.'
    
    pattern_ten_th = re.compile('万')
    pattern_num = re.compile('^\d+\.?\d*')
    match = re.search(pattern_ten_th, sales)
    if match:
        match_num = re.search(pattern_num, sales)
        num = int(float(match_num.group(0)) * 10000)
        return num
    else:
        match_num = re.search(pattern_num,sales)
        num = int(match_num.group(0))
        return num

#----------function definition----------


#----------main function----------

if __name__=='__main__':
    print(dealSales('3.6万笔'))
    
#----------main function----------
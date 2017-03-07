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

__date__ = '2016-5-28'

__moduleVersion__ = ''

__doc__ = '''

'''


#----------module document----------


#----------module import----------

# import system modules
import time

# import third-party modules

# import my own modules

#----------module import----------


#----------global variables----------

global_variables = ''

#----------global variables----------


#----------class definition----------

class Class(object):
    pass

#----------class definition----------


#----------function definition----------

def func():
    pass

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    # main function
    end = time.time()
    print('time:',end-begin)

#----------main function----------

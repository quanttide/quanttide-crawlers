# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-18'

__creation_date__ = '2016-6-18'

__moduleVersion__ = '1.1'

__doc__ = '''
This is a decorator module for China's Prices Project
'''


#----------module document----------


#----------module import----------

# import system modules
import time

#----------module import----------


#----------function definition----------

def printTime(func):
    def _deco(*args,**kwargs):
        begin = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print('time:',func.__name__,end-begin)
        return result
    return _deco


@printTime
def func():
    time.sleep(1)
    
#----------function definition----------
    
    
#----------main function----------

if __name__=="__main__":
    func()
    
#----------main function----------
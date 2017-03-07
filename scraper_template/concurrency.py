# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-18'

__creation_date__ = '2016-6-18'

__moduleVersion__ = '1.0'

__doc__ = '''
This is a concurrency module

'''

#----------module document----------


#----------module import----------

# import system modules
from threading import Thread
from multiprocessing import Process 
from multiprocessing.dummy import Pool

# import third-party modules
from gevent import monkey; monkey.patch_all()
import gevent
import requests

# import my own modules
from decorator import printTime
from scraperThreadPool import threadPool

#----------module import----------

#----------function definition----------

def testFunc(arg):
    r = requests.get('http://cn.bing.com/?mkt=zh-CN')
 
 
@printTime   
def one(func,args):
    for i in args:
        func(i)
        
     
@printTime        
def mapPool(func,args):
    map(func,args)
    
    
@printTime    
def dummyPool(func,args):
    pool = Pool()
    pool.map(func,args)


@printTime
def threadPool2(func,args):
    t = Thread(target=func,args=(args,)) #wrong
    t.start()
    t.join()
    

@printTime
def processPool(func,args):
    p = Process(target=func,args=(args,)) #wrong
    p.start()
    p.join()


@printTime
def geventPool(func,args):
    gevent.joinall([gevent.spawn(func,arg) for arg in args])
    
#----------function definition----------    
    

#----------main function----------
    
if __name__ == '__main__':
    func = testFunc
    args = range(10)
    one(func, args)
    mapPool(func, args)
    processPool(func, args)
    threadPool2(func, args)
    geventPool(func, args)
    threadPool(func,args)

#----------main function----------

    
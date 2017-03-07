# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__date__ = '2016-5-28'

__moduleVersion__ = '1.2'

__doc__ = '''
This is a multithreading scarper pool.
'''

#----------module document----------


#----------module import----------

import time
import Queue
from threading import Thread

from decorator import printTime

#----------module import----------


#----------class definition----------

class ScraperManager(object):
    'The Manager of the Scraper'
    
    def __init__(self,function,paraGroups,threadNum=100):
        self.workQueue = Queue.Queue()
        self.threads = []
        self.jobNum = len(paraGroups)
        self.__initWorkQueue(function,paraGroups,self.jobNum)
        self.__initThreadPool(threadNum)
        
    def __initThreadPool(self,threadNum):
        for i in range(threadNum):
            self.threads.append(ScraperWorker(self.workQueue))

    def __initWorkQueue(self,function,paraGroups,jobNum):
        for i in range(jobNum):
            self.addJob(function,paraGroups[i])
            
    def addJob(self,func,args):
        self.workQueue.put((func,args))
        
    def checkQueue(self):
        return self.workQueue.qsize()
    
    def waitAllComplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class ScraperWorker(Thread):
    'The Worker of the Scraper'
    
    def __init__(self,workQueue):
        Thread.__init__(self)
        self.workQueue = workQueue
        self.start()
        
    def run(self):
        while True:
            try:
                do,args = self.workQueue.get(block=False)
                do(args)
                self.workQueue.task_done()
            except Queue.Empty:
                break
            except Exception,e:
                print(e)
                break

        
#----------class definition----------
        
        
#----------function definition----------

@printTime
def threadPool(function,paraGroups,n=10):
    threadNum = len(paraGroups)
    if threadNum > n:
        threadNum = n
    workManager = ScraperManager(function,paraGroups,threadNum)
    workManager.waitAllComplete()
    
#----------function definition---------- 


#----------main function----------

if __name__ == '__main__':
    function = print
    paragroups = range(1000)
    threadPool(function,paragroups)


    
#----------main function----------
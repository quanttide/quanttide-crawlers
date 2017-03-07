# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module import----------

# import system modules
import Queue
from threading import Thread
import time

# import my own modules
from mofcomGoodsScraper import categoryScraper
from dataCleaning import cleanString

#----------module import----------


#----------global variables----------

try:
    with open('success_list') as f:
        success_list = f.readlines()
except:
    success_list = []
    
fail_url_lists = []
    
#----------global variables----------


#----------class definition----------

class ScraperManager(object):
    'The Manager of the Scraper'
    
    def __init__(self,function,categories,threadNum=100):
        self.workQueue = Queue.Queue()
        self.threads = []
        self.jobNum = len(categories)
        self.__initWorkQueue(function,categories,self.jobNum)
        self.__initThreadPool(threadNum)
        
    def __initThreadPool(self,threadNum):
        for i in range(threadNum):
            self.threads.append(ScraperWorker(self.workQueue))

    def __initWorkQueue(self,function,categories,jobNum):
        for i in range(jobNum):
            self.addJob(scraperFunc,function,categories[i])
            
    def addJob(self,func,args1,arg2):
        self.workQueue.put((func,args1,arg2))
        
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
                do,args1,arg2 = self.workQueue.get(block=False)
                do(args1,arg2)
                self.workQueue.task_done()
            except Exception,e:
                print(e)
                try:
                    fail_url_lists.append(arg2)
                except Exception,e:
                    print(e) 
                break
        
#----------class definition----------
        
        
#----------function definition----------

def scraperFunc(function,category):
    category = category.decode('utf-8')
    t = category.split(',')
    categoryName = t[0]
    goodsName = t[1]
    goodsURL= t[2]
    fail_url_list = function(categoryName,goodsName,goodsURL)
    success_list.append(category)
    fail_url_lists.extend(fail_url_list)
    
    
def scraper(function,categories,n=10):
    threadNum = len(categories)
    if threadNum > n:
        threadNum = n
    workManager = ScraperManager(function,categories,threadNum)
    workManager.waitAllComplete()
    
#----------function definition---------- 


#----------main function----------

if __name__ == '__main__':
    start = time.time()
    
    function = categoryScraper
    
    with open('mofcomGoodsURL') as f:
        categories = f.readlines()
    scraper(function,categories)
    
    with open('success_list','ab') as f:
        f.writelines(success_list) 
        
    with open('fail_list','ab') as f:
        f.writelines(fail_url_lists)

    end = time.time()
    print('time:',end-start)
    print('Web scraping is over')
    
#----------main function----------
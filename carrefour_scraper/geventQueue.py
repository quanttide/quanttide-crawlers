# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-7-24'

__creation_date__ = '2016-7-24'

__moduleVersion__ = '1.0'

__doc__ = '''
A gevent queue for RT-Mart Scraper.
'''


#----------module document----------


#----------module import----------

# import third-party modules
from gevent import monkey; monkey.patch_all()
import gevent
from gevent.queue import Queue

#----------class definition----------

class ScraperGeventQueue(object):
    '''
    A gevent queue for carrefourScraper.
     Parameters
     ----------
     scraperClass: class
      carrefour page scraper for CPP
     args: list
      a multi-list for CPP
     gevent_num=100: int
      maximum running gevent number.  
    '''
    
    def __init__(self,scraperClass,args,gevent_num=80):
        self.scraperClass = scraperClass
        self.args = self._args(args)
        
        self.gevent_num = gevent_num
        self.tasks = Queue()    # create a gevent queue
        
        self.failure_list = []
        
    def _args(self,args):
        '''
        Parse input args.
         Parameters
         ----------
          category: list or tuple
           a group of input categories
          areas: list or tuple
           a group pf input area information
         Returns
         -------
          new_args: list
           a group of new input args 
        
        '''
        
        new_args = []
        for arg in args:
            category,selectedCategoryId = splitPara(arg)
            new_args.append((category,selectedCategoryId,1))
        return new_args
    
    def _run(self,task):
        '''
        Define the run function.
         Parameters
         ----------
          task: list or tuple
           a group of parameters for self.scraperClass 
        '''
        
        # split parameters for the page scraper class
        category_name,selectedCategoryId,page_num=task
        
        # run the page scraper class
        scraper = self.scraperClass(category_name,selectedCategoryId,page_num)
        scraper.json = scraper.getJSON()
        
        # if connect error, add the parameters into queue once again
        if (not scraper.json) and (task not in self.failure_list):
            self.failure_list.append(task)
            self.tasks.put_nowait(task)
            
        data_list = scraper.parseJSON(scraper.json)
        #indicator = scraper.writeMongoDB(data_list)
        indicator = scraper.writeCSV(data_list)
        
        # produce new parameters and add them to the gevent queue
        if (page_num == 1) and indicator:
            total_page = scraper.getTotalPageNumber()
            if total_page>1:
                [self.tasks.put_nowait((category_name,selectedCategoryId,i)) for i in range(2,total_page+1)]
        
    def worker(self):
        'A gevent worker.'
        
        while not self.tasks.empty():
            task = self.tasks.get()
            self._run(task)

    def manager(self):
        'A gevent manager, creating the initial gevents'
        
        for arg in self.args:
            self.tasks.put_nowait(arg)
            
    def start(self):
        'Run the gevent queue.'
        
        gevent.spawn(self.manager).join()
        tasks = [gevent.spawn(self.worker) for i in range(self.gevent_num)]
        gevent.joinall(tasks)
        
#----------class definition----------    


#----------function definition---------- 

def splitPara(category):
    'Split parameters for carrefour scraper.'
    if (type(category)== list) or (type(category)==tuple):
            categoryName = category[0]
            try:
                if type(category[1]==str):
                    selectedCategoryId = category[1]
                else:
                    selectedCategoryId = ''
            except IndexError:
                selectedCategoryId = ''
    elif (type(category)== unicode or type(category)==str):
        categoryName = category
        selectedCategoryId = ''
    else:
        print('Error: wrong categories list!!'.encode('utf-8'))
        categoryName = ''
        selectedCategoryId = ''
    return categoryName,selectedCategoryId
        
#----------function definition---------- 
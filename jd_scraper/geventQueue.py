# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-24'

__creation_date__ = '2016-6-24'

__moduleVersion__ = '1.1'

__doc__ = '''
A gevent queue for TmallScraper and JDScraper.
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
    A gevent queue for Tmall and JD scraper.
     Parameters
     ----------
     scraperClass: class
      Tmall or JD page scraper for CPP
     args: list
      a multi-list for CPP
     gevent_num=100: int
      maximum running gevent number.  
    '''
    
    def __init__(self,scraperClass,args,gevent_num=100):
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
          args: list or tuple
           a group of input args
         Returns
         -------
          new_args: list
           a group of new input args 
        
        '''
        
        new_args = []
        for arg in args:
            category_name,url_parameters = splitPara(arg)
            new_arg = (category_name,1,url_parameters)
            new_args.append(new_arg)
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
        category_name,page_num,url_parameters=task
        
        # run the page scraper class
        scraper = self.scraperClass(category_name,page_num,**url_parameters)
        scraper.html = scraper.getHTML(scraper.url)
        
        if not scraper.html and (task not in self.failure_list):
            self.tasks.put(task)
            
        data_list= scraper.parseHTML(scraper.html)
        scraper.html2 = scraper.getHTML(scraper.url2)
        data_list_2 = scraper.parseHTML2(scraper.html2,order = 2)
        if data_list_2:
            data_list.extend(data_list_2)
        indicator = scraper.writeCSV(data_list)
        
        # produce new parameters and add them to the gevent queue
        if (page_num == 1) and indicator:
            total_page = scraper.getTotalPageNumber()
            if total_page>1:
                [self.tasks.put((category_name,i,url_parameters)) for i in range(2,total_page+1)]
        
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
    'Split parameters for Tmall and JD scrapers.'
    if type(category)== list:
            categoryName = category[0]
            try:
                if type(category[1]==dict):
                    urlParameters = category[1]
                else:
                    urlParameters = {}
            except IndexError:
                urlParameters = {}
    elif (type(category)== unicode or type(category)==str):
        categoryName = category
        urlParameters = {}
    else:
        print('Error: wrong categories list!!'.encode('utf-8'))
        categoryName = ''
        urlParameters = {}
    return categoryName,urlParameters

#----------function definition----------
            
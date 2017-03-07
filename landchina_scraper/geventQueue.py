# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__last_edit_date__ = '2016-6-28'

__creation_date__ = '2016-6-28'

__moduleVersion__ = '1.0'

__doc__ = '''
A gevent queue for landChina scrpaer
'''


#----------module document----------


#----------module import----------

# import system modules
import codecs
import csv
import os

# import third-party modules
from gevent import monkey; monkey.patch_all()
import gevent
from gevent.queue import Queue

#----------class definition----------

class ScraperGeventQueue(object):
    def __init__(self,scraperClass,gevent_num=100):
        self.scraperClass = scraperClass
        
        self.gevent_num = gevent_num
        self.tasks = Queue()
    
    @property    
    def args(self):
        day_list = [('1989-01-01','1999-12-31',1)]
        for i in range(2000,2017):
            for j in range(1,13):
                begin_day = str(i)+'-'+str(j)+'-01'
                end_day = str(i)+'-'+str(j)+'-'+ str(daysInMonth(i, j)) 
                day_list.append((begin_day,end_day,1))
        return day_list
        
    def _run(self,task):
        begin_day,end_day,page_num = task
        scraper = self.scraperClass(begin_day,end_day,page_num)
        if page_num == 1:
            
            scraper.html = scraper.getHTML()
            totalPage = scraper.getTotalPageNumber()

            if totalPage>200:
                new_end_day,new_begin_day = aveDay(begin_day,end_day)
                task1 = (begin_day,new_end_day,1)
                task2 = (new_begin_day,end_day,1)
                self.tasks.put(task1)
                self.tasks.put(task2)
                writeCSV('overflow_list',*task)
                writeCSV('split_list',*task1)
                writeCSV('split_list',*task2)
            elif totalPage>1:
                writeCSV('total_page_list',*(begin_day,end_day,totalPage))
                [self.tasks.put_nowait((begin_day,end_day,i)) for i in range(2,totalPage+1)]
                map(print,self.tasks) 
            elif totalPage==1:
                writeCSV('total_page_list',*(begin_day,end_day,totalPage))
            else:
                self.tasks.put(task)
                writeCSV('failure_list',*task)
                
            if os.path.isfile(scraper.file_name):
                indicator = True
            else:
                indicator = scraper.parseURL(scraper.html)
        else:
            indicator = scraper.start()
        
        if indicator:
            writeCSV('success_list',*task)
            print(begin_day,end_day,page_num,'success')
        else:
            self.tasks.put(task)
            writeCSV('failure_list',*task)
            
    def worker(self):
        while not self.tasks.empty():
            task = self.tasks.get()
            self._run(task)

    def manager(self):
        for arg in self.args:
            self.tasks.put_nowait(arg)
            
    def start(self):
        gevent.spawn(self.manager).join()
        tasks = [gevent.spawn(self.worker) for i in range(self.gevent_num)]
        gevent.joinall(tasks)
        
#----------class definition----------    


#----------function definition----------

def isLeapYear(year):
    if (year%4==0 and year%100!=0) or (year%400==0):
        return 1
    else:
        return 0
    
    
def daysInMonth(year,month):
    if 1<=month<=12:
        if month in {1,3,5,7,8,10,12}:
            return 31
        elif month in {4,6,9,11}:
            return 30
        elif month == 2:
            return 28+isLeapYear(year)
        

def aveDay(begin_day,end_day):
    year_month = '-'.join(begin_day.split('-')[:-1])
    begin_day_short = int(begin_day.split('-')[-1])
    end_day_short = int(end_day.split('-')[-1])
    new_end_day_short = int((begin_day_short+end_day_short)/2)
    new_begin_day_short = new_end_day_short + 1
    return year_month+'-'+str(new_end_day_short),year_month+'-'+str(new_begin_day_short)


def writeCSV(fileName,*data):
    if data:
        with codecs.open(fileName,'ab',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    
#----------function definition----------
            
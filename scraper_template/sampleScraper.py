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
from bs4 import BeautifulSoup

# import my own modules
from scraperRequest import getHTML
from writeData import createFile,writeCSV
from scraperThreadPool import threadPool

#----------module import----------


#----------global variables----------

# request headers
headers = {}
successList = []    # produce sign list
failureList = []    # produce sign list

#----------global variables----------


#----------class definition----------

class SamplePageScraper(object):
    def __init__(self,keyword):
        self.keyword = keyword
        self.url = self.joinURL(keyword)
        self.dictName = ''
        self.html = getHTML(self.url,headers)
        
    def joinURL(self,keyword):
        pass
    
    def parseHTML(self):
        if self.html == None:
            print(self.keyword,':connect error'.encode('utf-8'))
            return None
        
        try:
            soup = BeautifulSoup(self.html,'html.parser')
            '''
            parse this HTML with BeautifulSoup
            '''
            sourceList = []
        except AttributeError:
            print(self.keyword,':parse error'.encode('utf-8'))
            return None
        
        labels = ''
        fileName = createFile(self.dictName,self.keyword,*labels)
        
        if sourceList:
            for sourceData in sourceList:
                '''
                parse source data and put them into one list
                '''
                data = []    # please put data into this list
                try:
                    writeCSV(fileName,*data)
                except:   # Exception depends on specific situations
                    print(self.keyword,',',sourceList.index(sourceData),'write error')
                    continue
            return True
        
        else:
            print(self.keyword,':parse error'.encode('utf-8'))
            return None
        
#----------class definition----------


#----------function definition----------

def samplePageScraper(keyword):
    try:
        scraper = SamplePageScraper(keyword)
        indicator = scraper.parseHTML()
        if indicator:
            successList.append(keyword)    # successList as global variables
        else:
            failureList.append(keyword)    # failureList as global variables
        return indicator
    except:
        return None
        # failureList.append(keyword)  


def sampleOneThreadScraper():
    
    keywords = []
    for keyword in keywords:    # mutiparas: work with zip function
        samplePageScraper(keyword)
  
        
def threadFunc(func,paraGroup):
    '''
    spilt the parameter group
    '''
    # samplePageScraper(keyword)


def sampleMultiThreadScraper():
    paraGroups = []
    threadPool(threadFunc, paraGroups, n=10)

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    # scraper one page
    ''' 
    Web scrapering
    '''
    '''
    save sign list
    '''
    end = time.time()
    print('time:',end-begin)
    print('Web scraping is over')

#----------main function----------

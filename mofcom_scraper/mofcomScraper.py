# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module import----------

import time

import requests
from bs4 import BeautifulSoup

#----------module import----------


#----------class definition----------

class HomePageScraper(object):
    def __init__(self):
        self.presentDay = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        #self.presentTime = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.logTime = '[{} {}]'.format(self.presentDay,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
        
        self.homePageURL = 'http://nc.mofcom.gov.cn/channel/gxdj/jghq/index.shtml'
        self.html = self.getHTML()
        
    def getHTML(self):
        r = requests.get(self.homePageURL)
        return r.content
    
    def parseHTML(self):
        soup = BeautifulSoup(self.html,'lxml')
        div_pzIndexBox = soup.find('div',attrs ={'class':'pzIndexBox'})
        divs = div_pzIndexBox.find_all('div')
        
        i_s = divs[0].find_all('i')
        iTextList = []
        for i in i_s:
            iTextList.append(i.getText().encode('utf-8')) 
            
        ts = range(1,len(divs))
        for t in ts:
            categoryName = iTextList[t-1]
            a_s = divs[t].find_all('a')
            for a in a_s:
                goodsName = a.get_text().encode('utf-8')
                goodsURL = a['href'].encode('utf-8')
                with open('mofcomGoodsURL','ab') as f:
                    f.write(categoryName)
                    f.write(',')
                    f.write(goodsName)
                    f.write(',')
                    f.write(goodsURL)
                    f.write(',\n')
            
        

#----------class definition----------


#----------function definition----------

def homepageScraper():
    scraper = HomePageScraper()
    scraper.parseHTML()

#----------function definition----------


#----------main function----------
if __name__ == '__main__':
    begin = time.time()
    homepageScraper()
    end = time.time()
    print('time:',end-begin)

#----------main function----------

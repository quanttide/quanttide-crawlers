# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module import----------

import time
import os
import re

import requests
from bs4 import BeautifulSoup

from dataCleaning import cleanString

#----------module import----------

#----------global variables----------

try:
    with open('success_list') as f:
        success_list = f.readlines()
except:
    success_list = []
    
fail_url_lists = []
    

#----------class definition----------

class PageScraper(object):
    def __init__(self,categoryName,goodsName,goodsURL,pageNum = 1):
        self.presentDay = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        #self.presentTime = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.logTime = '[{} {}]'.format(self.presentDay,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
        
        self.categoryName = categoryName
        self.goodsName = goodsName
        self.pageNum = pageNum
        self.homepageURL = 'http://nc.mofcom.gov.cn'
        self.goodsURL_source = goodsURL
        self.goodsURL = ''.join([self.homepageURL,goodsURL,'&page=',str(pageNum)])

        self.html = self.getHTML()
        
        self.fail_url = None
        
        
    def getHTML(self):
        try:
            r = requests.get(self.goodsURL)
        except:
            print(self.logTime,'connect error',self.goodsURL)
            category = ','.join([self.categoryName,self.goodsName,self.goodsURL,str(self.pageNum),'\n'])
            self.fail_url = category.encode('utf-8')
            return None
        return r.content
    
    def getTotalPageNumber(self):
        if self.html == None:
            return None
        
        pattern = re.compile('\d+')
        try:
            soup = BeautifulSoup(self.html,'lxml')  
            page = soup.select('#mainBody > div > div.s_Lmain.clearfix > div.s_cPriceListMain.mt10 > div.pmCon > script')
            match = re.findall(pattern,str(page))
            if match:
                return int(match[0])
            else:
                print(self.logTime,'fail to get total page number',self.goodsURL)
                return None
        except:
            print(self.logTime,'fail to get total page number',self.goodsURL)
            return None
    
    def parsePageHTML(self):
        if self.html == None:
            return None
        
        dictionaryName = self.categoryName +'_'+ self.presentDay
        
        try:
            os.makedirs(dictionaryName)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        fileName = dictionaryName + '/' + self.goodsName
        
        try:
            soup = BeautifulSoup(self.html,'lxml')
            trs = soup.table.tbody.find_all('tr')
            for tr in trs:
                tdList = tr.find_all('td')
                goodsName = tdList[0].getText()
                goodsName = cleanString(goodsName)
                goodsPrice = tdList[1].getText()
                goodsPrice = cleanString(goodsPrice)
                goodsPlace = tdList[2].a.getText()
                goodsPlace = cleanString(goodsPlace)
                goodsDate = tdList[3].getText()
                goodsDate = cleanString(goodsDate)
                data = '{},{},{},{},\n'.format(goodsName,goodsPrice,goodsPlace,goodsDate).encode('utf-8')
                with open(fileName,'ab') as f:
                    f.write(data)
                    
        except Exception:
            print(self.logTime,'parse error',self.goodsURL)
            category = ','.join([self.categoryName,self.goodsName,self.goodsURL,str(self.pageNum),'\n'])
            self.fail_url = category.encode('utf-8')
            return None

                
#----------class definition----------
        
#----------function definition----------

def pageScraper(categoryName,goodsName,goodsURL,pageNum = 1):
    fail_url_list = []
    scraper = PageScraper(categoryName,goodsName,goodsURL)
    scraper.parsePageHTML()
    if scraper.fail_url:
        fail_url_list.append(scraper.fail_url)
    return fail_url_list
        
        
def categoryScraper(categoryName,goodsName,goodsURL):
    fail_url_list = []
    scraper = PageScraper(categoryName,goodsName,goodsURL)
    scraper.parsePageHTML()
    if scraper.fail_url:
        fail_url_list.extend(scraper.fail_url)
    totalPage = scraper.getTotalPageNumber()
    if totalPage:
        total = range(2,totalPage+1)
        for i in total:
            scraper = PageScraper(categoryName,goodsName,goodsURL,pageNum=i)
            scraper.parsePageHTML()
            if scraper.fail_url:
                fail_url_list.extend(scraper.fail_url)
    return fail_url_list

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    #categoryName = '粮油'
    #goodsName = '花生油'
    #goodsURL = '/channel/gxdj/jghq/jg_list.shtml?craft_index=13094&par_craft_index=13073'

        
    with open('mofcomGoodsURL') as f:
        categories = f.readlines()
        
    for category in categories:
        if category.decode('utf-8') in success_list:
            continue
        category = category.decode('utf-8')
        t = category.split(',')
        categoryName = t[0]
        goodsName = t[1]
        goodsURL= t[2]
        fail_url_list = categoryScraper(categoryName,goodsName,goodsURL)
        success_list.append(category.encode('utf-8'))
        fail_url_lists.extend(fail_url_list)
        
    with open('success_list','ab') as f:
        f.writelines(success_list)
        
    with open('fail_list','ab') as f:
        f.writelines(fail_url_lists)
        
    end = time.time()
    print('time:',end-begin)

#----------main function----------


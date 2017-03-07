# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


import time
import csv
import re
import random

import requests
from bs4 import BeautifulSoup

from scraperHeaders import USER_AGENT_LIST,PROXIES


class BaiduNewsScraper(object):
    def __init__(self,keyword):
        self.keyword = keyword
        self.url = ''.join(['http://news.baidu.com/ns?word=',keyword,'&pn=0&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'])
        self.scrapedList = []
        self.fileName = 'newsList_' + re.sub('"','',keyword) + '.txt'
        
    def getHTML(self,url):
        userAgent = random.choice(USER_AGENT_LIST)
        proxies = random.choice(PROXIES)
        headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate,sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'news.baidu.com',
'user-agent':userAgent,
'http':proxies,
    }
        try:
            r = requests.get(url,headers)
            return r.content
        except:
            return None
        
    def parseHTML(self,html):

        if html == None:
            return None

        #try: 
        soup = BeautifulSoup(html,'lxml')
        resultList = soup.find_all('div',attrs={'class':'result'})
        for result in resultList:
            t = result.a
            newsURL = t['href'].encode('utf-8')
            newsTitle = t.get_text().encode('utf-8')
            with open(self.fileName,'ab') as f:
                f.write(newsURL)
                f.write(',')
                f.write(newsTitle)
                f.write(',\n')

        newPageURL = 'http://news.baidu.com' + soup.find('p',attrs={'id':'page'}).find_all('a')[-1]['href']
        t = '&rsv_page=1'
        if t not in newPageURL:
            newPageURL = newPageURL + t
        return newPageURL
        
        #except:
            #return None
            
    def pageScraper(self):

        with open(self.fileName,'ab') as f:
            f.write('newsURL,newsTitle,\n')
            
        html = self.getHTML(self.url)
        newPageURL = self.parseHTML(html)
        print(newPageURL)
        
        
    def keywordScraper(self):
        with open(self.fileName,'wb') as f:
            f.write('newsURL,newsTitle,\n')
        
        print(self.url)
        html = self.getHTML(self.url)
        
        self.scrapedList.append(self.url)
        newPageURL = self.parseHTML(html)
        print(newPageURL)
        
        while newPageURL not in self.scrapedList:
            html = self.getHTML(newPageURL)
            self.scrapedList.append(newPageURL)
            newPageURL = self.parseHTML(html)
            print(newPageURL)
            
            
if __name__ == '__main__':
    keyword = u'短租房'
    scraper = BaiduNewsScraper(keyword)
    #scraper.pageScraper()
    scraper.keywordScraper()

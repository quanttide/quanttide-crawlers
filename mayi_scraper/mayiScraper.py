# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


import time
import csv
import random

import requests
from bs4 import BeautifulSoup

from scraperHeaders import USER_AGENT_LIST,PROXIES


def getHTML(url):
    userAgent = random.choice(USER_AGENT_LIST)
    proxies = random.choice(PROXIES)
    headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'http://www.mayi.com/',
'user-agent':userAgent,
'http':proxies,
    }
    try:
        r = requests.get(url,headers)
        return r.content
    except:
        return None


def parseHTML(html):
    if html == None:
        print('connect error')
        return None
    
    try:    
        soup = BeautifulSoup(html,'html5lib')  #html5lib容错性最好；需要下载html5lib的库
        dl = soup.body.find('dl',attrs = {'class':'a_group','id':'searchRoom'})
        dds = dl.find_all('dd')
    except:
        print('parse error')
        return None
    
    for dd in dds:
        id = dd['id'].encode('utf-8')
        a = dd.find('a',attrs = {'target':'_blank'})
        goodsURL = a['href'].encode('utf-8')
        goodsName = a['title'].encode('utf-8')

        try:
            lis = dd.ul.find_all('li')
        except:
            continue
        
        try:
            score = lis[-4].span.get_text().encode('utf-8')
        except:
            score = None
        try:
            commentNum = lis[-3].get_text().encode('utf-8')
        except:
            commentNum = None
        try:
            houseType = lis[-2].get_text().encode('utf-8')
        except:
            houseType = None
        try:
            peopleNum = lis[-1].get_text().encode('utf-8')
        except:
            peopleNum = None
        #print(id,goodsURL,goodsName,score,commentNum,houseType,peopleNum)
        presentTime = str(time.strftime('%H:%M:%S',time.localtime(time.time())))
        writeData(presentTime,id,goodsURL,goodsName,score,commentNum,houseType,peopleNum)
        
    try:
        #print(dl.find('div',attrs ={'id':'page'}))
        a_ = dl.find('div',attrs={'id':'page'}).find_all('a',attrs = {'class':'up-page'})[-1]
        if a_.get_text()=='>':
            newURL = 'http://www.mayi.com' + a_['href']
            newURL = newURL.split('?')[0]
        else:
            newURL = None
    except:
        newURL = None
    #print(newURL)
    return newURL
        
        
def writeData(*data):
    presentTime = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    fileName = 'mayi_' + presentTime
    with open(fileName,'ab') as f:
        writer = csv.writer(f)
        writer.writerow(data)  
        
        
def mayiScraper():
    url = 'http://www.mayi.com/xiamen/'
    html = getHTML(url)
    url = parseHTML(html)
    while url:
        html = getHTML(url)
        url = parseHTML(html)


if __name__ == '__main__':
    begin = time.time()
    mayiScraper()
    end = time.time()
    print('time:',end-begin)


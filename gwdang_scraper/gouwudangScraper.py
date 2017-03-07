# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__date__ = '2016-5-22'

__moduleVersion__ = '1.1'

__doc__ = '''
This is a scraper for 'www.gwdang.com' 
'''

#----------module document----------


#----------module import----------

# import system module
import time
import codecs
import csv
import random
import os
import re

# import third-party module
import requests

# import my own module
from scraperHeaders import USER_AGENT_LIST,PROXIES

#----------module import----------


#----------class definition----------

class GwdangScraper(object):
    def __init__(self,goodsID):
        self.goodsID = goodsID
        self.parsedID = self.parseID()
        self.url = ''.join(['http://www.gwdang.com/app/price_trend/?&dp_ids=',self.parsedID,'&dp_id=',self.parsedID,'&days=180'])
        self.sourceData = self.getSourceData()
        
    def parseID(self):
        if 'J' in self.goodsID:
            parsedID =''.join([self.goodsID.split('_')[1],'-3'])
        else:
            parsedID = self.goodsID
        return parsedID
        
    def createFile(self):    
        # check or create a daily dictionary
        dictionaryName = 'gwdangData'
        try:
            os.makedirs(dictionaryName)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        # create a file and its name for a certain page
        fileName = ''.join([dictionaryName,'/',self.goodsID])
        
        # write the first line
        with codecs.open(fileName,'wb',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(('dataDay','dataTime','price'))
      
        return fileName
        
    def getSourceData(self):
        userAgent = random.choice(USER_AGENT_LIST)
        proxies = random.choice(PROXIES)
        headers = {
'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
'Accept-Encoding':'gzip,deflate,sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.gwdang.com',
'Referer':''.join(['http://www.gwdang.com/trend/',self.parsedID,'.html?static=true']),
'user-agent':userAgent,
'http':proxies,
'X-Requested-With':'XMLHttpRequest',
    }
        try:
            r = requests.get(self.url,headers)
            return r.content
        except:
            print(self.goodsID.encode('utf-8'),'connect error')
            return None


    def parseData(self):
        if self.sourceData == None:
            return None
        
        
        
        try:
            sourceData = eval(self.sourceData)
            datas = sourceData['store'][0]['data']
        except:
            print(self.goodsID.encode('utf-8'),'parse error')
            return None
        
        fileName = self.createFile()
        
        for data in datas:
            try:
                timeStamp = data[0][0:-3]
                timeArray = time.localtime(eval(timeStamp)-28800)  
                dataDay = str(time.strftime("%Y-%m-%d",timeArray))
                dataTime = str(time.strftime('%H:%M:%S',timeArray))
                # 晚8个小时
            except:
                dataDay = None
                dataTime = None
            try:
                price = data[1]
            except:
                price = None
   
            #print(dataDay,dataTime,price)

            try:
                with codecs.open(fileName,'ab',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([dataDay,dataTime,price])
            except:
                print(self.goodsID.encode('utf-8'),'write error')
                continue
            
        return True

#----------class definition----------
                
                
#----------function definition----------

def gwdangPageScraper(goodsID):
    try:
        scraper = GwdangScraper(goodsID)
        print(scraper.url)
        indicator = scraper.parseData()
        return indicator
    except:
        return None
    
    
def gwdangScraper(fileName):
    with codecs.open(fileName,encoding='utf-8') as f:
        idList = f.readlines()
    try:
        with codecs.open('gwdang_successList',encoding='utf-8') as f:
            successList = f.readlines()
    except IOError:
        successList = []
    
    try:
        with codecs.open('gwdang_failureList',encoding='utf-8') as f:
            failureList = f.readlines()
    except IOError:
        failureList = []
        
    for goodsID in idList:
        if (goodsID in successList) or (goodsID in failureList):
            continue
        goodsID = re.sub('\n','',goodsID)
        indicator = gwdangPageScraper(goodsID)
        if indicator:
            with codecs.open('gwdang_successList','ab',encoding='utf-8') as f:
                f.write(goodsID)
                f.write('\n')
        else:
            with codecs.open('gwdang_failureList','ab',encoding='utf-8') as f:
                f.write(goodsID)
                f.write('\n')
        time.sleep(random.random())
        time.sleep(random.random())
    
#----------function definition----------


#----------main function----------

if __name__=='__main__':
    begin = time.time()
    #gwdangPageScraper('8965959525')
    fileName = 'TmallData_2016-05-20_goodid.txt'
    gwdangScraper(fileName)

    end = time.time()
    print('time:',end-begin)

#----------main function----------
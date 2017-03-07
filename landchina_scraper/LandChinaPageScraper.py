# !/usr/bin/env python
# -*- coding: utf-8 -*-    
from __future__ import print_function,unicode_literals    

import sys
reload(sys)
sys.setdefaultencoding('utf-8')  


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributor__ = 'Xingjian Lin'

__last_edit_date__ = '2016-6-28'

__creation_date__ = '2016-5-31'

__moduleVersion__ = '2.0'

__doc__ = '''
A Page scraper for landchina.com
'''

#----------module document----------


#----------module import----------

# import system modules
import time
import codecs
import random
import csv
import re
import os

# import third-party modules
import requests
from bs4 import BeautifulSoup

# import my own modules
from scraperHeaders import USER_AGENT_LIST,PROXIES

#----------module import----------


#----------class definition----------

class LandChinaPageScraper(object):
    def __init__(self,begin_day,end_day,page_num = 1):
        self.begin_day = str(begin_day)
        self.end_day = str(end_day)
        self.page_num = page_num
        
        self.url = 'http://www.landchina.com/default.aspx?tabid=263'
        
        self.dict_name = os.path.join(os.path.dirname(__file__),'../landChina_URLs')
        self.file_name = self.dict_name + '_'.join(['/landChina_URLs',self.begin_day,self.end_day,str(self.page_num)])
        
    def getHTML(self):
        userAgent = random.choice(USER_AGENT_LIST)
        proxy = random.choice(PROXIES)
        proxy = re.sub('\n','',proxy) 
        headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'3010',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'www.landchina.com',
'Origin':'http://www.landchina.com',
'Referer':'http://www.landchina.com/default.aspx?tabid=263',
'user-agent':userAgent,
'http':proxy,
         }
        post_data = {
'__VIEWSTATE':'/wEPDwUJNjkzNzgyNTU4D2QWAmYPZBYIZg9kFgICAQ9kFgJmDxYCHgdWaXNpYmxlaGQCAQ9kFgICAQ8WAh4Fc3R5bGUFIEJBQ0tHUk9VTkQtQ09MT1I6I2YzZjVmNztDT0xPUjo7ZAICD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHgRUZXh0ZWRkAgEPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFhwFDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6O0JBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3dfc3lfamhnZ18wMDAuZ2lmKTseBmhlaWdodAUBMxYCZg9kFgICAQ9kFgJmDw8WAh8CZWRkAgIPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHwJlZGQCAg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAICD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCAgEPZBYCZg8WBB8BBYYBQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjtCQUNLR1JPVU5ELUlNQUdFOnVybChodHRwOi8vd3d3LmxhbmRjaGluYS5jb20vVXNlci9kZWZhdWx0L1VwbG9hZC9zeXNGcmFtZUltZy94X3Rkc2N3X3p5X2pnZ2dfMDEuZ2lmKTsfAwUCNDYWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIBD2QWAmYPZBYCZg9kFgJmD2QWAgIBD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIDD2QWAgIDDxYEHglpbm5lcmh0bWwFtwY8cCBhbGlnbj0iY2VudGVyIj48c3BhbiBzdHlsZT0iZm9udC1zaXplOiB4LXNtYWxsIj4mbmJzcDs8YnIgLz4NCiZuYnNwOzxhIHRhcmdldD0iX3NlbGYiIGhyZWY9Imh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS8iPjxpbWcgYm9yZGVyPSIwIiBhbHQ9IiIgd2lkdGg9IjI2MCIgaGVpZ2h0PSI2MSIgc3JjPSIvVXNlci9kZWZhdWx0L1VwbG9hZC9mY2svaW1hZ2UvdGRzY3dfbG9nZS5wbmciIC8+PC9hPiZuYnNwOzxiciAvPg0KJm5ic3A7PHNwYW4gc3R5bGU9ImNvbG9yOiAjZmZmZmZmIj5Db3B5cmlnaHQgMjAwOC0yMDE0IERSQ25ldC4gQWxsIFJpZ2h0cyBSZXNlcnZlZCZuYnNwOyZuYnNwOyZuYnNwOyA8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCI+DQp2YXIgX2JkaG1Qcm90b2NvbCA9ICgoImh0dHBzOiIgPT0gZG9jdW1lbnQubG9jYXRpb24ucHJvdG9jb2wpID8gIiBodHRwczovLyIgOiAiIGh0dHA6Ly8iKTsNCmRvY3VtZW50LndyaXRlKHVuZXNjYXBlKCIlM0NzY3JpcHQgc3JjPSciICsgX2JkaG1Qcm90b2NvbCArICJobS5iYWlkdS5jb20vaC5qcyUzRjgzODUzODU5YzcyNDdjNWIwM2I1Mjc4OTQ2MjJkM2ZhJyB0eXBlPSd0ZXh0L2phdmFzY3JpcHQnJTNFJTNDL3NjcmlwdCUzRSIpKTsNCjwvc2NyaXB0PiZuYnNwOzxiciAvPg0K54mI5p2D5omA5pyJJm5ic3A7IOS4reWbveWcn+WcsOW4guWcuue9kTxiciAvPg0K5aSH5qGI5Y+3OiDkuqxJQ1DlpIcwOTA3NDk5MuWPtyDkuqzlhaznvZHlronlpIcxMTAxMDIwMDA2NjYoMikmbmJzcDs8YnIgLz4NCjwvc3Bhbj4mbmJzcDsmbmJzcDsmbmJzcDs8YnIgLz4NCiZuYnNwOzwvc3Bhbj48L3A+HwEFZEJBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3cyMDEzX3l3XzEuanBnKTtkZDgA+MFK90yI4WPW8j/nSzl0gTST519balSd/Kz5oI3l',
'__EVENTVALIDATION':'/wEWAgKS9fGsDwLN3cj/BAfk0tzlLwvnwbuNEg8E+M+jFAriIWay/5KoCTUnfQg0',
'hidComName':'default',
'TAB_QueryConditionItem':'9f2c3acd-0256-4da2-a659-6949c4671a2a',
'TAB_QuerySortItemList:282':'False',
'TAB_QuerySubmitConditionData':'9f2c3acd-0256-4da2-a659-6949c4671a2a:'+str(self.begin_day)+'~'+str(self.end_day), #控制时间
'TAB_QuerySubmitOrderData:282':'False',
'TAB_RowButtonActionControl':'',
'TAB_QuerySubmitPagerData':str(self.page_num), #控制页码
'TAB_QuerySubmitSortData':'',
        }
        try:
            r = requests.post(self.url,post_data,headers)
            return r.content
        except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout),e:
            print(self.begin_day,self.end_day,self.page_num,e)
            return None

    def getTotalPageNumber(self):
        
        try:
            html = self.html 
        except AttributeError:
            html = self.getHTML()    
        
        if html == None:
            return None
        
        try:
            html = html.decode('GB18030')
        except UnicodeDecodeError,e:
            print(self.begin_day,self.end_day,e)
            return None
        try:
            pattern = re.compile(r'共\d+页')
            patternNum = re.compile(r'\d+')
            match = re.search(pattern,html)
            cate = match.group(0)
            totalPage = re.findall(patternNum,cate)[0]
            return int(totalPage)
        except AttributeError,e:
            print(self.begin_day,self.end_day,self.page_num,e)
            return None
        
    
    def parseURL(self,html):
        if html == None:
            return None
        
        try:
            soup = BeautifulSoup(html,'html.parser',from_encoding='gb18030')   
            table = soup.find('table',attrs={'id':'TAB_contentTable'})
            trs =table.tbody.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                url = tds[2].find('a')['href']
                self.writeData(url)
            return True
        except AttributeError,e:
            print(self.begin_day,self.end_day,self.page_num,e)
            return None
     
    def writeData(self,*data):
        
        try:
            os.makedirs(self.dict_name)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        with codecs.open(self.file_name,'ab',encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        
    def start(self):
        if os.path.isfile(self.file_name):
            return True
        else:
            self.html = self.getHTML()
            indicator = self.parseURL(self.html)
            return indicator
    
    '''
    def parseHTML(self,html):
        if html == None:
            return None
        try:
            soup = BeautifulSoup(html,'html.parser',from_encoding='gb18030') #转中文乱码
            table = soup.find('table',attrs={'id':'TAB_contentTable'})
            trs =table.tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                data = []
                for td in tds:
                    data.append(td.get_text())
                    self.writeData(*data)
            return True
        except:
            return None
    '''

#----------class definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    scraper = LandChinaPageScraper('1989-01-01','1999-12-31')
    totalPage = scraper.getTotalPageNumber()
    print(totalPage)
    end = time.time()
    print('time:',end-begin)

#----------main function----------

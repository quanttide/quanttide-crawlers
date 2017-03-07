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

__last_edit_date__ = '2016-7-25'

__creation_date__ = '2016-7-24'

__moduleVersion__ = '1.1'

__doc__ = '''
A page scraper of carrefourScraper for China's Prices Project.
'''

#----------module document----------


#----------module import----------

# import system modules
import os
import csv
import time
import random
import codecs
import urllib
import re
import math

# import third-party modules
import requests
from pymongo import MongoClient

# import my own modules
from proxiesPool.headers import MOBILE_USER_AGENTS,PROXIES

#----------module import----------


#----------class definition----------

class CarrefourPageScraper(object):
    '''
    A page scraper for TmallScraper.
     
     Parameters
     ----------
      category_name: keyword in the search page of RT-Mart.
      page_num: page number of the certain category.
    '''
    
    def __init__(self,category_name,selectedCategoryId,page_num=1):
        
        # time creating an instance, similar to request time
        self.present_day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        self.present_time = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
              
        # scraper variables
        self.category_name = category_name
        self.selectedCategoryId = selectedCategoryId 
        self.page_num = page_num
        
    def joinPostData(self):
        '''
        Join post data
        
         Returns
         -------
          post_data: str
           data for requests.post
        '''
        
        data1 = 'param=%7B%22keyword%22%3A%22'
        keyword = urllib.quote(self.category_name.encode('utf-8')) #'%E9%85%B1%E6%B2%B9'
        data2='%22%2C%22order%22%3A1%2C%22page%22%3A'
        data3='%2C%22pageCount%22%3A12%2C'
        if self.selectedCategoryId:
            data4 = '%22selectedCategoryId%22%3A'+self.selectedCategoryId
        else:
            data4 = ''
        data5='%7D'
        post_data = ''.join([data1,keyword,data2,str(self.page_num),data3,data4,data5])
        print(post_data)
        return post_data
        
    def getJSON(self):
        '''
        Request for a certain page JSON data.
        
         Returns
         -------
          r.json(): dict
            response json data,transformed into Python dict. (None if connect error happens) 
        '''
        
        user_agent = random.choice(MOBILE_USER_AGENTS)
        proxy =re.sub('\n','',random.choice(PROXIES))
        headers = {
'Host': 'www.carrefour.cn',
'Connection': 'keep-alive',
#'Origin': 'file://',
'language': 'zh-CN',
'User-Agent': user_agent,
'http':proxy,
#'osVersion': '4.4',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
'Accept': 'application/json, text/plain, */*',
#'unique': 'android-af204dccbb3669c1',
#'x-wap-profile': 'http://wap1.huawei.com/uaprof/HW_HUAWEI_MT7-CL00_2_20140903.xml',
#'subsiteId': '46',
#'os': 'android',
'appVersion': '1.2.0',
'Accept-Encoding': 'gzip,deflate',
'Accept-Language': 'zh-CN,en-US;q=0.8',
#'Cookie': 'MPLPD1=rd1o00000000000000000000ffff0a97f821o80; DISTRIBUTED_JSESSIONID=05F8432CA95C4071BF6B8E438EFA910E',
'X-Requested-With': 'cn.carrefour.app.mobile'
                   }
        
        url = 'https://www.carrefour.cn/mobile/api/product/search'
        post_data = self.joinPostData()
        r = requests.post(url,data = post_data,verify=False,headers=headers)
        print(r.content)
        return r.json()
    
    def getTotalPageNumber(self):
        '''
        Get total page number for the certain group of category name.
        
         Returns
         -------
          total_page: int
            total page number of the certain group of category name.
            (None if parse error happens.)
        '''
        
        # get JSON data if not requested
        try:
            json = self.json
        except AttributeError:
            json = self.getJSON()
            
        # return None if no right data
        if not json:
            return None
            
        # parse total page number
        try:
            total = json['data']['total']
            total_page = int(math.ceil(int(total)/12.))
            return total_page
        except KeyError:
            return None
    
    def parseJSON(self,json):
        '''
        parse a page JSON for carrefourScraper.
        
         Parameters
         ----------
          json: dict
            JSON to parse.
            
         Returns
         -------
          data_list: list
            a list of data with type "dict"
        ''' 
        if not json:
            return None
        
        try:
            items = json['data']['items']
        except KeyError:
            print('parse error')
            return None
        
        if not items:
            return None
        
        data_list = []
        for i,item in enumerate(items):
            data = {}
            try:
                id = item['id']
            except KeyError:
                id = None
            data['id'] = id
                
            try:
                name = item['name']
            except KeyError:
                name = None
            data['name'] = name
            
            try:
                price = item['flashSale']['price']
            except KeyError:
                price = None
            data['price'] = price
            
            try:
                salesCount = item['salesCount']
            except KeyError:
                salesCount = None
            data['sales'] = salesCount
            
            try:
                reviewCount = item['reviewCount']
            except:
                reviewCount = None
            data['reviews'] = reviewCount
        
            if filter((lambda x:x),data.values()):
                data['category_name'] = str(self.category_name).encode('utf-8')
                data['page_num']=self.page_num
                data['order'] = i+1
                data['present_day'] = self.present_day
                data['present_time'] = self.present_time
                data_list.append(data)
                
        return data_list
        
    def writeCSV(self,data_list):
        '''
        Write the data list into a .csv file
         
         Parameters
         ----------
          data_list: list
             elements with type "dict"
             
         Returns
         -------
          indicator: bool
              success with "True" and failure with "None"
        '''
        
        if not data_list:
            return None
        
        # check or create a daily dictionary
        try:
            file_dict = os.path.join(os.path.dirname(__file__),''.join(['../CarrefourData_',self.present_day]))
        except TypeError:
            file_dict = ''.join(['../CarrefourData_',self.present_day])
        try:
            os.makedirs(file_dict)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        # create a file and its name for a certain page
        file_name = ''.join([file_dict,'/','carrefourPrice','_',self.present_day,'_',self.present_time,'_',self.category_name,'_',str(self.page_num)])
        
        with codecs.open(file_name,'wb') as f:
            fieldnames = ['id','name','price','sales','reviews']
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list:
                data = {key:value for key,value in data.items() if key in fieldnames}
                writer.writerow(data)

        return True
    
    def writeMongoDB(self,data_list):
        '''
        Write data list into MongoDB
        
        Parameters
        ----------
         data_list: list
          elements with type "dict"
        
        Returns
        -------
         indicator: bool
          success with "True" and failure with "None"
        '''
        
        if data_list==None:
            return None
            
        # create a client
        client = MongoClient('localhost',27017)    # local database

        # create a database
        try:
            db = client.cppdata
        except AttributeError:
            db = client['cppdata']
            
        # login in the database
        #db.authenticate('username','password')
            
        # create a collection
        try:
            collection = db.carrefourdata
        except AttributeError:
            collection = db['carrefourdata']
        
        # insert data list into the collection
        result = collection.insert_many(data_list)
        
        if result:
            return True
        else:
            return None

    def start(self):
        'start the page scraper'
        
        self.json = self.getJSON()
        data_list = self.parseJSON(self.json)
        indicator = self.writeCSV(data_list)
        #indicator = self.writeMongoDB(data_list)

        return indicator

        
#----------class definition----------


#----------main function----------

if __name__ == '__main__':
    category_name = '酱油'
    selectedCategoryId = '250021223'
    page_num = 1
    scraper = CarrefourPageScraper(category_name,selectedCategoryId,page_num)
    scraper.start()
    
#----------main function----------

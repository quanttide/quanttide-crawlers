# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals

# modify system default encoding
# with two statements of modifying, most of the encoding problems will be avoided
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  


#----------module document----------

__author__ = 'Chen Qian,Guo Zhang'

__last_edit_date__ = '2016-7-23'

__creation_date__ = '2016-6-16'

__moduleVersion__ = '2.1'

__doc__ = '''
A page scraper for RT-Mart Scraper.
'''

#----------module document----------


#----------module import----------

# import system module
import os
import csv
import time
import random
import codecs
import urllib
import re

# import third-party module
import requests
from pymongo import MongoClient

# import my own module
from proxiesPool.headers import MOBILE_USER_AGENTS,PROXIES

#----------module import----------


#----------class definition----------

class RTMartPageScraper(object):
    '''
    A page scraper for TmallScraper.
     
     Parameters
     ----------
      category_name: keyword in the search page of RT-Mart.
      area_info: area information for the APP.
      page_num: page number of the certain category.
    '''
    
    def __init__(self,category_name,area_info,page_num = 1):
        
        # time creating an instance, similar to request time
        self.present_day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        self.present_time = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
              
        # scraper variables
        self.category_name = category_name
        self.area_info = area_info
        self.page_num = page_num
        
    def joinPostData(self):
        '''
        Join post data
         Returns
         -------
          post_data: str
           data for requests.post
        '''
                        
        data1 ='''data=%7B%22isCategory%22%3A0%2C%22appVersion%22%3A%222.1.5%22%2C%22areaCode%22%3A%22'''
        # areaCode
        data2 = '''%22%2C%22device_id%22%3A%223384af124d5dac5b57a2a64ea31349d56c8ca578%22%2C%22view_size%22%3A%221242x2208%22%2C%22token%22%3A%22e5051fe619b8495fb0d3846c3df7d3f5%22%2C%22body%22%3A%7B%22areaCode%22%3A%22'''
        # areaCode
        data3 = '''%22%2C%22search_price%22%3A%7B%7D%2C%22sortOrder%22%3A2%2C%22onePageSize%22%3A10%2C%22is_attribute%22%3A0%2C%22keywords%22%3A%22'''
        # keywords
        data4 = '''%0d%0a%22%2C%22sortType%22%3A4%2C%22terms%22%3A%7B%7D%2C%22pageIndex%22%3A'''    #'sortType%22%3A4%2C%22' control sort method
        # page number
        data5 = '''%7D%2C%22apiVersion%22%3A%22ir5.04%22%7D'''
        
        keyword = urllib.quote(self.category_name.encode('utf-8'))
        areaCode = urllib.quote(self.area_info[1].encode('utf-8'))
        post_data = ''.join([data1,areaCode,data2,areaCode,data3,keyword,data4,str(self.page_num),data5])
        
        '''
        data={
          "isCategory":0,
          "appVersion":"2.1.5",
          "areaCode":"CS000016-0-0-0",
          "device_id":"3384af124d5dac5b57a2a64ea31349d56c8ca578",
          "view_size":"1242x2208",
          "token":"e5051fe619b8495fb0d3846c3df7d3f5",
          "body":
            {"areaCode":"CS000016-0-0-0",
             "search_price":{},
             "sortOrder":1,
             "onePageSize":10,
             "is_attribute":0,
             "keywords":"酱油",
             "sortType":1,
             "terms":{},
             "pageIndex":1
             },
          "apiVersion":"ir5.04"
          }
        '''
        
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
                'Host': 'www-fnapp.feiniu.com',
                'Content - Type': 'application/x-www-form-urlencoded',    # important with the blank
                'Connection': 'keep-alive',
                'user-agent': user_agent,
                'http': proxy,
                   }
  
        url ='http://www-fnapp.feiniu.com/merchandise/GetSMbyKey/ir504'
        post_data = self.joinPostData()

        try:        
            self.present_day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            self.present_time = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
            r = requests.post(url,data = post_data,headers = headers)
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),e:
            self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
            print('%s,%s,%s,%s,connect error,%s'%(self.log_time,self.category_name.encode('utf-8'),self.area_info[0].encode('utf-8'),str(self.page_num),e))
            return None
        
    def getTotalPageNumber(self):
        '''
        Get total page number for the certain group of category name.
        
         Returns
         -------
          int(total_page): int
            total page number of the certain group of category name.
            (None if parse error happens.)
        '''
        
        # get JSON data if not requested
        try:
            json = self.json
        except AttributeError:
            json = self.getJSON()
            
        # return None if no right data
        
        if json==None:
            return None
            
        # parse total page number
        try:
            total_page = json['body']['totalPageCount']
            return int(total_page)
        except KeyError:
            return None
        
    def parseJSON(self,json):
        '''
        parse a page JSON for RTMartScraper.
        
         Parameters
         ----------
          json: dict
            JSON to parse.
            
         Returns
         -------
          data_list: list
            a list of data with type "dict"
        '''
    
        if json==None:
            return None

        #parses JSON data
        try:
            merchandiseList = json['body']['MerchandiseList']
        except KeyError:
            print('%s,%s,%s,%s,parse error'%(self.log_time,self.category_name.encode('utf-8'),self.area_info[0].encode('utf-8'),str(self.page_num)))
            return None
        
        if not merchandiseList:
            print('%s,%s,%s,%s,parse error'%(self.log_time,self.category_name.encode('utf-8'),self.area_info[0].encode('utf-8'),str(self.page_num)))
            return None

        data_list = []
        for i,merchandise in enumerate(merchandiseList):
            data = {}
            try:
                sm_seq = merchandise['sm_seq'].encode('utf-8')  # goodsID
            except KeyError:
                sm_seq = None
            data['sm_seq'] = sm_seq
                
            try:
                sm_name = merchandise['sm_name'].encode('utf-8')    # goodsname
            except KeyError:
                sm_name = None
            data['sm_name'] = sm_name

            try:
                sm_price = merchandise['sm_price']    # price
            except KeyError:
                sm_price = None
            data['sm_price'] = sm_price
                
            try:
                saleqty = merchandise['saleqty']    # sale quantity
            except KeyError:
                saleqty = None
            data['saleqty'] = saleqty

            try:
                goodRate = merchandise['goodRate'].encode('utf-8') # good rate
            except KeyError:
                goodRate = None
            data['goodRate'] = goodRate
                
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
        
        if data_list==None:
            return None
        
        # check or create a daily dictionary
        try:
            file_dict = os.path.join(os.path.dirname(__file__),''.join(['../RTMartData_',self.present_day]))
        except TypeError:
            file_dict = ''.join(['../RTMartData_',self.present_day])
        try:
            os.makedirs(file_dict)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        # create a file and its name for a certain page
        file_name = ''.join([file_dict,'/','rtmartPrice','_',self.present_day,'_',self.present_time,'_',self.category_name,'_',self.area_info[0],'_',str(self.page_num)])
        
        with codecs.open(file_name,'wb') as f:
            fieldnames = ['sm_seq','sm_name','sm_price','saleqty','goodRate']
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
            collection = db.rtmartdata
        except AttributeError:
            collection = db['rtmartdata']
        
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

if  __name__ == '__main__':
    begin = time.time()
    category_name = '酱油'
    area_info = ('北京','CS000023-0-0-0')
    scraper = RTMartPageScraper(category_name,area_info)
    scraper.start()
    print(scraper.json)
    #scraper.json = scraper.getJSON()
    #data_list = scraper.parseJSON(scraper.json)
    #print(scraper.getTotalPageNumber())
    end = time.time()
    print('time:',(end-begin))

#----------main function----------


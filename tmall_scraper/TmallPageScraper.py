# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals

# modify system default encoding
# with two statements of modifying, most of the encoding problems will be avoided
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = 'Lin Chen'

__last_edit_date__ = '2016-7-3'

__creation_date__ = '2016-6-26'

__moduleVersion__ = '1.4'

__doc__ = '''
A page scraper for TmallScraper.
'''

#----------module document----------


#----------module import----------

# import system module
import os
import codecs
import csv
import time
import random 
import re

# import third-party module
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# import my own module
from proxiesPool.headers import USER_AGENTS,PROXIES
from dataCleaning import dealSales

#----------module import----------


#----------class definition----------

class TmallPageScraper(object):
    '''
    A page scraper for TmallScraper.
     
     Parameters
     ----------
      categoryName: keyword in the search page of Tmall.
      pageNum: page number of the certain category with certain URL parameters.
      urlParameters: parameters for joining the URL.
    '''
    def __init__(self,category_name,page_num=1, **url_paras):
                
        # time creating an instance, similar to request time
        self.present_day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        self.present_time = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
        
        # scraper variables
        self.category_name = category_name
        self.paras = self.joinParas(**url_paras)
        self.page_num = page_num
        self.url = self.joinURL(category_name,self.paras,(page_num-1)*60)

    def joinParas(self,**url_paras):
        'Join parameters for the request URL'
        
        if not url_paras:
            return None

        paras = ''
        url_paras = url_paras.items()
        for para in url_paras:
            new_para = ''.join([para[0],'=',str(para[1])])
            paras = '&'.join([paras,new_para])
        return paras
    
    def joinURL(self,category_name,paras,s): 
        'join request URL'  
        
        url = u'http://list.tmall.com/search_product.htm?'
        query = ''.join([u'&s=',str(s),u'&q=',category_name,u'&sort=d']) 
        if paras:
            pageURL = ''.join([url,query,paras])
        else:
            pageURL = ''.join([url,query])
        return pageURL
        
    def getHTML(self,url):
        '''
        Request for a certain page HTML.
        
         Parameters
         ----------
          url: str
            request URL.
         
         Returns
         -------
          html: str
            response HTML. (None if connect error happens) 
        '''
        
        # request headers
        user_agent = random.choice(USER_AGENTS)
        proxy = re.sub('\n','',random.choice(PROXIES))
        headers = {
            ':host':'list.tmall.com',
            ':method':'GET',
            ':path':url,
            ':scheme':'https',
            ':version':'HTTP/1.1',
            'accept':'text/html',
            'accept-encoding':'gzip,deflate',
            'accept-language':'zh-CN,zh;q=0.8',
            'cache-control':'max-age=0',
            'referer':'https://list.tmall.com',
            'user-agent':user_agent,
            'http':proxy,
            }
        
        # request for the HTML
        try:
            self.present_day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            self.present_time = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
            r = requests.get(url,headers)
            return r.content
        except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout),e:
            self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
            print(self.log_time,url.encode('utf-8'),',connect error,',e)
            return None
        
    def getTotalPageNumber(self):
        '''
        Get total page number for the certain group of category name and parameters.
        
         Returns
         -------
          total_page: int
            total page number of the certain group of category name and parameters.
            (None if parse error happens.)
        '''
        
        # get the HTML if not requested
        try:
            html = self.html
        except AttributeError:
            html = self.getHTML(self.url)
        
        # return None if no HTML.
        if self.html == None:
            return None
        
        # parse HTML to get total page number.
        try:
            soup = BeautifulSoup(html,'html.parser')
            div_page = soup.body.find('div',attrs={'class','page'})
            div_content = div_page.find('div',attrs={'id':'content'})
            div_filter = div_content.find('div',attrs={'class':'filter clearfix'})
            p_ui = div_filter.find('p',attrs={'class':'ui-page-s'})
            total_page = p_ui.find('b',attrs={'class':'ui-page-s-len'}).getText().split('/')[1]
            return int(total_page)                                  
        except (AttributeError,TypeError),e:
            self.log_time = '[{} {}]'.format(self.present_day,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
            print(self.log_time,(self.url).encode('utf-8'),'fail to get page number',e)
            return None
    
    def parseHTML(self,html):
        '''
        parse a page HTML for TmallScraper.
        
         Parameters
         ----------
          html: str
            HTML to parse.
            
         Returns
         -------
          data_list: list
            a list of data with type "dict"
        '''
        
        # return None if no HTML.
        if self.html == None:
            return None
        
        # parse the HTML
        try:
            soup = BeautifulSoup(self.html,'html.parser')
            div_content = soup.body.find('div',attrs={'class':'page'}).find('div',attrs={'class':'content'})
            products = soup.find_all('div',attrs={'class':'product-iWrap'})
            
        except AttributeError,e:
            print(self.log_time,self.url.encode('utf-8'),'parse error',e)
            return None
        
        if not products:
            print(self.log_time,self.url.encode('utf-8'),'parse error','"products" is None')
            return None
        
        # parse the data
        data_list = []
        for goods_order,product in enumerate(products):
            data = {}
            try:
                goodsID = product.find('p',attrs = {'class':'productStatus'}).find_all('span')[-1]['data-item'].encode('utf-8')
            except (AttributeError,IndexError):
                goodsID = None
            data['goodsID'] = goodsID
                
            try:
                goodsURL = product.find('div',attrs={'class':'productImg-wrap'}).find('a')['href']
                goodsURL =''.join(['http:',goodsURL]).encode('utf-8')
            except (AttributeError,IndexError):
                goodsURL = None
            data['goodsURL'] = goodsURL
            
            try:
                goods_name = product.find('p',attrs={'class':'productTitle'}).find('a')['title'].encode('utf-8')
            except (AttributeError,IndexError):
                try:
                    a = product.find('div',attrs={'class':'productTitle productTitle-spu'}).find_all('a')
                    text = ''.join([i.getText() for i in a])
                    text = re.sub(' ','',text)
                    text = re.sub('\n','',text)
                    text = re.sub('\r','',text)
                    goods_name = text.encode('utf-8')
                except (AttributeError,IndexError):
                    goods_name = None
            except:
                goods_name = None
            data['goodsName'] = goods_name
            
            try:
                shopURL = product.find('div',attrs={'class':'productShop'}).find('a')['href']
                shopURL = ''.join(['http:',shopURL]).encode('utf-8')
            except (AttributeError,IndexError):
                shopURL = None
            data['shopURL'] = shopURL
                
            try:
                text = product.find('div',attrs={'class':'productShop'}).find('a').getText()
                text = re.sub('\n','',text)
                text = re.sub('\r','',text)
                shop_name = text.encode('utf-8')
            except (AttributeError,IndexError):
                shop_name = None
            data['shopName']=shop_name
 
            try:
                price = product.find('p',attrs={'class':'productPrice'}).em['title'].encode('utf-8')
            except (AttributeError,IndexError):
                price = None
            data['price']=price
               
            try:
                price_ave = product.find('span',attrs={'class':'productPrice-ave'}).getText().encode('utf-8')
            except (AttributeError,IndexError):
                price_ave = None
            data['price_ave']= price_ave
                
            try:
                monthly_sales = product.find('p',attrs={'class':'productStatus'}).em.getText()
                monthly_sales = str(dealSales(monthly_sales)).encode('utf-8')
            except (AttributeError,IndexError):
                monthly_sales = None
            data['monthly_sales']= monthly_sales
                
            try:
                comments = product.find('p',attrs={'class':'productStatus'}).a.getText()
                comments = str(dealSales(comments)).encode('utf-8')
            except (AttributeError,IndexError):
                comments = None
            data['comments']=comments
            
            # return non-empty data
            if filter((lambda x:x),data.values()):
                data['category_name'] = str(self.category_name).encode('utf-8')
                data['paras']=str(self.paras).encode('utf-8')
                data['page_num']=self.page_num
                data['order'] = goods_order+1
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
            file_dict = os.path.join(os.path.dirname(__file__),''.join(['../TmallData_',self.present_day]))
        except TypeError:
            file_dict = ''.join(['../TmallData_',self.present_day])
        try:
            os.makedirs(file_dict)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        # create a file and its name for a certain page
        if self.paras:
            file_name = ''.join([file_dict,'/','tmallPrice','_',self.present_day,'_',self.present_time,'_',self.category_name,'_',self.paras,'_',str(self.page_num)])
        else:
            file_name = ''.join([file_dict,'/','tmallPrice','_',self.present_day,'_',self.present_time,'_',self.category_name,'_',str(self.page_num)])
        
        with codecs.open(file_name,'wb') as f:
            fieldnames = ['goodsID','goodsName','goodsURL','shopName','shopURL','monthly_sales','price','price_ave','comments',]
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list:
                data = {key:value for key,value in data.items() if key in fieldnames}
                writer.writerow(data)
        
        # return indicator
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
            collection = db.tmalldata
        except AttributeError:
            collection = db['tmalldata']
        
        # insert data list into the collection
        result = collection.insert_many(data_list)
        
        if result:
            return True
        else:
            return None

    def start(self):
        'start the page scraper'
        
        self.html = self.getHTML(self.url)
        data_list = self.parseHTML(self.html)
        indicator = self.writeCSV(data_list)
        #indicator = self.writeMongoDB(data_list)

        return indicator
    
#----------class definition----------


#----------main function----------
    
if __name__ == '__main__':
    
    begin = time.time()
    
    categoryName,urlParameter = u'酱油',{'cat': u'50099300'}  # u'%BD%B4%D3%CD'
    #categoryName,urlParameter = u'笔记本电脑',{'cat':'50024399'}

    scraper = TmallPageScraper(categoryName,page_num = 1, **urlParameter)
    #print(scraper.url)
    indicator = scraper.start()
    print(indicator)

    end = time.time()
    print('time:',end-begin)
    
#----------main function----------
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

__author__ = 'Guo Zhang,Lin Chen'

__contributors__ = ''

__last_edit_date__ = '2016-7-3'

__creation_date__ = '2016-6-28'

__moduleVersion__ = '1.2'

__doc__ = '''
A page scraper for JDScraper.
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
import math

# import third-party module
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# import my own module
from proxiesPool.headers import USER_AGENTS,PROXIES

#----------module import----------


#----------class definition----------

class JDPageScraper(object):
    '''
    A page scraper for JDScraper.
     
     Parameters
     ----------
      categoryName: keyword in the search page of Tmall.
      pageNum: page number of the certain category with certain URL parameters.
      urlParameters: parameters for joining the URL.
    '''

    def __init__(self,category_name,page_num = 1,**url_paras):
        self.present_day = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        self.present_time = str(time.strftime('%H-%M-%S', time.localtime(time.time())))
        self.log_time = '[{} {}]'.format(self.present_day, str(time.strftime('%H:%M:%S', time.localtime(time.time()))))

        self.category_name = category_name
        self.paras = self.joinParas(**url_paras)
        self.page_num = page_num
        
        self.url = self.joinURL1(category_name, self.paras,page_num)
        self.url2 = self.joinURL2(category_name, self.paras,page_num)

    def joinParas(self,**url_paras):
        'Join parameters for the request URL'
        
        if not url_paras:
            return None

        paras = ''
        url_paras = url_paras.items()
        for para in url_paras:
            new_para = ''.join([para[0], '=', str(para[1])])
            paras = '&'.join([paras, new_para])
        return paras

    def joinURL1(self,category_name,paras,page_num):
        'join the first request URL'

        page = str(page_num * 2 - 1)
        s = str((page_num - 1) * 60 + 1)

        urlFirst = u'http://search.jd.com/search?enc=utf-8&psort=3'
        query = ''.join([u'&page=', page, u'&s=', s, u'&keyword=', category_name])
        if paras:
            url1 = ''.join([urlFirst,query,paras])
        else:
            url1 = ''.join([urlFirst,query])
        return url1
 
    def joinURL2(self,category_name,paras,page_num):
        'join the second request URL'

        page = str(page_num * 2)
        s = str(page_num * 60 - 29)

        urlFirst = u'http://search.jd.com/s_new.php?enc=utf-8&psort=3&scrolling=y'
        query = ''.join([u'&page=', page, u'&s=', s, u'&keyword=', category_name])
        if paras:
            url2 = ''.join([urlFirst, query, paras])
        else:
            url2 = ''.join([urlFirst, query])
        return url2

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
        proxy = re.sub('\n', '', random.choice(PROXIES))
        headers = {
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'search.jd.com',
            'Referer': 'http://www.jd.com/',
            'user-agent': user_agent,
            'http': proxy,
        }

        # request for the HTML
        try:
            r = requests.get(url,headers)
            return r.content
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print(self.log_time,url.encode('utf-8'),',connect error,',e)
            return None
        
    def getPrice(self,goodsID):
        if goodsID == None:
            return None
        
        # request head
        user_agent = random.choice(USER_AGENTS)
        proxy = random.choice(PROXIES)
        headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'p.3.cn',
    'Referer':'http://search.jd.com/',
    'user-agent':user_agent,
    'http':proxy,
        }
        
        # request for price data
        try:
            url = ''.join(['http://p.3.cn/prices/mgets?&skuIds=',goodsID])
            r = requests.get(url,headers)
            json_data = r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            return None
        
        # parse price data
        try:
            price = json_data[0]['p']
            return price
        except IndexError,KeyError:
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
        if html == None:
            return None
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            div_J_searchWrap = soup.body.find('div', attrs={'id': 'J_searchWrap'})
            div_m_list = div_J_searchWrap.find('div', attrs={'class': 'm-list'})
            div_ml_wrap = div_m_list.find('div', attrs={'class': 'ml-wrap'})
            div_J_filter = div_ml_wrap.find('div', attrs={'id': 'J_filter'})
            div_f_line_top = div_J_filter.find('div', attrs={'class': 'f-line top'})
            div_J_topPage = div_f_line_top.find('div', attrs={'id': 'J_topPage'})
            totalPage = div_J_topPage.span.i.getText()
            return int(math.ceil(float(totalPage)/2.))
        except (AttributeError,TypeError),e:
            print(self.log_time,(self.url).encode('utf-8'),'fail to get page number',e)
            return None
        
    def parseHTML(self,html):
        'Parse the HTML'
    
        if html == None:
            return None
    
        # parse the HTML
        try:
            soup = BeautifulSoup(html,'html.parser')
            div_J_searchWrap = soup.body.find('div',attrs={'id':'J_searchWrap'})
            div_m_list = div_J_searchWrap.find('div',attrs={'class':'m-list'})
            div_ml_wrap = div_m_list.find('div',attrs={'class':'ml-wrap'})
            div_J_goodsList = div_ml_wrap.find('div',attrs={'id':'J_goodsList'})
            ul = div_J_goodsList.ul
        except AttributeError,e:
            print(self.log_time,self.url.encode('utf-8'),'parse error',e)
            return None  
        
        data_list = self.parseHTML2(ul)
        return data_list
    
    def parseHTML2(self,ul,order = 1):
        'Parse all the data from HTML'
        
        if ul == None:
            return None
            
        try:
            ul = BeautifulSoup(ul,'html.parser')
        except:
            pass 
                
        # parse the data
        products = ul.find_all('li')
        if not products:
            print(self.log_time,self.url.encode('utf-8'),'parse error','"products" is None')
            return None
        
        data_list = []
        for i,product in enumerate(products):
            goods_order ='-'.join([str(order),str(i+1)])
            try:
                items = product.find_all('div',attrs={'class':'tab-content-item'})
            except AttributeError:
                items = None
                
            if items:
                for item in items:
                    data = self.parseItem(item,goods_order)
                    if data:
                        data_list.append(data)
            else:
                data = self.parseItem(product,goods_order)
                if data:
                    data_list.append(data)
                    
        return data_list
     
    def parseItem(self,product,goods_order):
        'parse one group of data from HTML'
        
        data = {}
        try:
            goodsURL = product.find('div',attrs={'class':'p-name p-name-type-2'}).a['href']
            goodsURL = ''.join(['http:',goodsURL]).encode('utf-8')
        except:
            goodsURL = None
        data['goodsURL'] = goodsURL
                
        try:
            goodsName = product.find('div',attrs={'class':'p-name p-name-type-2'}).a.em.get_text().encode('utf-8')
        except:
            goodsName = None
        data['goodsName']=goodsName
        
        try:
            id = product.find('div',attrs={'class':'p-price'}).strong['class'][0].encode('utf-8')
        except:
            id = None
        data['ID']=id
            
        try:
            price = product.find('div',attrs={'class':'p-price'}).i.get_text().encode('utf-8')
            addedPrice = None    # it is normal
            if not price:
                price = self.getPrice(id).encode('utf-8')
                addedPrice = '1'    # it is a binding goods of last goods
        except:
            price = None
            addedPrice = '0'  # no price information
        data['price']=price
        data['addedPrice']=addedPrice
            
        try:
            commentsNum = product.find('div',attrs={'class':'p-commit'}).strong.a.get_text().encode('utf-8')
        except:
            commentsNum = None
        data['commentsNum']=commentsNum
            
        if filter((lambda x:x),data.values()):
            data['category_name'] = str(self.category_name).encode('utf-8')
            data['paras']=str(self.paras).encode('utf-8')
            data['page_num']=self.page_num
            data['order'] = goods_order
            data['present_day'] = self.present_day
            data['present_time'] = self.present_time
            return data
        else:
            print(self.log_time,self.url.encode('utf-8'),'parse error','data is None')
            return None

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

        if data_list == None:
            return None
        
        # check or create a daily dictionary
        try:
            file_dict = os.path.join(os.path.dirname(__file__), ''.join(['../JDData_', self.present_day]))
        except TypeError:
            file_dict = ''.join(['../JDData_', self.present_day])
        try:
            os.makedirs(file_dict)
        except OSError, e:
            if e.errno != 17:
                raise (e)
            
        # create a file and its name for a certain page
        if self.paras:
            file_name = ''.join([file_dict, '/', 'jdPrice', '_', self.present_day, '_', self.present_time, '_', self.category_name, '_', self.paras, '_', str(self.page_num)])
        else:
            file_name = ''.join([file_dict, '/', 'jdPrice', '_', self.present_day, '_', self.present_time, '_', self.category_name, '_', str(self.page_num)])

        with codecs.open(file_name,'wb') as f:
            fieldnames = ['goodsURL','goodsName','ID','price','commentsNum','addedPrice']
            writer = csv.DictWriter(f,fieldnames= fieldnames)
            writer.writeheader()
            for data in data_list:
                data = {key: value for key, value in data.items() if key in fieldnames}
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
        client = MongoClient()
        
        # create a database
        try:
            db = client.cppdata
        except AttributeError:
            db = client['cppdata']
            
        # create a collection
        try:
            collection = db.jddata
        except AttributeError:
            collection = db['jddata']
        
        # insert data list into the collection
        result = collection.insert_many(data_list)
        
        if result:
            return True
        else:
            return None

    def start(self):
        'start the scraper'
        
        self.html = self.getHTML(self.url)
        data_list = self.parseHTML(self.html)
        self.html2 = self.getHTML(self.url2)
        data_list_2 = self.parseHTML2(self.html2,order = 2)
        if data_list_2:
            data_list.extend(data_list_2)
        indicator = self.writeCSV(data_list)
        # indicator = self.writeMongoDB(data_list)
        return indicator
    
#----------class definition----------


#----------main function----------

if __name__ == '__main__':
    begin=time.time()
    categoryName = u'酱油'
    urlParameter = {'cid2': '1584', 'cid3': '2677', 'ev': ''}
    scraper = JDPageScraper(categoryName, pageNum=1, **urlParameter)
    print(scraper.url)
    indicator = scraper.start()
    totalPage = scraper.getTotalPageNumber()
    print(indicator,totalPage)
    end = time.time()
    print('time:', end - begin)

#----------main function----------

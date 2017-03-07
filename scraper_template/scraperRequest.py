# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__date__ = '2016-5-29'

__moduleVersion__ = '1.0'

__doc__ = '''
A request module for web scraping programs.
Write with 'requests' module.
'''


#----------module document----------


#----------module import----------

# import system modules
import time
import random
import re

# import third-party modules
import requests

# import my own modules
from scraperHeaders import USER_AGENT_LIST,PROXIES

#----------module import----------


#----------function definition----------

def getHTML(url,headers = {}):
    userAgent = random.choice(USER_AGENT_LIST)
    proxies = random.choice(PROXIES)
    proxies = re.sub('\n','',proxies)
    headers['user-agent'] = userAgent
    headers['http'] = proxies
    try:
        r = requests.get(url,headers)
        return r.content
    except:
        return None
    
    
def getJSON(url,headers = {}):
    userAgent = random.choice(USER_AGENT_LIST)
    proxies = random.choice(PROXIES)
    proxies = re.sub('\n','',proxies)
    headers['user-agent'] = userAgent
    headers['http'] = proxies
    try:
        r = requests.get(url,headers)
        return r.json()
    except:
        return None


def getStr(url,headers = {}):
    userAgent = random.choice(USER_AGENT_LIST)
    proxies = random.choice(PROXIES)
    proxies = re.sub('\n','',proxies)
    headers['user-agent'] = userAgent
    headers['http'] = proxies
    try:
        r = requests.get(url,headers)
        return eval(r.content)
    except:
        return None


def getWebpage(url,headers = {},text = 'html'):
    userAgent = random.choice(USER_AGENT_LIST)
    proxies = random.choice(PROXIES)
    proxies = re.sub('\n','',proxies)
    headers['user-agent'] = userAgent
    headers['http'] = proxies
    try:
        r = requests.get(url,headers)
        if text == 'html':
            return r.content
        elif text == 'json':
            return r.json()
        elif text == 'str':
            return eval(r.content)
    except:
        return None

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    result = getWebpage('http://www.baidu.com')
    print(type(result))
    end = time.time()
    print('time:',end-begin)

#----------main function----------

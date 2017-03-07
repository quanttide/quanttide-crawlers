# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module document----------

__pyVersion__ = '2.7.9' #3.x

__author__ = 'Guo Zhang'

__date__ = '2016-3-26'

__moduleVersion__ = '1.2'

__doc__ = '''
This is a scarper header,
including user-agent,cookie and proxies pool.
'''

#----------module document----------


#----------module import----------

import codecs
#import cookielib
#import Cookie

#----------module import----------

#----------global variables----------

USER_AGENT_LIST = [
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'

'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                   
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',                   
                   
                   ]

try:
    PROXIES = codecs.open('ipProxiesList').readlines()
except IOError:
    PROXIES = codecs.open('proxiesList').readlines()
    
#COOKIE_SOURCE = 'cna=EevTDC8iykYCAXgk+TG2P1xu; lzstat_uv=35458846823960025326|2674749; sm4=350200; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=cf0cf648bf48c08b2cbdd0ca59756143; _tb_token_=pVUVpu3gVCQs; cookie2=0bac73354e9db62327a9d499e5315937; tt=tmall-main; pnm_cku822=203UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktzRnxFeEF6T3pDeiw%3D%7CU2xMHDJqDWIFeVd3WWZIaEYaex1xFmgSPGo8%7CVGhXd1llXGRRa1JvVm1YbVRtWmdFf0R%2BRX1Hc01wTXNPdkp%2FSmQy%7CVWldfS0SMgw2FioWNhgiBzFdLF9uSncGPxFHEQ%3D%3D%7CVmhIGCQZLQ0zDy8TLREkBDwJMQgoFCoRKgowCz4eIhwnHDwGOQxaDA%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1318*5854-client%3A1318*599-offset%3A1318*5854-screen%3A1366*768; cq=ccp%3D1; l=AhYWtIuhsQzSSe2EysvkHIFYbsIY11rx'
#COOKIE = cookielib.CookieJar()

#----------global variables----------
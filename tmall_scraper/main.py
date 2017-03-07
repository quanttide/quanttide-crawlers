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

__last_edit_date__ = '2016-6-27'

__creation_date__ = '2016-6-26'

__moduleVersion__ = '1.0.1'

__doc__ = '''

'''

#----------module document----------


#----------module import----------

# import my own modules
from TmallPageScraper import TmallPageScraper
from geventQueue import ScraperGeventQueue
from TmallCategories import CATEGORIES

from decorator import printTime

#----------module import----------


#----------function definition----------

@printTime    
def main():
    'main function of Tmall Scraper'
    
    categories = CATEGORIES
    '''
    If you want to divide the categories manually,
    you can change this sequence on different machines like that:
        categories = CATEGORIES[0:300]   # machine 1
        categories = CATEGORIES[300:600]    # machine 2
        categories = CATEGORIES[600:]    # machine 3
    '''
    
    scrapers = ScraperGeventQueue(TmallPageScraper,categories)
    scrapers.start()
    
#----------function definition----------


#----------main function----------

if __name__ == '__main__':    
    main()
    print('Web scraping is over')

#----------main function----------

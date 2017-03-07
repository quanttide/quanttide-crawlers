import random
import time
import re

from geventQueue import ScraperGeventQueue
from decorator import printTime
from categories import CATEGORIES_NAME
from proxiesPool.headers import USER_AGENTS,PROXIES


class TestPageScraper(object):
    def __init__(self,category_name,page_num=1,**url_parameters):
        self.category_name = category_name
        self.page_num = page_num
        self.url_parameters = url_parameters
        
    def start(self):
        user_agent,proxy = random.choice(USER_AGENTS),re.sub('\n','',random.choice(PROXIES))
        print(user_agent,proxy)
        time.sleep(0.01)
        print(self.category_name,self.page_num,self.url_parameters)
        
    def getTotalPageNumber(self):
        return random.choice([3,4,5])
    
@printTime    
def main():
    scrapers = ScraperGeventQueue(TestPageScraper,CATEGORIES_NAME)
    scrapers.start()

if __name__=='__main__':
    main()

# RTMartScraper
====
## Project Document
====
 * Project Name: RTMartScraper
 * Version: 1.1
 * Author：Guo Zhang,Chen Qian,Xingjianlin
 * Contributor: 
 * Data: 2016-07-24
 * Python version: 2.7.9 
 * Description: This is a RT-Mart scraper for China's Prices Project
 
----
  

## Project Structure
====
* main.py (main function)
  * RTMartPageScraper.py (a page scraper for RT-Mart APP)
  * geventQueue.py (a gevent queue for RTMartScraper)
  * RTMartCategories.py (the category list for RT-Mart)
  
  * decorator.py (decorators)

* proxiesPool
  * headers.py (user-agents,mobile user-agents and proxies for request headers) 
  * checkedProxies & proxies (IP proxies pool)
  
* serverManager(manager scraper on the server)
  * emailSending.py (send daily data and log with emails)
  * tmallscraper.sh (run the scraper)
  * tmallrar.sh (zip data)
  * tmallemail.sh (send daily emails)
  * crontab.md (guidance for make timing process)
  
 -----


## requirements
=====
   * requests
   * bs4
   * gevent
   * pymongo
   
-----   

## CHANGELOG
====
* Version 1.1.1:2016-7-24
  * 修改bug
* Version 1.1: 2016-7-24
  * 增加serverManager
* Version 1.0: 2016-7-24
  * 创建项目

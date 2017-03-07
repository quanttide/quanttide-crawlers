# RTMartScraper
====
## Project Document
====
 * Project Name: carrefourScraper
 * Version: 1.0
 * Author：Guo Zhang
 * Contributor: Xinjian Lin
 * Data: 2016-07-24
 * Python version: 2.7.9 
 * Description: This is a Carrefour scraper for China's Prices Project
 
----
  

## Project Structure
====
* main.py (main function)
  * carrefourPageScraper.py (a page scraper for Carrefour APP)
  * geventQueue.py (a gevent queue for CarrefourScraper)
  * carrefourCategories.py (the category list for RT-Mart)
  
  * decorator.py (decorators)

* proxiesPool
  * headers.py (user-agents,mobile user-agents and proxies for request headers) 
  * checkedProxies & proxies (IP proxies pool)
  
* serverManager(manager scraper on the server)
  * emailSending.py (send daily data and log with emails)
  * carrefourscraper.sh (run the scraper)
  * carrefourrar.sh (zip data)
  * carrefouremail.sh (send daily emails)
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
* Version 1.0.1: 2016-7-25
  * 修改请求头
* Version 1.0: 2016-7-24
  * 创建项目

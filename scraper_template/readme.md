# scraperModule
---
---

## Project Document
---
  * Project name: scraperModule
  * Project version: 1.0
  * Author: Guo Zhang
  * Contributer: Xingjian Lin
  * Date: 2016-5-28
  * Python version: 2.7.9
  * Descrption: This is a scarper module for China's Prices Project


## Project Structure
---
  * sampleScraper.py (main module, with parse function)
    * scraperRequest.py (request with requests)
      * scraperHeaders.py (user-agents and proxies)
        * ipProxiesList & ProxiesList (proxies)
    * scraperRequest_PyQt4.py (request with PyQt4)
    * writeData.py (write data into files or databases)
    * scraperThreadPool.py (a thread pool)
    * dataCleaning.py (clean data)
  * proxiesPool
    * get proxies
  * requirements
    * request: requests,PyQt4, 
    * parse: bs4, (lxml, html5lib,)
    * store: (MySQL-python, pymongo,)
    

## Project Version
---
  * Version 1.0 (2016-5-29):
    * First version

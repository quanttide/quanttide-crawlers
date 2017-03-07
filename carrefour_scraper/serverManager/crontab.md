# crontab

* crontab -e

* choose 3 (first time)

* edit
  *  minute hour \* \* \* sh /home/ubuntu/carrefourScraper/serverManager/carrefourscraper.sh >> /home/ubuntu/log/carrefourscraper.log 2>&1
  *  minute hour \* \* \* sh /home/ubuntu/carrefourScraper/serverManager/carrefourrar.sh >> /home/ubuntu/log/carrefourscraper.log 2>&1
  *  minute hour \* \* \* sh /home/ubuntu/carrefourScraper/serverManager/carrefouremail.sh >> /home/ubuntu/log/carrefouremail.log 2>&1
  
-----  
*　Pay attention:
　* If no log dictionary on the /home/ubuntu, it will not work.
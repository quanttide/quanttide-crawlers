# crontab

* crontab -e

* choose 3 (first time)

* edit
  *  minute hour \* \* \* sh /home/ubuntu/RTMartScraper/serverManager/rtmartscraper.sh >> /home/ubuntu/log/rtmartscraper.log 2>&1
  *  minute hour \* \* \* sh /home/ubuntu/RTMartScraper/serverManager/rtmartrar.sh >> /home/ubuntu/log/rtmartscraper.log 2>&1
  *  minute hour \* \* \* sh /home/ubuntu/RTMartScraper/serverManager/rtmartemail.sh >> /home/ubuntu/log/rtmartemail.log 2>&1
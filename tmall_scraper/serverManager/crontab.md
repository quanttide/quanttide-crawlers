# crontab

* crontab -e

* choose 3 (first time)

* edit
  * minute hour \* \* \* sh /home/ubuntu/TmallScraper/serverManager/tmallscraper.sh >> /home/ubuntu/log/tmallscraper.log 2>&1
  * minute hour \* \* \* sh /home/ubuntu/TmallScraper/serverManager/tmallrar.sh >> /home/ubuntu/log/tmallscraper.log 2>&1
  * minute hour \* \* \* sh /home/ubuntu/TmallScraper/serverManager/tmallemail.sh >> /home/ubuntu/log/tmallemail.log 2>&1
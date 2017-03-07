#!/usr/bin/python
# -*- coding: UTF-8 -*-


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Xingjian Lin'

__contributors__ = 'Guo Zhang'

__last_edit_date__ = '2016-7-24'

__creation_date__ = '2016-7-24'

__moduleVersion__ = '2.1'

__doc__ = '''
A email-sending module for China's Prices Project.
'''

#----------module document----------

#----------module import----------

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import Encoders
from email import MIMEMultipart
import mimetypes
import os
from os.path import getsize
import time
import re

#----------module import----------


#----------global variables----------

SERVER = 'nanpiao'    # server name
EMALL_ADDRESS = 'iguo19961110@foxmail.com'    # email address of the recipient 

SCRAPER_LOG = '/home/ubuntu/log/jdscraper.log'
RETAILER = 'JD'

#----------global variables----------


#----------class definition----------

class sendEmail(object):

    def __init__(self, to_addr, scraper_log, attch, from_addr = 'zhangguocpp@sina.com', password = 'zhangguo', smtp_server = 'smtp.sina.com'):
        self.from_addr = from_addr
        self.password = password
        self.smtp_server = smtp_server
        self.to_addr = to_addr
        self.scraper_log = scraper_log
        self.scraper_content = ''
        self.attch = attch
        self.main_msg = MIMEMultipart.MIMEMultipart()
        self.text_msg = ''
        self.fullText = ''
        self.match = 'Web scraping is over'

    #获得log文件的最后一行进行判断
    def getLogLastLine(self):
        filesize = getsize(self.scraper_log)
        blocksize = 1024
        data_file = open(self.scraper_log, 'rb')
        last_line = ""
        if filesize > blocksize :
            maxseekpoint = (filesize // blocksize)
            data_file.seek((maxseekpoint-1)*blocksize)
        elif filesize:
            data_file.seek(0, 0)
        lines =  data_file.readlines()
        if lines :
            last_line = lines[-1].strip()
        data_file.close()
        return last_line

    def matchLastLine(self):
        pattern = re.compile(self.match)
        match = re.search(pattern, self.getLogLastLine())
        if match:
            return True
        else:
            return False

    def getLogContent(self):
        with open(self.scraper_log, 'r') as f:
            f.seek(0, 0)
            for each_line in f.readlines():
                self.scraper_content = '{}{}'.format(self.scraper_content, each_line)
        #return self.scraper_content

    def getAttchFile(self):
        data = open(self.attch, 'r')
        ctype,encoding = mimetypes.guess_type(self.attch)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype,subtype = ctype.split('/',1)
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close( )
        Encoders.encode_base64(file_msg)#把附件编码
        # 设置附件头
        basename = os.path.basename(self.attch)
        return file_msg, basename

    def constructEmail(self, member):
        self.text_msg = MIMEText(self.scraper_content,_charset="utf-8")
        self.main_msg['subject'] = 'Scraper log by {} list'.format(member)
        self.main_msg['From'] = self.from_addr
        self.main_msg['To'] = self.to_addr
        if self.matchLastLine():
            if getsize(self.attch) <= 50007583:
                file_msg, basename = self.getAttchFile()
                file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
                self.main_msg.attach(file_msg)
            else:
                self.scraper_content = '{}{}{}'.format(self.scraper_content,'\n', 'your attchment is too large,please download by your self.')
                self.text_msg = MIMEText(self.scraper_content,_charset="utf-8")
            self.main_msg.attach(self.text_msg)
            self.fullText = self.main_msg.as_string()
        else:
            self.scraper_content = 'Web scraping is working'

    def sendEmail(self):
        server = smtplib.SMTP(self.smtp_server, 25) # SMTP协议默认端口是25
        server.set_debuglevel(False)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr], self.fullText)
            print 'send email OK'
        except smtplib.SMTPSenderRefused,e:
            print e
        server.quit()
        
#----------class definition----------


#----------main function----------

if __name__ == '__main__':
    begin = time.time()
    file_name = '/home/ubuntu/'+RETAILER+'Data_' +str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + '.rar'
    Email = sendEmail(to_addr=EMALL_ADDRESS, scraper_log=SCRAPER_LOG, attch=file_name)
    Email.getLogContent()
    Email.constructEmail(SERVER)
    Email.sendEmail()
    end = time.time()
    print 'time:',(end - begin)

#----------main function----------


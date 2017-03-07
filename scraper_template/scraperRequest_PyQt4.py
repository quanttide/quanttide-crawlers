# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__contributors__ = ''

__date__ = '2016-5-28'

__moduleVersion__ = ''

__doc__ = '''

'''

#----------module document----------


#----------module import----------

# import system modules
import time

# import third-party modules
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage

# import my own modules

#----------module import----------


#----------class definition----------


class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()
        
#----------class definition----------


#----------function definition----------

def getHTML_PyQt4(url):
    r = Render(url)    # This does the magic.Loads everything
    result = r.frame.toHtml()    # Result is a QString.
    return str(result)

#----------function definition----------


#----------main function----------


#----------main function----------
if __name__ == '__main__':
    begin = time.time()
    url = 'http://fdc.fang.com/data/land/___2______0_2.html'
    result = getHTML_PyQt4(url)
    with codecs.open('test_file','wb',encoding='utf-8') as f:
        f.write(result)
    end = time.time()
    print('time:',end-begin)
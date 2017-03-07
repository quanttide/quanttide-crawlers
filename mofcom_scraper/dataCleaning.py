# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module import----------

import re

#----------module import----------


#----------function definition----------

def cleanString(string):
    string = re.sub(' +','',string)
    string = re.sub('\n+','',string)
    string = re.sub('\r+','',string)
    string = re.sub('\t','',string)
    return string

#----------function definition----------


#----------main function----------

if __name__ =='__main__':
    string = u'\r\n\t\t\t\t\t\t\t\t\t\t\t\t\u82b1\u751f\u6cb9\r\n\t\t\t\t\t\t\t\t\t\t\t'
    newString = cleanString(string)
    print(newString)

#----------main function----------



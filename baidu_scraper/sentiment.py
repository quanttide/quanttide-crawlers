# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals

#----------module document----------

__pyVersion__ = '2.7.9'

__author__ = 'Guo Zhang'

__date__ = '2016-5-18'

__moduleVersion__ = '0.1'

#----------module document----------

#----------module import----------

import codecs
import re

import jieba

#---------module import----------


#---------global variables----------

with codecs.open('sentiment_positive',encoding='GBK') as f:
    positive = f.readlines()
positive_new = []
for i in positive:
    i = re.sub(' \n','',i)
    positive_new.append(i)

with codecs.open('sentiment_negative',encoding='GBK') as f:
    negative = f.readlines()
negative_new = []
for i in negative:
    i = re.sub(' \n','',i)
    negative_new.append(i)

#---------global variables----------


#----------function definition----------

def sentimentAnalysis(text):

    positiveScore = 0
    negativeScore = 0
    text_new = jieba.lcut(text,cut_all=False)
    
    for j in text_new:
        if j in positive_new:
            positiveScore+=1
        if j in negative_new:
            negativeScore+=1
                
    return positiveScore-negativeScore


def test():
    with codecs.open('newsList',encoding='utf-8') as f:
        newsList = f.readlines()
    newsSet = set(newsList)
    newsList_new = []
    for i in newsSet:
        i = re.sub('\n','',i)
        newsList_new.append(i)
        
    positive = []
    negative = []
    normal = []
    
    for i in newsList_new:
        text = i.split(',')[1]
        num = sentimentAnalysis(text)
        if num>0:
            positive.append(i)
        elif num<0:
            negative.append(i)
        else:
            normal.append(i)
    
    with codecs.open('positive','wb',encoding='utf-8') as f:
        for i in positive:
            f.write(i)
            f.write('\n')
            
    with codecs.open('negative','wb',encoding='utf-8') as f:
        for i in negative:
            f.write(i)
            f.write('\n')
            
    with codecs.open('normal','wb',encoding='utf-8') as f:
        for i in normal:
            f.write(i)
            f.write('\n')
            
    return len(positive),len(negative),len(normal)

#----------function definition----------

positive,negative,normal = test()
print('positive:',positive)
print('negative:',negative)
print('normal:',normal)
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


import codecs

import jieba


def mergeFiles(newName,*fileNames):
    newsList = []
    for fileName in fileNames:
        with codecs.open(fileName,'rb',encoding='utf-8') as f:
            newsList.extend(f.readlines()[1:])
    newsSet = set(newsList)
    newsList = list(newsSet)
    with codecs.open(newName,'wb',encoding='utf-8') as f:
        f.writelines(newsList)
        

def wordsFrequencyCount(fileName):
    
    with open(fileName,'rb') as f:
        myList = f.readlines()

    mySet = set(myList)

    text_list = []
    for i in mySet:
        i = i.decode('utf-8')
        text = i.split(',')[1]
        new_text = jieba.lcut(text,cut_all=False)
        text_list.extend(new_text)
        
    text_dict = {}
    for i in text_list:
        if i in text_dict.keys():
            text_dict[i]+=1
        else:
            text_dict[i]=1
            
    final_list = sorted(text_dict.iteritems(), key=lambda d:d[1], reverse = True)
    
    for i,j in final_list:
        print(i,j)
        with open('wordsStats_'+fileName,'ab') as f:
            f.write(i.encode('utf-8'))
            f.write(',')
            f.write(str(j).encode('utf-8'))
            f.write(',\n')  
            

def searchingWords(newFileName,words,filenames,printout=True):
    newsList = []
    for filename in filenames:
        with codecs.open(filename,'rb',encoding='utf-8') as f:
            theList = f.readlines()
            for i in theList:
                if words in i:
                    newsList.append(i)
    if printout:
        for i in newsList:
            print(i)
    
    with codecs.open('searchWords_'+newFileName,'wb',encoding='utf-8') as f:
        f.writelines(newsList)
                    
                
def test():
    '''
    mergeFiles('newsList_短租_all','newsList_短租.txt','newsList_短租市场_no.txt','newsList_短租市场.txt','newsList_短租平台_yes.txt','newsList_短租平台.txt')
    fileName = 'newsList_短租_all'
    #fileName = 'newsList_短租.txt'
    wordsFrequencyCount(fileName)
    '''
    searchingWords('中国_短租_all','中国',['newsList_短租_all',],)
    
    
if __name__=='__main__':
    test()
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


from mofcomGoodsScraper import pageScraper,categoryScraper


def addScraper():
    categories = [
    
     #['粮油','玉米','/channel/gxdj/jghq/jg_list.shtml?craft_index=13086&par_craft_index=13073'],
     #['粮油','糯米','/channel/gxdj/jghq/jg_list.shtml?craft_index=8754700&par_craft_index=13073'],
     #['蔬菜','香菜','/channel/gxdj/jghq/jg_list.shtml?craft_index=13504&par_craft_index=13075'],
     #['蔬菜','土豆','/channel/gxdj/jghq/jg_list.shtml?craft_index=20413&par_craft_index=13075'],
     ['蔬菜','黄瓜','/channel/gxdj/jghq/jg_list.shtml?par_craft_index=13075&craft_index=20410'],
     #['蔬菜','白萝卜','/channel/gxdj/jghq/jg_list.shtml?craft_index=20408&par_craft_index=13075'],
     #['畜产品','基础母牛(500斤左右)','/channel/gxdj/jghq/jg_list.shtml?craft_index=15060767&par_craft_index=13079'],
     #['水产品','活草鱼','/channel/gxdj/jghq/jg_list.shtml?craft_index=8754711&par_craft_index=13080'],
    #['畜产品','黄花母鸡','/channel/gxdj/jghq/jg_list.shtml?craft_index=15092420&par_craft_index=13079'],
    #['畜产品','三黄公鸡','/channel/gxdj/jghq/jg_list.shtml?craft_index=15092423&par_craft_index=13079'],
    #['畜产品','老母鸡','/channel/gxdj/jghq/jg_list.shtml?craft_index=13329&par_craft_index=13079'],
    #['畜产品','活鹅','/channel/gxdj/jghq/jg_list.shtml?craft_index=8754641&par_craft_index=13079'],
    #['畜产品','三黄鸡','/channel/gxdj/jghq/jg_list.shtml?craft_index=13328&par_craft_index=13079'],
    #['畜产品','牛肉','/channel/gxdj/jghq/jg_list.shtml?craft_index=13235&par_craft_index=13079'],
    #['畜产品','猪肉(白条猪)','/channel/gxdj/jghq/jg_list.shtml?craft_index=13233&par_craft_index=13079'],
    #['畜产品','鸡蛋','/channel/gxdj/jghq/jg_list.shtml?craft_index=13245&par_craft_index=13079'],
     
     ] 
    
    for category in categories:
        categoryName = category[0]
        goodsName = category[1]
        goodsURL = category[2]
        fail_url_list = categoryScraper(categoryName, goodsName, goodsURL)
        print(goodsName)
        with open('fail_list_again2','ab') as f:
            f.writelines(fail_url_list)
            
addScraper()
# -*- coding:utf-8 -*-
#@Time  : 2020/4/22 14:57
#@Author: Huangshaofei
#@File  : main.py
# -*- coding:utf-8 -*-
# @Time  : 2020/4/16 15:48
# @Author: Huangshaofei
# @File  : 第一个爬虫.py
from crawl.crawler_buff import craw_by_price
from multiprocessing import Pool
from filter.Compare import *
from multiprocessing import Manager

if __name__ == '__main__':
    """create a list can be shared by different process"""
    category_item = Manager().list()
    craw_by_price(category_item)
    print("We have crawed the data already")
    """filtrate the item list and find the useful info"""
    #sublist = filtrate(category_item)
    """output the outcome"""
    #for each_item in sublist:
        #print("Name: ", each_item.name, end=" ")
        #print("roi: ", each_item.roi)
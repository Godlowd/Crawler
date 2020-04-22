# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 21:30
# @Author: Huangshaofei
# @File  : crawler.py
from config import *
from crawl import Requester
from config.URL import *
from multiprocessing import Pool
import time
import config.Setting


def craw_by_price(category_item, category=None):
    """get the root's url and json"""
    root_url = goods_section_root_url(category)
    root_json = Requester.get_root_json(root_url)
    """if the json return normally"""
    if root_json is not None:
        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']
        print(total_count)
        page_url = goods_section_page_url(None, 2)
        print(page_url)
        """calculate the time of the process"""
        starttime = time.time()
        pool = Pool(processes=4)
        pool.map(Requester.get_json, page_url)
        pool.close()
        pool.join()
        #print(len(config.Setting.category_item))
        endtime = time.time()
        print('总共耗时: ', float(endtime - starttime))
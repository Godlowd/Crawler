# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 21:30
# @Author: Huangshaofei
# @File  : crawler.py
from config import *
from crawl import Requester
from config.URL import *
from multiprocessing import Pool
import time
from requests import *

from multiprocessing import Manager


def craw_by_price(item, category=None):
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
        #print(len(category_item))
        endtime = time.time()
        print('总共耗时: ', float(endtime - starttime))


# def get_json(url):
#     time.sleep(1)
#     try:
#         page_json = get(url, headers=Requester.headers, cookies=Requester.cookies, timeout=5).json()
#         print(category_item)
#         if page_json is not None:
#             """items on this page"""
#             items_json = page_json['data']['items']
#             for item in items_json:
#                 """get item"""
#                 csgo_item = Requester.collect_item(item)
#                 if csgo_item is not None:
#                     category_item.append(csgo_item)
#
#                     # config.Setting.category_item.append(csgo_item)
#                     # category_item_add(csgo_item)
#     except Timeout:
#         print("timeout for {}. Try again.".format(url))

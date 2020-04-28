# -*- coding:utf-8 -*-
# @Time  : 2020/4/22 14:57
# @Author: Huangshaofei
# @File  : main.py
# -*- coding:utf-8 -*-
# @Time  : 2020/4/16 15:48
# @Author: Huangshaofei
# @File  : 第一个爬虫.py
import time
from functools import partial
from multiprocessing import Pool
import multiprocessing
from requests import get, Timeout
from config.URL import *
from config.Setting import *
from crawl import Requester, craw_history_price
from filter import Compare
import crawl.crawler_buff


def get_json(url, category_item):
    time.sleep(1)
    try:
        page_json = get(url, headers=Requester.headers, cookies=Requester.cookies, timeout=5).json()
        if page_json is not None:
            """items on this page"""
            items_json = page_json['data']['items']
            for item in items_json:
                """get item"""
                csgo_item = Requester.collect_item(item)
                if csgo_item is not None:
                    category_item.append(csgo_item)
                    # config.Setting.category_item.append(csgo_item)
                    # category_item_add(csgo_item)
    except Timeout:
        print("timeout for {}. Try again.".format(url))
    except ValueError:
        print(url)


if __name__ == '__main__':
    """create a list can be shared by different process"""
    starttime = time.time()
    item = multiprocessing.Manager().list()
    crawl.crawler_buff.craw_by_price(item)
    print("We have crawed the data already")
    category = []
    # craw_history_price.craw_history_price(item)
    for each_item in item:
        category.append(each_item)
    sublist = list(filter(Compare.filtrate, category))
    sublist.sort(key=lambda Item: Item.roi)
    """filtrate the item list and find the useful info"""
    """output the outcome"""
    for each_item in sublist:
        print("Name: ", each_item.name, end=" ")
        print("roi: ", each_item.roi)

    endtime = time.time()
    print("程序总共耗时: ", float(endtime - starttime))

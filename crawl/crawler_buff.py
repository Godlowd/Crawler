# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 21:30
# @Author: Huangshaofei
# @File  : crawler.py
from functools import partial

from config import *
from crawl import Requester
from config.URL import *
from multiprocessing import Pool
import time
from requests import *
from config.Setting import PROCESS_NUM


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


def craw_by_price(item, category=None):
    """get the root's url and json"""
    root_url = goods_section_root_url(category)
    root_json = Requester.get_root_json(root_url)
    """if the json return normally"""
    if root_json is not None:
        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']
        print("所有物品数: ", total_count)
        """get all the urls to iterate"""
        print("总页数", total_page)
        all_pages = all_page_url(total_page)
        """calculate the time of the process"""
        starttime = time.time()
        p = Pool(processes=PROCESS_NUM)
        partial_func = partial(get_json, category_item=item)
        p.map(partial_func, all_pages)
        p.close()
        p.join()
        endtime = time.time()
        print('总共耗时: ', float(endtime - starttime))
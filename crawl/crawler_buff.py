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
                history_prices = []
                sold_time = []
                steam_price_url = steam_price_history_url(item['id'])
                history_price_json = Requester.get_root_json(steam_price_url)

                if history_price_json is not None and history_price_json['code'] == "OK":
                    days = history_price_json['data']['days']
                    raw_price_history = history_price_json['data']['price_history']
                    for pair in raw_price_history:
                        if len(pair) == 2:
                            sold_time.append(pair[0] / 1000)
                            history_prices.append(float(pair[1]))
                """get item"""
                csgo_item = Requester.collect_item(item,history_prices,days)
                            # set history price if exist
                if csgo_item is not None:
                    category_item.append(csgo_item)


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
        print('爬取现在价格总共耗时: ', float(endtime - starttime))

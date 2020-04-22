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
from crawl import Requester
"""define the number of the process"""
process_num = 6


def filtrate(category_item: list):
    for each in category_item:
        compare(each)
        """if we can not make profit by selling it neither on steam nor buff, remove it from the list"""
        if each.sellatsteam is not True and each.sellatbuff is not True:
            category_item.remove(each)
    category_item.sort(key=lambda Item: Item.roi)
    return category_item


def compare(Item):
    roi = calculate(Item.price, Item.steam_predict_price)
    Item.roi = roi
    if roi > ROI_STEAM:
        Item.sellatsteam = True
    elif roi < ROI_BUFF:
        Item.sellatbuff = True


def calculate(price_in_buff, price_in_steam):
    """calculate the ROI if we buy a item at buff and sell it at steam"""
    ROI = (price_in_steam * 0.85 - price_in_buff) / price_in_buff
    return ROI


def get_json(url, category_item):
    time.sleep(1)
    try:
        page_json = get(url, headers=Requester.headers, cookies=Requester.cookies, timeout=5).json()
        # print(category_item)
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


def craw_by_price(category=None):
    global item
    """get the root's url and json"""
    root_url = goods_section_root_url(category)
    root_json = Requester.get_root_json(root_url)
    """if the json return normally"""
    if root_json is not None:
        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']
        print("所有物品数: ", total_count)
        # page_url = goods_section_page_url(category, )
        # print(page_url)
        """get all the urls to iterate"""
        print(total_page)
        all_pages = all_page_url(total_page)

        """calculate the time of the process"""
        starttime = time.time()
        p = Pool(processes=process_num)
        partial_func = partial(get_json, category_item=item)
        p.map(partial_func, all_pages)
        p.close()
        p.join()
        # print(len(category_item))
        endtime = time.time()
        print('总共耗时: ', float(endtime - starttime))


if __name__ == '__main__':
    """create a list can be shared by different process"""
    item = multiprocessing.Manager().list()
    craw_by_price()
    print("We have crawed the data already")
    for each_item in item:
        print(each_item.name, each_item.price)
    category = []
    for each_item in item:
        category.append(each_item)

    sublist = filtrate(category)
    """filtrate the item list and find the useful info"""
    """output the outcome"""
    for each_item in sublist:
        print("Name: ", each_item.name, end=" ")
        print("roi: ", each_item.roi)

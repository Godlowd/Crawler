# -*- coding:utf-8 -*-
# @Time  : 2020/4/22 17:53
# @Author: Huangshaofei
# @File  : SecondMain.py
from multiprocessing import Manager
import time
import requests
from crawl import Requester

"""create a list can be shared by different process"""
category_item = Manager().list()


def get_json(url):
    time.sleep(1)
    try:
        page_json = requests.get(url, headers=Requester.headers, cookies=Requester.cookies, timeout=5).json()
        # print(category_item)
        if page_json is not None:
            """items on this page"""
            items_json = page_json['data']['items']
            for item in items_json:
                """get item"""
                csgo_item = Requester.collect_item(item)
                if csgo_item is not None:
                    category_item.append(csgo_item)
                    print(len(category_item))
                    # config.Setting.category_item.append(csgo_item)
                    # category_item_add(csgo_item)
    except requests.Timeout:
        print("timeout for {}. Try again.".format(url))

    print("We have crawed the data already")
    """filtrate the item list and find the useful info"""
    # sublist = filtrate(category_item)
    """output the outcome"""
    # for each_item in sublist:
    # print("Name: ", each_item.name, end=" ")
    # print("roi: ", each_item.roi

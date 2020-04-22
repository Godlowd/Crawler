# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 21:01
# @Author: Huangshaofei
# @File  : Requester.py
import requests
from requests import Timeout
import time
import os
from config.Setting import COOKIE
from config.Item import *
from functools import partial
from config.Setting import category_item_add
import config.Setting

FATHER_PATH = os.path.abspath(os.path.dirname(os.getcwd()))
RESULT_PATH = os.path.join(FATHER_PATH, 'result', 'result.txt')

"""Request header"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

"""Request proxies"""
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}

"""Request cookie"""
cookies = {}
for line in COOKIE.split(';'):
    k, v = line.split('=', 1)
    cookies[k] = v


def collect_item(item):
    buff_id = item['id']
    name = item['name']
    min_price = item['sell_min_price']
    sell_num = item['sell_num']
    steam_url = item['steam_market_url']
    steam_predict_price = item['goods_info']['steam_price_cny']
    buy_max_price = item['buy_max_price']

    # restrict price of a item
    return Item(buff_id, name, min_price, sell_num, steam_url, steam_predict_price, buy_max_price)


def get_json(url,category_item=None):
    time.sleep(1)
    try:
        page_json = requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
        print(category_item)
        if page_json is not None:
            """items on this page"""
            items_json = page_json['data']['items']
            for item in items_json:
                """get item"""
                csgo_item = collect_item(item)
                if csgo_item is not None:
                    pass

                    # config.Setting.category_item.append(csgo_item)
                    # category_item_add(csgo_item)
    except Timeout:
        print("timeout for {}. Try again.".format(url))


def get_root_json(url):
    time.sleep(1)
    try:
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
    except Timeout:
        print("timeout for {}. Try again.".format(url))

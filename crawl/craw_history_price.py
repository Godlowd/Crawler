# -*- coding:utf-8 -*-
# @Time  : 2020/4/23 23:25
# @Author: Huangshaofei
# @File  : craw_history_price.py
import time

import config.URL
import crawl.Requester
from functools import partial
from multiprocessing import Pool
from config.Setting import PROCESS_NUM
import config.Item


def craw_history_price(item: config.Item):
    history_prices = []
    item_id = item.id
    steam_price_url = config.URL.steam_price_history_url(item_id)
    history_price_json = crawl.Requester.get_root_json(steam_price_url)

    if history_price_json is not None and history_price_json['code'] == "OK":
        days = history_price_json['data']['days']
        print(days)
        raw_price_history = history_price_json['data']['price_history']
        for pair in raw_price_history:
            if len(pair) == 2:
                history_prices.append(float(pair[1]))

        # set history price if exist
        if len(history_prices) != 0:
            item.set_history_prices(history_prices, days)


def get_history_price(item: list):
    starttime = time.time()
    p = Pool(processes=PROCESS_NUM)
    p.map(craw_history_price, item)
    p.close()
    p.join()
    endtime = time.time()
    print('爬取历史价格总共耗时: ', float(endtime - starttime))
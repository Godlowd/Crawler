# -*- coding:utf-8 -*-
# @Time  : 2020/4/19 15:58
# @Author: Huangshaofei
# @File  : Compare.py
from crawl.crawler_buff import *
from config import Item
from config.Setting import ROI_BUFF, ROI_STEAM
from operator import attrgetter


def filtrate(item: Item):
    compare(item)
    if item.sellatsteam is not True and item.sellatbuff is not True:
        return False
    elif item.sell_num < 10:
        return False
    elif len(item.history_prices) < 10:
        return False
    else:
        return True


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

# -*- coding:utf-8 -*-
# @Time  : 2020/4/19 15:58
# @Author: Huangshaofei
# @File  : Compare.py
from crawl.crawler_buff import *
from config import Item
from config.Setting import ROI_BUFF, ROI_STEAM


def filtrate(category_item: list):
    for each in category_item:
        compare(each)
        """if we can not make profit by selling it neither on steam nor buff, remove it from the list"""
        if each.sellatsteam is not True and each.sellatbuff is not True:
            category_item.remove(each)
        elif each.sell_num < 10:
            category_item.remove(each)
        elif len(each.history_prices) < 10:
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




# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 9:11
# @Author: Huangshaofei
# @File  : URL.py
from config.Setting import MAX_PRICE, MIN_PRICE
import sys

BUFF_ROOT = 'https://buff.163.com/'
BUFF_GOODS = BUFF_ROOT + 'api/market/goods?'
BUFF_HISTORY_PRICE = BUFF_ROOT + 'api/market/goods/price_history?'
BUFF_HISTORY_PRICE_CNY = BUFF_ROOT + 'api/market/goods/price_history/buff?'


def goods_root_url():
    return BUFF_ROOT + 'market/?game=csgo#tab=selling&page_num=1'


def category_root_url(category):
    return BUFF_GOODS + 'game=csgo&page_num=1&category=%s' % category


def category_page_url(page_num, category):
    return BUFF_GOODS + 'game=csgo&page_num={}&category={}'.format(page_num, category)


def steam_price_history_url(item_id):
    """7 days history prices"""
    return BUFF_HISTORY_PRICE + 'game=csgo&goods_id={}&currency=&days=7'.format(item_id)


def buff_price_history_url(item_id):
    return BUFF_HISTORY_PRICE_CNY + 'game=csgo&goods_id={}&currency=CNY&days=7'.format(item_id)


def goods_section_root_url(category):
    """
    buff is strange: only request with page number beyond actual upper bound,
    can you get the true page number with this price section.
    """

    base = BUFF_GOODS + 'game=csgo&page_num={}&sort_by=price.asc&min_price={}&max_price={}' \
        .format(sys.maxsize, MIN_PRICE, MAX_PRICE)
    if category is not None:
        base += '&category={}'.format(category)

    return base


def goods_section_page_url(category, page_num):
    """return the URL and sort them with the price descendant"""
    base = BUFF_GOODS + 'game=csgo&page_num={}&sort_by=price.desc&min_price={}&max_price={}' \
        .format(page_num, MIN_PRICE, MAX_PRICE)

    if category is not None:
        base += '&category={}'.format(category)

    return base


def all_page_url(total_page: int = 2):
    base = [BUFF_GOODS + 'game=csgo&page_num={}&sort_by=price.desc&min_price={}&max_price={}'.format(str(i), MIN_PRICE,
                                                                                                     MAX_PRICE) for i in
            range(1, total_page)]
    return base

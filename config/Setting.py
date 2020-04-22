# -*- coding:utf-8 -*-
# @Time  : 2020/4/18 9:05
# @Author: Huangshaofei
# @File  : Setting.py
import sys
import json
import os
import configparser
from config.Item import *

"""the list of the category item"""




config = configparser.RawConfigParser()
# config
CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.ini'
CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_DIR, CONFIG_FILE_NAME)
"""read the config file"""
try:
    config.read(CONFIG_PATH, encoding='utf-8')
except IOError:
    print('File {} does not exist. Exit!'.format(CONFIG_PATH))
    exit(1)

# cookie
COOKIE = config['BASIC']['cookie']

# price
config_filter = config['FILTER']
"""最小值大于0"""
MAX_PRICE = max(0, float(config_filter['max_price']))
MIN_PRICE = config_filter['min_price']

# ROI
ROI_STEAM = config.getfloat('RATIO', 'ROI_STEAM')
ROI_BUFF = config.getfloat('RATIO', 'ROI_BUFF')


def category_item_add(item: Item):
    category_item.append(item)


def category_item_remove(item: Item):
    category_item.remove(item)

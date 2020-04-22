# -*- coding:utf-8 -*-
# @Time  : 2020/4/22 14:57
# @Author: Huangshaofei
# @File  : main.py
# -*- coding:utf-8 -*-
# @Time  : 2020/4/16 15:48
# @Author: Huangshaofei
# @File  : 第一个爬虫.py
from functools import partial
from multiprocessing import Pool
from filter.Compare import *
import multiprocessing
from config.URL import *

"""define the number of the process"""
process_num = 1


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
        #page_url = goods_section_page_url(category, )
        #print(page_url)
        """get all the urls to iterate"""
        all_pages = all_page_url()

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
        print(each_item.name)
    # sublist = filtrate(item)
    # """filtrate the item list and find the useful info"""
    # """output the outcome"""
    # for each_item in sublist:
    #     print("Name: ", each_item.name, end=" ")
    #     print("roi: ", each_item.roi)

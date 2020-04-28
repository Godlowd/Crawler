# -*- coding:utf-8 -*-
# @Time  : 2020/4/22 17:55
# @Author: Huangshaofei
# @File  : test.py
lst = [1, 1, 0, 2, 0, 0, 8, 3, 0, 2, 5, 0, 2, 6]

for item in lst:
    if item == 0:
        lst.remove(item)
print (lst)

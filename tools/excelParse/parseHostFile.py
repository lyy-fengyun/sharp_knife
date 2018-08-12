#!/bin/env python
# coding=utf-8
# Script Name	: parseHostFile.py
# Author		: liyayong
# Created		: 2018/5/25 17:26
# Last Modified	:
# Version		: 1.0

# Modifications	: 

# Description	:
__author__ = "liyayong"

import sys
import csv
import unittest

# reload(sys)
# sys.setdefaultencoding("utf-8")

'''
functions: 
'''

def parse_csv_file(file_name):
    '''
    解析csv文档，转换内容后输出到文件中
    :param file_name:
    :return:
    '''
    user_list = {}

    index = 1
    with open(file_name,'r') as f_in:
        f_csv = csv.DictReader(f_in)

        for row in f_csv:
            if index == 1:
                index += 1
                continue
            else:
                parse_list(row,user_list)
    print()
    for key,value in user_list.items():
        print(key+": "+str(value))

    convert_mapList_to_listMap(user_list,file_name.split('.')[0]+"-conv.csv")

def parse_list(list_of_user,user_dict):
    '''
    解析单个csv文件内容
    :param list_of_user:
    :param user_dict:
    :return:
    '''
    print(list_of_user)
    for host,user in list_of_user.items():
        # print(info)
        # host,user = info
        ori_user = user.strip()
        if len(ori_user) == 0:
            continue
        user = ori_user.split(' ')[0]
        id = ori_user.split(' ')[1]
        id = 501 if not len(id) else  id
        # print(id)
        if int(id) < 200:
            continue

        list_of_host = user_dict.get(user)
        if list_of_host is None:
            list_of_host = []
            user_dict[user] = list_of_host

        list_of_host.append(host)

def convert_mapList_to_listMap(map_of_list,conv_file_name):
    '''
    转化 map of list type of date to list of map
    :param map_of_list:
    :return:
    '''
    raws = []
    heads = map_of_list.keys()
    heads = sorted(heads)
    max_value=1
    for key in heads:
        list_len  = len(map_of_list.get(key))
        max_value = max_value if max_value >= list_len else list_len

    for index in range(max_value):
        raw_dict = {}
        for key in heads:
            host_list = map_of_list.get(key)
            if index < len(host_list):
                raw_dict[key] = host_list[index]
            else:
                raw_dict[key] = ''
        raws.append(raw_dict)

    with open(conv_file_name,'w') as f_out:
        f_csv_out = csv.DictWriter(f_out,fieldnames=heads)
        f_csv_out.writeheader()
        f_csv_out.writerows(raws)

    print()
    for list_raw in raws:
        print(str(list_raw))




# gloable variable

# functions
def main():
    '''
    main control function
    '''
    pass


def test():
    '''
       回归测试函数
    '''
    unittest.main()


if __name__ == "__main__":
    parse_csv_file("upay.csv")
    parse_csv_file("youjiaka.csv")
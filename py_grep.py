#!/usr/bin/python
# coding='utf-8'

import os
import glob
import unittest

def file_find(file_pattern):
    '''
    find file name by file pattern
    :param file_pattern:
    :return: list of file name
    '''
    return  glob.glob(file_pattern)

def cmd_run(cmd):
    '''
    run shell command in linux
    :param cmd:
    :return: output
    '''
    pro = os.popen('cmd')
    return pro.readlines()


def gen_grep_cmd(grepthing,file_list):
    '''
    generate command to run
    :param grepthing:
    :param file_list:
    :return:
    '''
    return ['grep '+grepthing+" "+x for x in file_list]


if __name__ == '__main__':
    ans = cmd_run('ls')
    print(ans)